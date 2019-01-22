import flask
from google.cloud import bigquery


def validate_bigquery():
    client = bigquery.Client()
    query_job = client.query("""
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
   LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    jsonString = "["
    for row in results:
        jsonString += "{"
        for key in row.keys():
           #if isnumeric(row[key]):
           jsonString += "'" + key + "':'" + str(row[key]) + "'";  
           #else:
           #   jsonString += "'" + key + "':'"# + row[key] + "'";  
           print(key, row[key])
        jsonString += "},"
         
        print("{} : {} views".format(row.url, row.view_count))
    jsonString += "]"

    return jsonString

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return validate_bigquery()

app.run()
