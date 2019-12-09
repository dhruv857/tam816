from google.cloud import bigquery
from elasticsearch import Elasticsearch

def query_github():
    client = bigquery.Client()
    query_job = client.query("""
        select distinct(t2.repo_name), t1.committer.time_sec, t2.language_name, t3.license, EXTRACT(YEAR FROM TIMESTAMP_SECONDS(t1.committer.time_sec)) AS year, EXTRACT(MONTH FROM TIMESTAMP_SECONDS(t1.committer.time_sec)) AS month from `dhruv-816.816.commits` t1,UNNEST(repo_name) AS repo_name
        join `dhruv-816.816.languages_repos_11` t2 USING (repo_name) join `dhruv-816.816.licenses` t3 USING (repo_name)
        """)

    results = query_job.result()  # Waits for job to complete.
    es=Elasticsearch([{'host':'localhost','port':9200}])
    for row in results:
        commit = {
                "repo_name": row[0],
                "timestamp": row[1]*1000,
                "language": row[2],
                "license": row[3],
                "year": row[4],
                "month": row[5]
                }
        res =es.index(index='816-github-1',body=commit)
        print(res)


if __name__ == '__main__':
    query_github()