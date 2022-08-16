
import os
from unicodedata import category
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import *

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    def paginate(num_of_questions, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * num_of_questions
        end = start + num_of_questions

        books = [book.format() for book in selection]
        return books[start:end]

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true")
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            cats = [cat.format()['type'] for cat in Category.query.all()]
            return jsonify({
                "categories": cats
            })
        except BaseException:
            abort(400)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_all_questions():
        try:
            questions = paginate(
                num_of_questions=QUESTIONS_PER_PAGE,
                selection=Question.query.order_by(
                    Question.id).all())
            return jsonify({
                "questions": questions,
                "total_questions": len(questions),
                "categories": [d.format()['type'] for d in Category.query.all()]
            })

        except BaseException:
            abort(400)

    @app.route('/search', methods=['POST'])
    def search_question():

        try:
            term = request.get_json()['search_term']
            selection = Question.query.filter(
                Question.question.ilike(
                    '%{}%'.format(term))).all()
            questions = [d.format() for d in selection]
            cat = None
            for i in questions:
                cat = i['category']
                break
            result = jsonify({
                "questions": questions,
                "total_questions": len(questions),
                "current_category": cat,
            })
            return result
        except BaseException:
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def del_question(q_id):
        question = Question.query.filter(Question.id == (q_id)).one_or_none()
        id = question.format()['id']
        ques = question.format()['question']
        if question is not None:
            question.delete()
            question.update()
            return jsonify({
                "success": True,
                "deleted": id,
                "question": ques
            })
        else:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:

            data = request.get_json()
            category = int(data["category"]) + 1
            question = Question(
                data['question'],
                data['answer'],
                category,
                data['difficulty'])
            question.insert()
            question.update()
            print([d.format() for d in Question.query.filter(
                Question.category == category).all()])
            return jsonify({
                "success": True,
                "created": question.format()['question'],
                "total_questions": len(Question.query.all())
            })
        except BaseException:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions')
    def get_questions_by_category(cat_id):
        id = cat_id + 1
        category = Category.query.filter(Category.id == id).one_or_none()

        if category is not None:
            questions = [q.format() for q in Question.query.filter(
                Question.category == category.format()['id']).all()]
            result = jsonify({
                "questions": questions,
                "total_questions": len(questions),
                "current_category": category.format()['type']
            })
            return result
        else:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        data = request.get_json()
        previous = data['previous_questions']
        category = int(data['quiz_category']['id']) + 1
        try:
            questions = Question.query.filter(
                Question.category == category).all()

            if data['quiz_category']['type'] == 'click':
                questions = Question.query.all()

            next_ups = []

            for i in questions:
                if i.format()["category"] not in previous:
                    next_ups.append(i)
                print(previous)
            if next_ups:
                return jsonify({
                    "question": next_ups[random.randrange(-1, len(next_ups))].format()
                })
            else:
                return jsonify({})
        except BaseException:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400,
                       'message': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404,
                       'message': 'Not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422,
                       'message': 'Unprocessable'}), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 500,
                       'message': 'Internal Error'}), 500
    return app
