# Dialogflow data cleasing sample

import pandas as pd

# Load the Dialogflow log data into a Pandas DataFrame
df = pd.read_csv('dialogflow_logs.csv')

# Remove irrelevant data, such as metadata or debugging information
df = df.drop(['metadata', 'debug_info'], axis=1)

# Standardize data by converting all text to lowercase and removing punctuation
df['user_query'] = df['user_query'].str.lower().str.replace('[^\w\s]','')
df['chatbot_response'] = df['chatbot_response'].str.lower().str.replace('[^\w\s]','')

# Handle missing data by filling in missing values with the mode of the data
df['intent_name'] = df['intent_name'].fillna(df['intent_name'].mode()[0])

# Remove duplicates by dropping any rows that have the same combination of user ID and timestamp
df = df.drop_duplicates(subset=['user_id', 'timestamp'])

# Handle outliers by identifying any queries or inputs that are significantly different from the rest of the data
q1 = df['user_query'].quantile(0.25)
q3 = df['user_query'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
df = df[(df['user_query'] >= lower_bound) & (df['user_query'] <= upper_bound)]
