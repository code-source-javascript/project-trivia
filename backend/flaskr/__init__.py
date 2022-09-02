from ast import Not, expr
import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app,resources={r'/api/*':{'origins':'*'}})
    CORS(app)

    # function for pagination
    def setup_pagination(request, data):
        page = request.args.get('page', 1, type=int)
        item_per_page = 10
        start = (page - 1)*item_per_page
        end = start + item_per_page
        formatted_data = [info.format() for info in data]
        return formatted_data[start:end]

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Allow-Control-Access-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Allow-Control-Access-Methods",
                             "GET,POST,DELETE,PATCH,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    def get_categories():
        error = False
        # categories = []
        category = {}
        try:
            data = Category.query.order_by('id').all()
            categories = [info.format() for info in data]

            for cat in categories:
                key = str(cat.get("id"))
                category[key] = cat.get('type')
        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'categories': category,
                    'totalCategories': len(categories)
                })

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
    @app.route('/questions', methods=['GET'])
    def get_questions():
        error = False
        questions = []
        data = []
        category = {}
        try:

            data = Question.query.order_by('id').all()
            questions = setup_pagination(request, data)
            print(questions)
            category_data = Category.query.order_by('id').all()
            categories = [info.format() for info in category_data]

            for cat in categories:
                key = str(cat.get("id"))
                category[key] = cat.get('type')
        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'totalQuestions': len(data),
                    'categories': category
                })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = False
        try:
            question = Question.query.get(question_id)
            question.delete()
        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                })

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
    def post_question():
        error = False
        question = {}
        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()

        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True
                })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        error = False
        questions = []
        try:
            searchTerm = request.json.get('searchTerm')
            question_data = Question.query.filter(
                Question.question.like('%' + searchTerm+'%')).all()
            questions = [data.format() for data in question_data]
        except:
            error = True

        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'totalQuestions': len(questions),
                    'currentCategory': ''
                })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def category_question(category_id):
        error = False
        questions = []
        current_category = {}
        try:
            data = Question.query.filter_by(category=category_id).all()
            questions = [info.format() for info in data]
            current_category = Category.query.get(category_id)
        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'totalQuestions': len(questions),
                    'currentCategory': current_category.type
                })

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
        error = False
        quiz = {}
        try:
            body = request.get_json()
            found = False
            checker = False
            final = False
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            print(previous_questions)

            if len(previous_questions) == 0:
                data = Question.query.filter(
                    Question.category == quiz_category['id']).first()
                print('here')
                quiz = data.format()
            else:
                __questions = Question.query.all()
                questions = [_question.format() for _question in __questions]

                for question in questions:
                    if found:
                        for quest in previous_questions:
                            if quest == question['id']:
                                final = False
                                break
                            else:
                                final = True

                        if final:
                            final = False
                            found = False
                            quiz = question
                            break
                        else:
                            found = False
                            continue
                    else:
                        for _previous in previous_questions:
                            if _previous == question['id']:
                                checker = False
                            else:
                                checker = True

                        if checker:
                            if str(question['category']) == str(quiz_category['id']):
                                found = True
                                quiz = question
                            else:
                                continue
                        else:
                            continue

        except:
            error = True
        finally:
            if error:
                abort(400)
            else:
                return jsonify({
                    'success': True,
                    'question': quiz
                })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    return app
