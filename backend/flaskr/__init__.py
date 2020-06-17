import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
     #Set up CORS. Allow '*' for origins
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/')
    def hello():
        return jsonify({'message':'Hello, World!'})

    #Get all categories to Json
    @app.route('/api/categories')
    def get_categories():
      try:         
        return jsonify(get_all_categories())
      except Exception as e:
        logging.exception(e)

    #Get all categories
    def get_all_categories():
      try: 
        categories = Category.query.all()
        format_categories = [categorie.format() for categorie in categories]
        return format_categories
      except Exception as e:
        logging.exception(e)

    def filter_questions(category_id=None):
      try:
        search_term = request.args.get('searchTerm')
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        if search_term:
          questions = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
            ).all()

        elif category_id:
          questions = Question.query.filter_by(category=str(category_id)).all()
        else:
          questions = Question.query.all()

        total_questions = len(questions)
        format_quesions = [question.format() for question in questions][start:end]

        if(total_questions == 0):
            abort(404)

        #Return a list of questions
        return jsonify({
            'success': True,
            'questions': format_quesions,
            'total_questions': total_questions,
            'current_category': category_id if category_id else 0,
            'categories': get_all_categories()
        })
      except Exception as e:
        logging.exception(e)

    #Get all questions
    @app.route('/api/questions')
    def get_questions():
      return filter_questions()

    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
      return filter_questions(category_id)
    
    return app

#   '''
#   TEST: At this point, when you start the application
#   you should see questions and categories generated,
#   ten questions per page and pagination at the bottom of the screen for three pages.
#   Clicking on the page numbers should update the questions. 
#   '''

#   '''
#   @TODO: 
#   Create an endpoint to DELETE question using a question ID. 

#   TEST: When you click the trash icon next to a question, the question will be removed.
#   This removal will persist in the database and when you refresh the page. 
#   '''

#   '''
#   @TODO: 
#   Create an endpoint to POST a new question, 
#   which will require the question and answer text, 
#   category, and difficulty score.

#   TEST: When you submit a question on the "Add" tab, 
#   the form will clear and the question will appear at the end of the last page
#   of the questions list in the "List" tab.  
#   '''

#   '''
#   @TODO: 
#   Create a POST endpoint to get questions based on a search term. 
#   It should return any questions for whom the search term 
#   is a substring of the question. 

#   TEST: Search by any phrase. The questions list will update to include 
#   only question that include that string within their question. 
#   Try using the word "title" to start. 
#   '''

#   '''
#   @TODO: 
#   Create a GET endpoint to get questions based on category. 

#   TEST: In the "List" tab / main screen, clicking on one of the 
#   categories in the left column will cause only questions of that 
#   category to be shown. 
#   '''


#   '''
#   @TODO: 
#   Create a POST endpoint to get questions to play the quiz. 
#   This endpoint should take category and previous question parameters 
#   and return a random questions within the given category, 
#   if provided, and that is not one of the previous questions. 

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not. 
#   '''

#   '''
#   @TODO: 
#   Create error handlers for all expected errors 
#   including 404 and 422. 
#   '''

    return app

    