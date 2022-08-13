import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:Liukangs240@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"question":"What is my favorite programming language?","answer":"Python","category":"Programming Languages","difficulty":1}

        self.new_quiz = {
            "previous_questions":[1],
            "quiz_category":{"type":"Phone","id":2}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(not data['categories'],False)

    def test_add_new_quest(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
    
    def test_get_all_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_search_question(self):
        res = self.client().get('/questions',json={"seachTerm":"name"})

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        
    def test_delete_question(self):
        res = self.client().delete('/questions/7')
        data = json.loads(res.data)
        ques = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
        self.assertEqual(ques,None)
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(not data['questions'],False)

    def test_get_quizzes(self):
        res = self.client().get('/quizzes',json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(not data['questions'],False)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()