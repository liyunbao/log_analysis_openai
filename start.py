from flask import Flask, render_template, request, jsonify
import openai
from werkzeug.utils import secure_filename
import os

# Replace with your API key
openai.api_key = "your_openai_api_key_here"
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize variables for Elasticsearch and OpenAI clients
openai.api_key = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    global openai
    openai.api_key = request.form['openai_key']
    # other config here
    return jsonify({'success': True})


@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        file = request.files['file']
        #f.save(f.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': True})
            #return render_template("Acknowledgement.html", name=f.filename)


@app.route('/message', methods=['POST'])
def message():
    if not not openai.api_key:
        return jsonify({'error': 'Configuration is missing. Please provide the OpenAI API key.'}), 400

    user_input = request.form['user_input']
    response = send_request(user_input)
    return jsonify({'response': response})

def send_request(user_input):
    user_input = "list all the exceptions"
    top_result = ""
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]
    print(f'*************{onlyfiles}')
    log_file = None
    if len(onlyfiles) > 1:
        log_file = onlyfiles[0]

    with open(log_file, "r") as f:
        top_result = f.read()

    # print(top_result)
    print(user_input)

    analysis_input = f"With the following user input {user_input} please analyze the following this log messages: {top_result}"
    analysis = [{"role": "system",
                 "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause."},
                {"role": "user", "content": analysis_input}]

    analysis_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=analysis,
        temperature=0,
    )

    print(analysis_response)
    analysis = analysis_response["choices"][0]["message"]["content"].strip()
    return analysis

if __name__ == "__main__":

    app.run(host="localhost", port=5000, debug=True)





