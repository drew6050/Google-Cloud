# Sample code that pulls data from Dialogflow into BigQuery and trains a machine learning
from google.cloud import bigquery
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Initialize the BigQuery client
client = bigquery.Client()

# Set the query to retrieve intent and user query data from Dialogflow logs
query = """
    SELECT
        intents.name AS intent_name,
        queries.query_text AS query_text
    FROM
        `your-project-id.your-dialogflow-agent-name.your-dialogflow-log-table-name`,
        UNNEST(queryResult.diagnosticInfo.queryPlan.nodes) AS nodes
    WHERE
        timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
"""

# Execute the query and retrieve the results as a pandas dataframe
df = client.query(query).to_dataframe()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['query_text'], df['intent_name'], test_size=0.2, random_state=42)

# Define the pipeline for the machine learning model
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('clf', RandomForestClassifier(n_estimators=100))
])

# Fit the pipeline on the training data
pipeline.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = pipeline.predict(X_test)

# Print the classification report to evaluate the performance of the model
print(classification_report(y_test, y_pred))

# Save the trained model to BigQuery
model = pipeline.steps[1][1]
model_name = 'your-model-name'
model_version = 'v1'
model_path = f'{model_name}/{model_version}'
client = bigquery.Client()
job_config = bigquery.QueryJobConfig()
job_config.destination = f'{client.project}.{model_path}'
job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
job_config.schema = [
    bigquery.SchemaField('query_text', 'STRING'),
    bigquery.SchemaField('predicted_intent', 'STRING')
]
query = f"""
    SELECT
        query_text,
        '{model.classes_[0]}' AS predicted_intent
    FROM
        UNNEST(@query_texts) AS query_text
"""
query_params = [
    bigquery.ArrayQueryParameter('query_texts', 'STRING', list(X_test))
]
job = client.query(query, job_config=job_config, query_params=query_params)
job.result()
