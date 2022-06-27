## API Reference

## Trivia API

#### Introduction

The trivia api is a quiz Api with endpoints that can handle creation of questions and returning questions in a random order for quizzes. The APi was designed as a project for Udacity Backend development course. It runs on Flask's framework and it was designed following the [Pep-8 guidelines](https://peps.python.org/pep-0008/).

#### Getting Started

• Base-url : the project still runs locally as it is yet to be hosted. The base-url can be found at:

`localhost:5000/`

•  Authentication: This version of the application is not designed to use any authentication or API keys.

#### ERROR HANDLING

Errors in the application are returned in JSON format, coupled with traditional http response codes
Sample codes:
+2xx : This indicates that a request is successful, an example is the status code '200'.
+4xx: indicates that something is not right about the request.

Expected Error codes and their meaning:

- 400 : This indicates that the request is either not properly formatted or there are some missing data
- 406: The request is not acceptable
- 422 : Cannot process a request
- 404: The resource(question or category) is not found

An error response example:
This is what an error message would look like

```json
{
"Success" : False,
"Error": "oops! 404 method not found"
}
```

### End Points:

#### GET

###### `/categories`

The categories endpoints returns all the categories available as a collection of quiz.

##### Sample

```javascript
curl http://localhost:5000/categories
```

The `response` will be formatted this way if successful:

```json
"categories": {
"1" : "Science",
"2" :"Art",
 "3" : "Geography",
"4" : "History",
"5" : "Entertainment",
"6" : "Sports"
}
```

###### `/categories/{id}/questions`

Handles the request to get questions based on a category.

####Sample

```javascript
 curl http://localhost:5000/categories/2/questions
```

-Response

```Json

{
"success": true,
"current_category":{
"6": "sports"
},
{
"questions":[{
"question": "Who won the last world cup?",
"answer ": "France",
"category": "6",
"difficulty": "4"
}, {
"question": "Who won the last ballon d'or?",
"answer": "Lionel Messi",
"category": "6",
"difficulty": "3"
}]
}
```

###### `/questions`

This endpoint returns list of questions and their category, the total number of pages
This endpoint is paginated to show 10 questions per page.

#### Sample

```javascript
curl http://localhost:5000/questions
```

-Response:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "page": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

This endpoint also accepts a `page` parameter that indicates the `page` number and the total questions to display per `page` is 10, it also returns availabe categories.

```javascript
GET /questions?page=5
```

#### POST

###### `/questions`

This endpoint allows you to create and add questions to the application, it takes

- questions
- category
- answer
- difficulty
  as its parameter.
  They are all required to create a `POST` request to this endpoint.

#### Sample

```javascript
curl -X POST -d '{"question": "Who won the last Uefa Champions league title?", "answer": "Real Madrid", "category": "6", "difficulty":"2"}' localhost:5000/questions -H "Content-Type: application/json"
```

-Response

```json
{
  "success": true,
  "added_question": 1
}
```

##### `/questions/search`

This endpoint is used to search for questions, which only takes the search term as parameter in the `POST` request body.

```javascript
curl localhost:5000/questions/search -X POST -d '{"search_term":"name"}'
```

##### `/quizzes`

This endpoints returns questions for quizzes, the questions are randomly returned. It takes `previous_questions` and `quiz_category` as parameters.

####Sample

```javascript
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions": [], "quiz_category": {"type": "click","id": "0" }}'
```

-Response
Generated randomly.

```json
{
  "current_category": "2",
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}
```

#### DELETE

This endpoint deletes or removes a question by providing an `id`. You can only delete a question with question`id` on this endpoint

####Sample
`curl -X DELETE http://localhost:5000/questions/6`

-Response

```Json
{
"deleted": 34,
"success" : true
}
```
