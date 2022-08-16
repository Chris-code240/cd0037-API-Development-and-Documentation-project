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
        self.database_name = "test_trivia"
        self.database_path = "postgres://{}/{}".format(
            'postgres:Liukangs240@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            "question": "What is my favorite programming language?",
            "answer": "Python",
            "category": 3,
            "difficulty": 1}

        self.new_quiz = {
            "previous_questions": [18],
            "quiz_category": {"type": "Art", "id": 2}
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
        self.assertEqual(res.status_code, 200)
        self.assertEqual(not data['categories'], False)

    def test_could_not_get_all_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(not data['success'], True)

    def test_add_new_quest(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_could_not_add_question(self):
        res = self.client().post(
            '/questions',
            json={
                "question": "What is my favorite programming language?",
                "answer": "Python",
                "category": 51,
                "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)

    def test_get_all_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_could_not_get_all_questions(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_search_question(self):
        res = self.client().get('/questions', json={"seach_term": "language"})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_could_not_search_for_question(self):
        res = self.client().post('/questions', json={"seach_term": "chicken"})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        ques = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(not ques, True)

    def test_could_not_delete_question(self):
        res = self.client().delete('/questions/43')
        data = json.loads(res.data)
        ques = Question.query.filter(Question.id == 43).one_or_none()

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(not ques, True)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(not data['questions'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_get_quizzes(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def testcould_not_get_quizzes(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [18],
                "quiz_category": {
                    "type": "Art",
                    "id": 6}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(not data,True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
