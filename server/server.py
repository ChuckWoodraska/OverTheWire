from flask import Flask, send_from_directory, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)


@app.route('/<path:path>')
def send_python(path):
    return send_from_directory('python', path)


@app.route('/imports_load')
def imports_load():
    return jsonify({'imports': ['neat', 'hello']})


# @app.route('/commands')
# def commands():
#     return jsonify([])


@app.route('/commands')
def commands():
    return jsonify([{'import_list': ['schedule'], 'import_base_url': 'https://raw.githubusercontent.com/dbader/schedule/master', 'main': 'scan', 'main_base_url': 'http://127.0.0.1:5002'}])


@app.route('/save_db', methods=['POST'])
def save_db():
    f = request.files['scans']
    f.save(os.path.join('./db_files', '{}{}.db'.format(f.filename, datetime.now())))
    return jsonify({'data': 'file uploaded successfully'})


@app.route('/load_db')
def load_db():
    return send_from_directory('db_files', 'scans.db')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
