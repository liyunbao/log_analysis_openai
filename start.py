from flask import Flask, render_template, request, jsonify
import openai
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
openai.api_key = open('API_KEY').read()
# Initialize variables and OpenAI clients
client = openai.OpenAI()

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

@app.route('/message_test', methods=['POST'])
def send_message():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        # Extract the content from the JSON data
        content = data.get('content')

        # Here you can process the received message, for now, let's just print it
        print("Received message:", content)

        # response = "Message received successfully!"
        response = send_request(content)
        return jsonify({'response': response}), 200
    except Exception as e:
        # If any error occurs, return an error response
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def message():
    #if not not openai.api_key:
    #    return jsonify({'error': 'Configuration is missing. Please provide the OpenAI API key.'}), 400

    user_input = request.form['user_input']
    response = send_request(user_input)
    return jsonify({'response': response})

def send_request(user_input):
    #user_input = "list all the exceptions and errors and analyze the root causes"
    file_content = utils.getFileContent(UPLOAD_FOLDER)
    analysis_input = f"With the following user input {user_input} please analyze the following this log messages: {file_content}"
    analysis = [{"role": "system",
                 "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause and how to fix it. In a friendly way"},
                {"role": "user", "content": analysis_input}]


    analysis_response = client.chat.completions.create(
        #model="gpt-4",
        #model="ft:gpt-3.5-turbo-0125:personal::9S5KSrpa",
        model="gpt-3.5-turbo",
        messages=analysis,
        temperature=0,
    )
    print(analysis_response)
    response = str(analysis_response.choices[0].message.content.strip())
    response = response.replace('\n', '\\n')
    response = response.replace('####', '')
    response = response.replace('###', '')
    return response
    '''
    #response = 'Hey there! I\'ve taken a look at the log messages you provided, and it seems like everything is running smoothly without any exceptions, errors, or warnings. However, I did notice some CPU-intensive processes that might be causing high CPU usage.\n\n1. The process "minerva-processor.minerva-process-query" seems to be quite CPU-intensive, with an elapsed time of 1.345 seconds and a peak CPU usage of 5912 kCPU. This process might be a potential candidate for optimization to reduce CPU load.\n\n2. Another CPU-intensive process is "minerva-processor.evaluate-query" with an elapsed time of 1.33 seconds and a peak CPU usage of 1434 kCPU. This process could also benefit from optimization to improve performance and reduce CPU usage.\n\nTo address the high CPU usage caused by these processes, you may consider the following steps:\n\n1. **Optimization**: Review the code and algorithms used in the CPU-intensive processes to identify any inefficiencies or bottlenecks. Optimize the code to reduce unnecessary computations and improve performance.\n\n2. **Resource Allocation**: Ensure that the resources allocated to these processes are sufficient but not excessive. Adjust resource allocations based on the actual requirements of the processes to prevent unnecessary strain on the CPU.\n\n3. **Monitoring**: Implement monitoring tools to keep track of CPU usage over time and identify any spikes or patterns of high usage. This will help in proactively addressing any performance issues before they escalate.\n\nBy optimizing the CPU-intensive processes and monitoring CPU usage effectively, you can improve overall system performance and prevent any potential issues related to high CPU usage. Let me know if you need further assistance or more details on this analysis!'
    response = 'Hey there! I see you\'ve provided a log snippet containing memory usage records from various events in the lot. Let\'s dive into the analysis:\n\n1. **Memory Usage Trends:**\n   - I noticed that there are events with varying memory usage patterns. For example, "minerva-processor.minerva-process-query" and "minerva-processor.evaluate-query" events exhibit relatively high memory usage compared to others.\n\n2. **Correlation with Event Characteristics:**\n   - There seems to be a correlation between the type of event and memory usage. Events like "minerva-processor.evaluate-query" and "ds.validate" have higher memory allocations compared to events like "qp.run-query" which have minimal memory usage.\n\n3. **Memory-Intensive Events:**\n   - Events like "minerva-processor.minerva-process-query" and "minerva-processor.evaluate-query" stand out as memory-intensive events, potentially impacting overall memory usage in the system.\n\n4. **Recommendations:**\n   - To optimize memory usage, consider implementing memory management techniques like efficient resource allocation and deallocation strategies.\n   - For memory-intensive events, optimize resource allocation and consider adjusting resource limits based on historical memory usage patterns.\n   - Additionally, scheduling memory-intensive events during off-peak hours or distributing them across different time intervals can help in balancing memory usage.\n\n**Root Cause:**\n- The memory-intensive events are likely causing spikes in memory usage, potentially leading to performance degradation if not managed efficiently.\n\n**Action Plan:**\n- Monitor memory usage trends over time to identify patterns and outliers.\n- Implement memory profiling tools to analyze memory consumption at a granular level.\n- Optimize memory allocation strategies for memory-intensive events to prevent resource contention and improve system performance.\n\nFeel free to reach out if you need further assistance or more detailed analysis!'
    response = response.replace('\n', '\\n')
    print(response)
    return response
    '''



if __name__ == "__main__":

    app.run(host="localhost", port=5000, debug=True)





