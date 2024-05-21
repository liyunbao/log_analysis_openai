
# Analyze your logs with OpenAI

This project is a log analyzer built on Flask, powered by the OpenAI GPT-4 model to work.

It takes a user input, logs, and then uses the OpenAI model to analyze these logs and provide suggestions about the root cause of any identified issues.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

- Here is an architecture diagram of how this works.
TBD

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

3. Run the application:

        python start.py

      Again, you may need to use `python3` instead of `python`, depending on your setup.

### Usage

After starting the Flask app, you can use the following endpoints:

- `/` : Returns the 'index.html' page. This is where you should start, open this up in your browser. It should look like this below:

TBD


- `/config` (POST method): Configures the API key for OpenAI clients. The request should contain the following parameters in form data, you can use the front end application and the "Save Config" button to populate this.

    - 'openai_key' : Your OpenAI API key.
    - 'logs' : upload your logs.

- `/message` (POST method): Takes 'user_input' as a form data parameter, analyzes the log results using OpenAI's GPT-4 model, and returns the analysis.

### Troubleshooting

If the `/message` endpoint returns an error message saying "Configuration is missing. Please provide the OpenAI API key and Elasticsearch details.", make sure you have properly configured the Elasticsearch and OpenAI clients using the `/config` endpoint or populating the config and using the "Save Config" button on the front end as a first step.

### Further Development

This is a basic setup for a log analysis tool. Depending on your specific use case and needs, you may want to tune the OpenAI model parameters, or handle more complex log analysis tasks.

Please feel free to fork this project and modify it according to your needs.

## License
log_analysis_openai is available under the Apache 2.0 license. For more details see LICENSE.


