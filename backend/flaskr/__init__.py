import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get("page", 1, type=int)
    
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    paged_questions = [question.format() for question in questions]
    
    paginated_questions = paged_questions[start:end]
    
    return paginated_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app = Flask(__name__)
    setup_db(app)
    # This CORS app passing allows * for origins
    cors = CORS(app, resources={r"/api/*":{"origins": "*"}})
    

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        return response
   
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        all_categories = [category.format() for category in categories]

        #This condition checks if the categories have data in them
        if len(all_categories) == 0:
            abort(404, "No category found")
        


        else:
            category_dict = {}
            
            # this block loops into the formatted category which is returned
            # as a list of several dictionaries(object) and converts it to a single dictionary

            for category in all_categories:
                category_dict[category['id']] = category['type']
            
            return jsonify({
                "success": True,
                "categories": category_dict,
                "total_categories": len(category_dict)
            })



    @app.route('/questions')
    def get_questions():
        page = request.args.get("page", 1, type=int)
        questions = Question.query.order_by(Question.id).all()
        current_page = paginate_questions(request, questions)

        categories = Category.query.all()
        all_categories = [category.format() for category in categories]
        category_dict = {}
        
        for category in all_categories:
            category_dict[category['id']] = category['type']
        
        if len(current_page) == 0:
            abort(404, "No questions for now, check back later")

        else:
            return jsonify({
                "success": True,
                "questions": current_page,
                "total_questions": len(Question.query.all()),
                #"current_category": None,
                "categories": category_dict,
                "page": page
            })

    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
       # try:
        question = Question.query.get(question_id)
            
        if question == None:
            abort(404, "Question not found")
            
        else:
            question.delete()
            questions = Question.query.all()
            #all_questions = paginate_questions(request, questions)

            return jsonify({
                   # "questions": all_questions,
                    "success": True,
                    "deleted": question_id
                })
        #except:
            #abort(422,"Delete action not processed")        
    # """
    
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # """

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
 
        question = body['question']
        answer = body['answer']
        category = body['category']
        difficulty = body['difficulty']

        new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            
            #this block validates the existence of the incoming category
        check_category = Question.query.get(category)
        if check_category == None:
            abort(406, "Category doesn't exist. Hint: (category:{between 1 to 6})")
            
        else:
            try:
                new_question.insert()
                
                questions = Question.query.order_by(Question.id).all()
                current = [question.format() for question in questions]
                
                return jsonify({
                    "success": True,
                    "added_question":new_question.id,
                    "questions": current
                    })
            except:
                    abort(400, "Something is not right with your request, Please check again")
                    
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search = body['searchTerm']

    
        question = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
        search_questions = [questions.format() for questions in question]



        return jsonify({
            "success": True,
            "questions": search_questions,
            #"search-term": search,
            "total_questions": len(search_questions)#,
            #"current_category": search_questions.category
        })

        
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_by_category(id):
        questions = Question.query.filter(Question.category == id).all()
        if questions == 0 or None:
            abort(404, "Question not found")

        else:
            category_confirm = Category.query.get(id)

            if category_confirm == None:
                abort(406,"Category doesn't exist. Hint: (category:{between 1 to 6})")
            
            else:
                current_questions = paginate_questions(request, questions)
                
                categories = Category.query.filter(Category.id == id).all()
                category_format = [category.format() for category in categories]
                category_dict = {}
                for check in category_format:
                    category_dict[check['id']] = check['type']
                
                return jsonify({
                    "success":True,
                    "questions": current_questions,
                    "current_category": category_dict
                })
    

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        
        try:
            body = request.get_json()

            current_category = body.get('quiz_category')
            previous_question = body.get('previous_questions')



            if current_category['type'] == 'click':
                gotten_questions = Question.query.filter(Question.id.notin_((previous_question))).all()

            else: 
                gotten_questions = Question.query.filter_by(category=current_category['id']
                ).filter(Question.id.notin_((previous_question))).all()

            questions = gotten_questions[random.randrange(0, len(gotten_questions))].format() if len(gotten_questions) > 0 else None

            return jsonify({
                "success": True,
                "question": questions
            })
        except:
            abort(422, "Quiz not found")
        
        
        
        
        
        
        
        
        
        
        
        


    # """
    # @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "Error": f"Oops!, {error}"
        }),404

    @app.errorhandler(422)
    def not_processed(error):
        
        return jsonify({
            "success": False,
            "Error": f"Sorry, {error}"
        }),422

    @app.errorhandler(400)
    def bad_request(error):
        
        return jsonify({
            "success": False,
            "Error": f"{error}"
        }),400

    @app.errorhandler(406)
    def not_acceptable(error):
        return jsonify({
            "success": False,
            "Error":f'{error}'
        }),406
    return app

