from elasticsearch import Elasticsearch
from share.log.logs import Logger

logger = Logger.get_logger() 

class ElasticSearch:
    def __init__(self, index_name, hosts: str):
        self.index_name = index_name 
        self.elastic = Elasticsearch(hosts=[hosts], verify_certs=False)

    def create_index(self, metadata: dict):
        try:
            id = metadata.get('id')
            index = self.elastic.index(index=self.index_name, document=metadata, id=id) 
            logger.info(f"the index added successfully {str(index)}")
        except Exception as e:
            logger.error(f"id not exist {e}")