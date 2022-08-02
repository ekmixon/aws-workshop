import psycopg2
import json
import boto3

client = boto3.client('ssm')

db_host = client.get_parameter(
    Name='/prod/api/DATABASE_HOST')['Parameter']['Value']
db_name = client.get_parameter(
    Name='/prod/api/DATABASE_NAME')['Parameter']['Value']
db_user = client.get_parameter(
    Name='/prod/api/DATABASE_USER')['Parameter']['Value']
db_pass = client.get_parameter(
    Name='/prod/api/DATABASE_PASSWORD', WithDecryption=True)['Parameter']['Value']

db_port = 5432


def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            f"dbname={db_name} user={db_user} host={db_host} password={db_pass}"
        )

    except:
        print("Cannot connect.")
    return conn


def fetch(conn, query):
    print(f"Now executing: {query}")
    cursor = conn.cursor()
    cursor.execute(query)
    raw = cursor.fetchall()
    return list(raw)


def lambda_handler(event, context):

    print(event)

    query = event['query'] if 'query' in event.keys() else ''
    query_cmd = "select * from articles_article where title like '%"+query+"%'"

    print(query_cmd)

    conn = create_conn()

    result = fetch(conn, query_cmd)
    conn.close()

    return {
        'statusCode': 200,
        'body': str(result)
    }
