# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development

export DB_NAME=trivia
export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=localhost:5432
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
Before runing the tests, you can change test database info to your test database
```bash
export DB_NAME=trivia
export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=localhost:5432
```

To run the tests with 'unittest'
```bash
python -m unittest
```

Or run the tests with below command
```bash
python test_flaskr.py
```

## API Reference
### Getting Started
The API follows the RESTful API guideline. The api is served at port 5000, which for local development translates to:
#### Base URL
http://127.0.0.1:5000

#### API Keys /Authentication
There is no authentication system in place

### Error Handlers
You can expect the following types of errors from API:
- 400: Bad Request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal Server Error

#### Example
```json
{
"success":False,
"error":500,
"message":"Internal Server Error"
}
```
### Resource endpoint library

#### Category

Requests for all available categories. 

###### Example
```bash
curl http://127.0.0.1:5000/api/categories
```
###### Response

```json
[
    {
        "id": 1,
        "type": "Science"
    },
    {
        "id": 2,
        "type": "Art"
    },
    {
        "id": 3,
        "type": "Geography"
    },
    {
        "id": 4,
        "type": "History"
    },
    {
        "id": 5,
        "type": "Entertainment"
    },
    {
        "id": 6,
        "type": "Sports"
    }
]
```

#### Question
Requests for questions, including pagination (every 10 questions). 

###### Example
```bash
curl http://127.0.0.1:5000/api/categories/2/questions
```
###### Response

```json
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "current_category": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "text",
            "category": 2,
            "difficulty": 2,
            "id": 28,
            "question": "Test2"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

#### Add a new question
- Creates a new question
- Parameters
    - question (string)
    - answer (string)
    - difficulty (integer)
    - category (integer)

###### Example

```bash
curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{"answer":"yes", "question":"Do you have a cat?", "category":1, "difficulty": 1}'
```
###### Response

```json
{
"id":52,
"category":1,
"difficulty":1,
"question":"Do you have a cat?",
"answer":"yes",
}
```

#### Delete a question
Delete a question.

###### Example

```bash
curl -X DELETE http://127.0.0.1:5000/api/questions/52
```
###### Response

```json
{
"deleted_id":52,
"success":true
}
```

#### Play quizzes
Play quizzes.

###### Example

```bash
curl -X POST 'http://127.0.0.1:5000/api/quizzes' \
-H 'Content-Type: application/json' \
-d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'
```
###### Response

```json
{
    "previous_questions":[],
    "question":
        {
            "answer":"test",
            "category":1,
            "difficulty":1,
            "id":27,
            "question":"Test"
    },
    "success":true
}
```