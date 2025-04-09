from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from werkzeug.utils import secure_filename
import os
import utils

UPLOAD_FOLDER = './uploads'
FILE_CONTENT = None
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set you api key in config file named API_KEY
# or set the OPENAI_API_KEY Environment Variable
# Unix/Linux/MacOS: export OPENAI_API_KEY=your_api_key
# Windows: set OPENAI_API_KEY=your_api_key
client = OpenAI(api_key=open('API_KEY').read().strip())

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
def send_message():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the content from the JSON data
    content = data.get('content')

    # Here you can process the received message, for now, let's just print it
    print("Received message:", content)

    # response = "Message received successfully!"
    response = send_request(content)
    return jsonify({'response': response})

def send_request(user_input):
    file_content = utils.getFileContent(UPLOAD_FOLDER)
    analysis_input = f"With the following user input {user_input} please analyze the following this log messages: {file_content}"
    analysis = [{"role": "system",
                 "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause and how to fix it. In a friendly way"},
                {"role": "user", "content": analysis_input}]

    analysis_response = client.responses.create(
        # After fine tuned your model, replace with your model
        #model="ft:gpt-3.5-turbo-0125:personal::9S5KSrpa",
        model="gpt-4o-mini",
        input=analysis,
    )
    response = analysis_response.output_text
    print(response)
    response = response.replace('\n', '\\n')
    response = response.replace('####', '')
    response = response.replace('###', '')
    return response

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)





