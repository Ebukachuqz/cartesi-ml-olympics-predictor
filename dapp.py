from os import environ
import model
import json
import traceback
import logging
import requests

# Cartesi API Definitions
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Util functions
def hex2str(hex):
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    return "0x" + str.encode("utf-8").hex()

# Function to make predictions
def predict_country(country_code):
    input_data = {"team": country_code}
    formatted_input = format(input_data)
    prediction = model.score(formatted_input)
    return prediction

# Function to format input data
def format(input):
    formatted_input = {}
    for key in input.keys():
        if key in model.columns:
            formatted_input[key] = input[key]
        else:
            ohe_key = key + "_" + str(input[key])
            ohe_key_unknown = key + "_nan"
            if ohe_key in model.columns:
                formatted_input[ohe_key] = 1
            else:
                formatted_input[ohe_key_unknown] = 1
    output = []
    for column in model.columns:
        if column in formatted_input:
            output.append(formatted_input[column])
        else:
            output.append(0)
    return output

# Initialize the array to store user inputs and predictions
user_predictions = []

# Cartesi API
def handle_advance(data):
    status = "accept"
    try:
        input_data = hex2str(data["payload"])
        input_json = json.loads(input_data)
        country_code = input_json["country_code"]
        sender = input_json["sender"]
        
        prediction = predict_country(country_code)
        
        # Store sender, country code input, and prediction
        user_predictions.append({
            "sender": sender,
            "country_code": country_code,
            "prediction": prediction
        })
        
        output = str2hex(str(prediction))
        response = requests.post(rollup_server + "/notice", json={"payload": output})
    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
    return status

def handle_inspect(data):
    response_data = {
        "count": len(user_predictions),
        "predictions": user_predictions
    }
    response_payload = str2hex(json.dumps(response_data))
    response = requests.post(rollup_server + "/report", json={"payload": response_payload})
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    response = requests.post(rollup_server + "/finish", json=finish)
    if response.status_code == 202:
        pass
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
