import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import random
import logging

from models import setup_db, Question, Category
from sqlalchemy import func
from werkzeug.exceptions import HTTPException


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  # Set up CORS. Allow '*' for origins
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                          'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                          'GET,POST,DELETE,OPTIONS')
    return response

  # Get all categories to Json
  @app.route('/api/categories')
  def get_categories():
    try:
        return jsonify(get_all_categories())
    except Exception as e:
        logging.exception(e)

  # Get all categories

  def get_all_categories():
    try:
        categories = Category.query.all()
        format_categories = [categorie.format()
                              for categorie in categories]
        return format_categories
    except Exception as e:
        logging.exception(e)

  # Get questions by searchTerm or category_id  including pagination

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
            questions = Question.query.filter_by(
                category=str(category_id)).all()
        else:
            questions = Question.query.all()

        total_questions = len(questions)
        format_quesions = [question.format()
                            for question in questions][start:end]

        if(total_questions == 0):
            abort(404)

        # Return a list of questions
        return jsonify({
            'success': True,
            'questions': format_quesions,
            'total_questions': total_questions,
            'current_category': category_id if category_id else 0,
            'categories': get_all_categories()
        })
    except Exception as e:
        logging.exception(e)

  # Get all questions

  @app.route('/api/questions')
  def get_questions():
    return filter_questions()

  # Get questions by category_id
  @app.route('/api/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    return filter_questions(category_id)

  # POST a new question
  @app.route('/api/questions', methods=['POST'])
  def add_question():
    data = request.get_json()

    question = data.get("question", None)
    answer = data.get("answer", None)
    difficulty = data.get("difficulty", None)
    category = data.get("category", None)

    if not all([question, answer, category, difficulty]):
      abort(400)

    try:
        question = Question(
          question=question,
          answer=answer,
          category=category,
          difficulty=difficulty
        )
        question.insert()

        return filter_questions(category)
    except Exception as e:
        logging.exception(e)
        abort(500)

  #Delete a question
  @app.route('/api/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.filter(
            Question.id == question_id
        ).one_or_none()

    if question is None:
        abort(404)
    try:
        # delete question       
        question.delete()

        # return response
        return jsonify({
            'success': True,
            'deleted_id': question.id
        })
    except Exception as e:
        logging.exception(e)
        abort(500)

  #Get random question for the quiz
  @app.route('/api/quizzes', methods=['POST'])
  def quizzes_game():
    try:
      data = request.get_json()
      if data is None:
          previous_questions = []
          quiz_category = {}
      else:
          previous_questions = data.get('previous_questions', [])
          quiz_category = data.get('quiz_category', {})

      query = Question.query

      if 'id' in quiz_category:
          query = query.filter(Question.category == quiz_category['id'])

      question = query.filter(
          Question.id.notin_(previous_questions)
      ).order_by(func.random()).first()

      return jsonify({
                'success': True,
                'question': question.format() if question else False,
                'previous_questions': previous_questions,
            })
      
    except Exception as e:
      logging.exception(e)
      abort(500)

    '''
    Create error handlers for all expected errors
    including 404 and 422.
    '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
      }), 405

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
      }), 500
    
          


  return app