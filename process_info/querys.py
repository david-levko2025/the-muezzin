from elasticsearch import Elasticsearch
from share.core.config import settings

class ElasticQueries:
    def __init__(self):
        self.es = Elasticsearch(settings.ELASTIC_URL)
        self.index = settings.ELASTIC_INDEX_NAME

    def get_threat_distribution(self):
        query = {
            "size": 0,
            "aggs": {
                "levels": {
                    "terms": {"field": "level_threat_bds.keyword"}
                }
            }
        }
        response = self.es.search(index=self.index, body=query)
        buckets = response['aggregations']['levels']['buckets']
        return {b['key']: b['doc_count'] for b in buckets}

    def get_top_danger_podcasts(self, limit=5):
        query = {
            "size": limit,
            "sort": [{"precent_bds": "desc"}],
            "_source": ["filename", "precent_bds", "level_threat_bds"]
        }
        response = self.es.search(index=self.index, body=query)
        return [hit['_source'] for hit in response['hits']['hits']]

    def search_by_keyword(self, keyword):
        query = {
            "query": {
                "match": {"text": keyword}
            }
        }
        response = self.es.search(index=self.index, body=query)
        return [hit['_source']['filename'] for hit in response['hits']['hits']]