import asyncio
from pymongo import MongoClient

from share.kafka.kafka_consumer import MenagesConsumer 
from share.core.config import settings 
from .gridfs import MongoLoader 
from share.log.logs import Logger

logger = Logger.get_logger()

class Manager:
    def __init__(self):
        self.mongo_url = settings.MONGODB_URL 
        self.mongo_db_name = settings.MONGO_DB 
        
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.metadata_topic = [settings.METADATA_TOPIC]
        self.group_id = settings.KAFKA_GROUP_ID 

        self.mongo_loader = None
        self.consumer = None 


    async def setup(self):
        self.consumer = MenagesConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.metadata_topic
        )
        self.mongo_client = MongoClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_name]

    async def manage_file(self, file_dict: dict):
        try:
            self.mongo_loader = MongoLoader(
                db=self.db, 
                file_path=file_dict.get('path', ''), 
                filename=file_dict.get('filename', '')
                )
            id = file_dict.get('id', '')

            self.mongo_loader.send_file(id)

        except Exception as e:
            logger.error(e)

    async def run(self):
        await self.setup()
        logger.info("the program set up seccessfully")

        await self.consumer.consumer_loop(self.manage_file)  # type: ignore
        
    async def main(self):
        await self.run() 

if __name__ == "__main__":
    manager = Manager()
    asyncio.run(manager.main())