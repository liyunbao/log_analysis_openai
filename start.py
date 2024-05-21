from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# Replace with your API key
openai.api_key = "your_openai_api_key_here"

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    global openai
    openai.api_key = request.form['openai_key']
    # other config here
    return jsonify({'success': True})

@app.route('/message', methods=['POST'])
def message():
    if not not openai.api_key:
        return jsonify({'error': 'Configuration is missing. Please provide the OpenAI API key.'}), 400

    user_input = request.form['user_input']
    response = send_request(user_input)
    return jsonify({'response': response})

def send_request(user_input):
    # no-op
    user_input = "list all the exceptions"
    top_result = ""
    with open("D:/log_sample.txt", "r") as f:
        top_result = f.read()

    # print(top_result)
    print(user_input)

    analysis_input = f"With the following user input {user_input} please analyze the following this log messages: {top_result}"
    analysis = [{"role": "system",
                 "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause."},
                {"role": "user", "content": analysis_input}]

    analysis_response = client.chat.completions.create(
        model="gpt-4",
        messages=analysis,
        temperature=0,
    )

    print(analysis_response)
    analysis = analysis_response["choices"][0]["message"]["content"].strip()
    return analysis

if __name__ == "__main__":

    app.run(host="localhost", port=5000, debug=True)





