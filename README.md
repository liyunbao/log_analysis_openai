
# Analyze Logs with Fine-tuned GPT Model

This project is a log analyzer built on Flask, powered by the fined-tune OpenAI GPT model.

You can config your API key, and upload your logs to the server, and then server will use the OpenAI to analyze the logs and provide suggestions about the root cause of any identified issues.

## How it works

![alt text](https://github.com/liyunbao/log_analysis_openai/blob/main/static/img/Log_Analysis_Finetune.png)

### Prerequisites

- Python 3.6 or higher
- OpenAI API key

### Installation

1. Clone the repository to your local machine:
       
        git@github.com:liyunbao/log_analysis_openai.git
        cd log_analysis_openai

2. Install the required Python packages using pip:

        pip install -r requirements.txt

      Note: If you have both Python 2 and Python 3 installed on your machine, you may need to use `pip3` instead of `pip`.

      The `requirements.txt` file includes the following packages:

      - flask
      - openai

      Note: The code works with OpenAI SDK Version: 1.72.0. If the request to OpenAI is failed it may be caused by the SDK version is too old, use `pip show openai` to check the version.
   
3. Fine Tune your model
      Follow the steps in fine_tune.py to training the GPT model with your training data

4. Run the application:
      After your model is finished training, OpenAI will give you a model id. Use this id in start.py and run

        python start.py

      Note: You may need to use `python3` instead of `python`, depending on your setup.

5. Open this link in browser http://localhost:5000/

      Upload your log file, you could select the pre-defined options, or input the questions and click Send button. Your question and the response from GPT will show up in the message form.
![alt text](https://github.com/liyunbao/log_analysis_openai/blob/main/static/img/tool_ui.png)


### Further Development

This is a basic setup for a log analysis tool. We can build more sophisticated system by fine-tuning the OpenAI model parameters, or handling more complex log analysis tasks.

## License
log_analysis_openai is available under the MIT license. For more details see LICENSE.


