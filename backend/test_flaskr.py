import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

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

    def test_get_categories(self):
        
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(data.status_code,200)
        self.assertTrue(data[0]["id"])
        self.assertTrue(data[0]["type"])
        self.assertEqual(len(data), Category.query.count())

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()