from flask import Blueprint, request, jsonify, url_for
from flask_cors import CORS
import random
import json
import os
import threading
from utils.image_handlers import delete_images
from generateQuestionPaper import generate_question
import diagram

questions_bp = Blueprint('questions', __name__)
CORS(questions_bp)

# Remove the @current_app.csrf.exempt decorator
@questions_bp.route('/diagram', methods=['POST'])
def diagram_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Define output folder for diagrams
    output_folder = os.path.join(os.getcwd(), 'static', 'result')
    os.makedirs(output_folder, exist_ok=True)

    # Call the diagram drawing function with the provided JSON (wrapped in a list)
    diagram.draw_shape([data], output_folder=output_folder)

    # Build URL for the generated image
    image_filename = f"{data['id']}.png"
    image_url = url_for('static.static_file', filename=os.path.join('result', image_filename), _external=True)
    return jsonify({'image_url': image_url})

@questions_bp.route('/nvr', methods=['GET'])
def nvr():
    # Generate images for random question (excluding 3,4)
    valid_nums = [i for i in range(1, 13) if i not in [3, 4]]
    question_num = random.choice(valid_nums)
    question_data = generate_question(question_num)
    question_info = list(question_data.values())[0]

    # Build URLs for question assets
    question_url = url_for('static.static_file', filename=question_info['question'])
    answer_url = url_for('static.static_file', filename=question_info['answer'])
    distractor_urls = [url_for('static.static_file', filename=path) for path in question_info['distractors']]

    threading.Timer(300, delete_images, args=(question_info['question'], question_info['answer'], *question_info['distractors'])).start()

    return jsonify({
        'questions': [{
            'question': question_url,
            'answer': answer_url,
            'distractors': distractor_urls,
            'text': question_info['text'],
            'explanation': question_info['explanation']
        }]
    })

@questions_bp.route('/spatial', methods=['GET'])
def spatial():
    question_data = generate_question(random.choice([3, 4]))
    question_info = list(question_data.values())[0]

    question_url = url_for('static.static_file', filename=question_info['question'])
    answer_url = url_for('static.static_file', filename=question_info['answer'])
    distractor_urls = [url_for('static.static_file', filename=path) for path in question_info['distractors']]

    threading.Timer(300, delete_images, args=(question_info['question'], question_info['answer'], *question_info['distractors'])).start()

    return jsonify({
        'questions': [{
            'question': question_url,
            'answer': answer_url,
            'distractors': distractor_urls,
            'text': question_info['text'],
            'explanation': question_info['explanation']
        }]
    })

@questions_bp.route('/english', methods=['GET'])
def english():
    static_dir = os.path.join(os.getcwd(), 'static', 'data')
    with open(os.path.join(static_dir, 'english.json'), 'r') as file:
        data = json.load(file)
    return jsonify(data)

@questions_bp.route('/maths', methods=['GET'])
def maths():
    static_dir = os.path.join(os.getcwd(), 'static', 'data')
    with open(os.path.join(static_dir, 'maths.json'), 'r') as file:
        data = json.load(file)
    return jsonify(data)

@questions_bp.route('/vr', methods=['GET'])
def vr():
    static_dir = os.path.join(os.getcwd(), 'static', 'data')
    with open(os.path.join(static_dir, 'vr.json'), 'r') as file:
        data = json.load(file)
    return jsonify(data)
