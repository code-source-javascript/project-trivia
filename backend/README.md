# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

Getting Started 
  .Base URL: At present this api can only be run locally and is not hosted as a base URL. The backend app is hosted at the default http://127.0.0.1:5000/ which is set as a proxy in the frontend configuration.


### Error Handling

Errors are returned as JSON objects in the following format:

```json
  {
    "success":False,
    "error":400,
    "message":"Bad Request"
  }
 ```  
  The API will return three error types when requests fail
    - 400 Bad Request 
    - 404 Resource Not Found
    - 422 Unprocessable Entity
    - 405 Method Not Allowed 
    - 500 Internal Server Error
  



### Endpoints

`curl http://localhost:5000/categories -X GET`

- Fetches a dictionary of categories, totalCategories, and success
- Request Arguments: None
- Returns: An object with  `categories`, that contains an object of `id: category_string` key: value pairs , `success` with value `True` which signifies success and `totalCategories` which defines the number of category items in the database .

```json
{ "categories":{
  "1":"Science",
  "2":"Art",
  "3":"Geography",
  },
  "success":true,
  "totalCategories":6
}
```

`curl http://localhost:5000/questions -X GET`

- Fetches a dictionary of categories,paginated questions based on the query parameter value, success and totalQuestions 
- Request Arguments: None
- Query Parameter: `/questions?page=1`
- Returns: An object with  `categories`, that contains an object of `id: category_string` key: value pairs , `questions`, which is an array of object containing  keys `answer, category, difficulty, id and question` , `success` with value `True` which signifies successful process and `totalQuestions` which defines the number of question items in the database .

```json
{
  "categories":{
  "1":"Science",
  "2":"Art"
  },
  "questions":[
    {
      "answer":"Apollo 13",
      "category":5,
      "difficulty":4,
      "id":2,
      "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer":"Tom Cruise",
      "category":5,
      "difficulty":4,
      "id":4,
      "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success":true,
  "totalQuestions":18
  
}
```

`curl http://localhost:5000/questions/6 -X DELETE`

- Deletes a particular question
- Request Arguments: `question id`
- Returns: An object with  `success` with value `True` which signifies successful deletion and `question` with value of deleted question id

```json
{ 
  "success":true,
  "question":6
}
```



`curl http://localhost:5000/questions -X POST -H 'Content-Type:application/json' -d '{"question":"How many continents are in the world","answer":"Seven","difficulty":1,"category":3 }' `

- Create a question with it answer,difficulty, and category
- Request Arguments: None
- Request Body: `{"question":String,"answer":String,"difficulty":Integer,"category":Integer } `
- Returns: An object with  `success` with value `True` which signifies successful creation and `question` which is an object that contains it fields and values of the question created

```json
{
  "question":{
    "answer":"Seven",
    "category":3,
    "difficulty":1,
    "id":31,
    "question":"How many continents are in the world"
    },
    "success":true
  }
```


`curl http://localhost:5000/questions/search -X POST -H 'Content-Type:application/json' -d '{"searchTerm":"What" }' `

- Retrieve questions based on a searchTerm
- Request Arguments: None
- Request Body: `{"searchTerm":"What"}`
- Returns: An object with  `success` with value `True` which signifies successful search,  `questions` which is an array of objects  containing it fields and values, `totalQuestions` defining the total question found and `currentCategory` giving the name of the current category.

```json
{
  "currentCategory":"ALL",
  "questions":[
    {
      "answer":"Muhammad Ali",
      "category":4,
      "difficulty":1,
      "id":9,
      "question":"What boxer's original name is Cassius Clay?"
    },
    {
      "answer":"Apollo 13",
      "category":5,
      "difficulty":4,
      "id":2,
      "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    ],
    "success":true,
    "totalQuestions":2
  }
```

`curl http://localhost:5000/categories/6/questions -X GET `

- Retrieve questions based on some category
- Request Arguments: `category_id`
- Returns: An object with  `success` with value `True` which signifies successful fetch,  `questions` which is an array of objects that contains it fields and values `totalQuestions`defining the total question found and `currentCategory` gives a value for the current category.

```json
{
  "currentCategory":"Geography",
  "questions":[
    {
      "answer":"Muhammad Ali",
      "category":3,
      "difficulty":1,
      "id":9,
      "question":"What boxer's original name is Cassius Clay?"
    },
    {
      "answer":"Apollo 13",
      "category":3,
      "difficulty":4,
      "id":2,
      "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    ],
    "success":true,
    "totalQuestions":2
  }
```



`curl http://localhost:5000/quizzes -X POST -H 'Content-Type:application/json' -d 'json={"previous_questions":[1,2],"quiz_category":0 }' `

- Retrieve unrepeatred quiz questions in relation to a category
- Request Arguments: None
- Request Body: `{"previous_questions":Array, "quiz_category":Integer}`
- Returns: An object with  `success` with value `True` which signifies successful quiz selection,  `question` which is an array of objects that contains it fields and values

```json
{
  "question":{
      "answer":"Muhammad Ali",
      "category":4,
      "difficulty":1,
      "id":9,
      "question":"What boxer's original name is Cassius Clay?"
    },
    "success":true,
   
  }
```





## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
