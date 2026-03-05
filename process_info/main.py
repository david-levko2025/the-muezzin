import asyncio

from share.kafka.kafka_consumer import MenagesConsumer
from share.core.config import settings 
from .elastic_search import ElasticSearch, Elasticsearch
from share.log.logs import Logger

logger = Logger.get_logger()

class Manager:
    def __init__(self):
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.topics = [settings.METADATA_TOPIC]
        self.group_id = settings.PROCESSING_GROUP_ID 

        self.index_name = settings.ELASTIC_INDEX_NAME 
        self.elastic_url = settings.ELASTIC_URL

        self.consumer: MenagesConsumer = None   # type: ignore
        self.elastic_con: ElasticSearch = None  # type: ignore 
       

    async def setup(self):
        self.consumer = MenagesConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.topics
        )
        self.elastic_con = ElasticSearch(
            index_name=self.index_name, 
            hosts=settings.ELASTIC_URL
        )
        
    
    async def manage_index(self, metadata_dict):
        self.elastic_con.create_index(metadata_dict)

    async def run(self):
        await self.setup()
        logger.info("the program start")

        await self.consumer.consumer_loop(self.manage_index)
    
    async def main(self):
        await self.run()

if __name__ == "__main__":
    manager = Manager()
    asyncio.run(manager.main())

        