from flask import Flask, render_template, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

TEMP_DIR = 'temp_codes'
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.form['code']
    input_data = request.form['input']

    filename = f"{TEMP_DIR}/temp_{uuid.uuid4().hex}.py"
    with open(filename, 'w') as f:
        f.write(code)

    try:
        result = subprocess.run(
            ['python', filename],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)
    finally:
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify({'output': output})

if __name__ == '__main__':
    from os import environ
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)
