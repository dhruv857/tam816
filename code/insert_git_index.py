from google.cloud import bigquery
from elasticsearch import Elasticsearch

def query_github():
    client = bigquery.Client()
    query_job = client.query("""
        select repo_name, committer.time_sec, subject, message, language_name from `dhruv-816.816.commits`,UNNEST(repo_name) AS repo_name
        join `dhruv-816.816.language_repos` USING (repo_name)
        """)

    results = query_job.result()  # Waits for job to complete.
    es=Elasticsearch([{'host':'localhost','port':9200}])
    for row in results:
        commit = {
                "repo_name": row[0],
                "language": row[4],
                "subject": row[2],
                "message": row[3],
                "timestamp": row[1]
                }
        res =es.index(index='816-github',body=commit)
        print(res)


if __name__ == '__main__':
    query_stackoverflow()
