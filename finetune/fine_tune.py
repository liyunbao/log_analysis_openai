import json
import openai
from collections import defaultdict

api_key = open('API_KEY').read()
openai.api_key = api_key

def load_data(data_path):
    # Load the dataset
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]

    # Initial dataset stats
    print("Num examples:", len(dataset))
    print("First example:")
    for message in dataset[0]["messages"]:
        print(message)
    return dataset

def validate_format(dataset):
    # Format error checks
    format_errors = defaultdict(int)

    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue

        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue

        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1

            if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
                format_errors["message_unrecognized_key"] += 1

            if message.get("role", None) not in ("system", "user", "assistant", "function"):
                format_errors["unrecognized_role"] += 1

            content = message.get("content", None)
            function_call = message.get("function_call", None)

            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1

        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    if format_errors:
        print("Found errors:")
        for k, v in format_errors.items():
            print(f"{k}: {v}")
        return False
    else:
        print("No errors found")
        return True

def fine_tune(client, file_id):
    #create model
    response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )
    print(f'{response}')
    return response.id
def upload_file(client, data_path):
    # Upload the file
    upload_response = client.files.create(
        file=open(data_path, "rb"),
        purpose="fine-tune"
    )
    file_id = upload_response.id
    print(f"File uploaded successfully. ID: {file_id}")
    return file_id

if __name__ == '__main__':

    data_path = "training_data.jsonl"
    # load training data
    dataset = load_data(data_path)
    # check data formatting
    if not validate_format(dataset):
        raise SystemExit('Training data is not valid!')

    # Upload data to openAI
    # OpenAI will return file id which we can use to train the model
    client = openai.OpenAI()
    file_id = upload_file(client, data_path)

    # create training job
    job_id = fine_tune(client, file_id)

    # It takes sometime to finish training, depends on the size of the training data or the job queue
    # Use this command to check the status of the job
    job_status = client.fine_tuning.jobs.retrieve(job_id)
    print(job_status)



