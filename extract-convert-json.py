# Sample for extracting from Dialogflow and from JSON to BigQuery tabular
from google.cloud import bigquery
import json

def dialogflow_to_bigquery(dialogflow_request, project_id, dataset_id, table_name):
    # Extract relevant data from Dialogflow request
    user_id = dialogflow_request['session'] 
    intent_name = dialogflow_request['queryResult']['intent']['displayName']
    query_text = dialogflow_request['queryResult']['queryText']
    
    # Define the schema for the BigQuery table
    schema = [
        bigquery.SchemaField('user_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('intent_name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('query_text', 'STRING', mode='REQUIRED')
    ]
    
    # Create a BigQuery client and table
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_name)
    table = bigquery.Table(table_ref, schema=schema)
    
    # Insert data into the table
    rows_to_insert = [(user_id, intent_name, query_text)]
    errors = client.insert_rows(table, rows_to_insert)
    
    if errors == []:
        print(f'Successfully inserted row into {table_name}.')
    else:
        print(f'Error inserting row into {table_name}: {errors}')
