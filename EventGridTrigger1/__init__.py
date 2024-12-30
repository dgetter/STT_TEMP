import azure.functions as func
import logging
import json
import http.client
from urllib.parse import urlparse

def main(event: func.EventGridEvent):
    logging.info("Event Grid trigger function processed an event.")

    try:
        # Parse the event data
        event_data = event.get_json()
        logging.info(f"Event Data: {event_data}")

        # Extract blob details from the event
        blob_url = event_data['data']['url']
        logging.warning(f"blob_url: {blob_url}")
        blob_name = blob_url.split("/")[-1]
        logging.info(f"Blob URL: {blob_url}, Blob Name: {blob_name}")

        # Process only .wav files
        if blob_name.lower().endswith('.wav'):
            # The URL of the endpoint where you want to send the POST request
            post_url = 'https://mokdimai-service.azurewebsites.net/meitav'
            data = {
                "filename": blob_name
            }

            # Parse the URL into components
            parsed_url = urlparse(post_url)
            host = parsed_url.netloc
            path = parsed_url.path

            # Convert data to JSON
            json_data = json.dumps(data)
            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(json_data))
            }

            # Sending the POST request using http.client
            try:
                conn = http.client.HTTPSConnection(host)
                conn.request("POST", path, body=json_data, headers=headers)
                response = conn.getresponse()
                response_data = response.read().decode("utf-8")
                logging.info(f'POST request sent. Status code: {response.status}, Response: {response_data}')
                conn.close()
            except Exception as e:
                logging.error(f'Error sending POST request: {e}')
        else:
            logging.info("Uploaded file is not a .wav file, skipping...")

    except KeyError as e:
        logging.error(f"Missing key in event data: {e}")
    except Exception as e:
        logging.error(f"Error processing the event: {e}")
