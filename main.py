from os import environ
import json
from model import score
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

# Load the team mapping from the JSON file
with open("team_mapping.json", "r") as file:
    team_mapping = json.load(file)

def format_input(input_json):
    # Map the 'team' (country code) to its corresponding numeric code
    formatted_input = [
        team_mapping.get(input_json["team"], -1),  # Convert team code, use -1 for unknown teams
        input_json["athletes"],                   # Number of athletes
        input_json["prev_medals"]                 # Previous medals won
    ]
    return formatted_input


# Initialize the array to store user inputs and predictions
user_predictions = []

# Cartesi API
def handle_advance(data):
    status = "accept"
    try:
        input_data = hex2str(data["payload"])
        sender = input_json["metadata"]["msg_sender"]
        input_json = json.loads(input_data)

        # format input data
        formatted_data = format_input(input_json)

        # Use the formatted data to make a prediction
        prediction = score(formatted_data)
        
        # Store sender, input, and prediction
        user_predictions.append({
            "sender": sender,
            "input": input_json,
            "prediction": prediction
        })
        
        output = str2hex(str(prediction))
        logger.info(f"Adding notice with payload: {predicted}")
        response = requests.post(rollup_server + "/notice", json={"payload": output})
        logger.info(f"Received notice status {response.status_code} body {response.content}")
    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")
    
    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")

    response_data = {
        "count": len(user_predictions),
        "predictions": user_predictions
    }
    response_payload = str2hex(json.dumps(response_data))
    response = requests.post(rollup_server + "/report", json={"payload": response_payload})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
