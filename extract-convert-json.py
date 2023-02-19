# Sample for extracting from Dialogflow and from JSON to BigQuery tabular
import json

def dialogflow_to_bigquery(dialogflow_request):
    # Extract relevant data from Dialogflow request
    user_id = dialogflow_request['session'] 
    intent_name = dialogflow_request['queryResult']['intent']['displayName']
    query_text = dialogflow_request['queryResult']['queryText']
    
    # Create a JSON object for BigQuery
    bigquery_request = {
        'user_id': user_id,
        'intent_name': intent_name,
        'query_text': query_text
    }
    
    # Convert the JSON object to a string
    bigquery_request_json = json.dumps(bigquery_request)
    
    return bigquery_request_json