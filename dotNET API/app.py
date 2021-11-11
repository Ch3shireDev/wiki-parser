import os
from flask import Flask, send_from_directory, jsonify, request, Response
from flask_cors import CORS
from json import dumps, load
from lib import get_tags, get_elements, find_elements

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


static = os.path.join(os.path.dirname(__file__), 'static')

elements = get_elements('elements.json')
tags = get_tags('tags.json')
types = get_elements('types.json')


@app.route('/api/tags')
def get_tags():
    return jsonify(tags)

@app.route('/api/types')
def get_types():
    return jsonify(types)

@app.route('/')
def index():
    return send_from_directory(static, 'index.html')


@app.route('/app.js')
def file():
    return send_from_directory(static, 'app.js')


@app.route('/style.css')
def style():
    return send_from_directory(static, 'style.css')


@app.route('/api/elements')
def find_elements():
    tags = request.args.get('tags')
    types = request.args.get('types')
    tag_names = tags.split(',')
    type_names = types.split(',')
    result = find_elements(elements, type_names, tag_names)
    return jsonify(result)


app.run(debug=True, port=80)
