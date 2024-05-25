from flask import Flask, render_template, request, jsonify
from openai import OpenAI
client = OpenAI()
from werkzeug.utils import secure_filename
import os
import utils

# Replace with your API key
OpenAI.api_key = "your token"
UPLOAD_FOLDER = './uploads'
FILE_CONTENT = None
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize variables and OpenAI clients
OpenAI.api_key = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    global OpenAI
    OpenAI.api_key = request.form['openai_key']
    # other config here
    return jsonify({'success': True})


@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        file = request.files['file']
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': True})
            #return render_template("Acknowledgement.html", name=f.filename)


@app.route('/message', methods=['POST'])
def message():
    if not not OpenAI.api_key:
        return jsonify({'error': 'Configuration is missing. Please provide the OpenAI API key.'}), 400

    user_input = request.form['user_input']
    response = send_request(user_input)
    return jsonify({'response': response})

def send_request(user_input):
    #user_input = "list all the exceptions and errors and analyze the root causes"
    file_content = utils.getFileContent(UPLOAD_FOLDER)
    analysis_input = f"With the following user input {user_input} please analyze the following this log messages: {file_content}"
    analysis = [{"role": "system",
                 "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause."},
                {"role": "user", "content": analysis_input}]

    analysis_response = client.chat.completions.create(
        #model="gpt-4",
        model="ft:gpt-3.5-turbo-0125:personal::9S5KSrpa",
        messages=analysis,
        temperature=0,
    )

    print(analysis_response)
    return str(analysis_response.choices[0].message.content.strip())

if __name__ == "__main__":

    app.run(host="localhost", port=5000, debug=True)





