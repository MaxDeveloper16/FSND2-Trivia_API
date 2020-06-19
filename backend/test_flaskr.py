import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

from flaskr import create_app
from models import setup_db, Question, Category

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_path = 'postgres://{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST, DB_NAME)
 
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question':'Do you have a pet?',
            'answer':'Yes',
            'category':1,
            'difficulty':1
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #Test get_categories
    def test_get_categories(self):
        
        #request
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(data[0]["id"])
        self.assertTrue(data[0]["type"])
        self.assertEqual(len(data), Category.query.count())

    #Test get_questions
    def test_get_questions(self):
       
        #request
        total_questions = Question.query.count()

        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])
        self.assertEqual(total_questions,data['total_questions'])
        self.assertEqual(0,data['current_category'])

    #Test get_questions_by_category
    def test_get_questions_by_category(self):
              
        category_id = Category.query.first().id
        total_questions = Question.query.filter_by(
                category=str(category_id)).count()
        
        #request
        res = self.client().get('/api/categories/'+str(category_id)+'/questions')
        data = json.loads(res.data)

        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])
        self.assertEqual(total_questions,data['total_questions'])
        self.assertEqual(category_id,data['current_category'])

    #Test get_questions with searchTerm 
    def test_get_questions_by_searchTerm(self):
        
        question = Question.query.first()
        search_term = question.question

        #request
        res = self.client().get('/api/questions?search_term='+search_term)
        data = json.loads(res.data)

        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(0,data['current_category'])

    #Test add_question
    def test_add_question(self):
        
        #request
        res = self.client().post('/api/questions',json=self.new_question)
        question = Question.query.filter_by(question=self.new_question['question'])
        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(question)

    #Test delete_question
    def test_delete_question(self):
        question = Question.query.order_by(desc(Question.id)).first()
        
        #request
        res = self.client().delete('/api/questions/'+str(question.id))
        self.assertEqual(res.status_code, 200)

        #assert
        deleted = Question.query.filter_by(id=question.id).first()
        self.assertIsNone(deleted)

    #Test quizzes_game
    def test_quizzes_game(self):
        
        #request
        res = self.client().post('/api/quizzes')
        data = json.loads(res.data)
        
        #assert
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['question'])
        self.assertTrue(data['success'])

    #Test 404
    def test_405_errorhandler(self):
        
        #request
        res = self.client().post('/api/categories')
        data = json.loads(res.data)

        #assert
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['error'],405)
        self.assertEqual(data['message'],'Method not allowed')


        



    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()