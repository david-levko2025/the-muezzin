import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from share.kafka.kafka_producer import MenagesProducer
from share.kafka.kafka_consumer import MenagesConsumer 
from share.core.config import settings 
from share.log.logs import Logger 
from .gridfs import MongoLoader 

logger = Logger.get_logger()
class Manager:
    def __init__(self):
        self.mongo_url = settings.MONGODB_URL 
        self.mongo_db_name = settings.MONGO_DB 
        
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.metadata_topic = [settings.METADATA_TOPIC]
        self.group_id = settings.KAFKA_GROUP_ID 

        # kafka producer
        self.mongo_audio_topic = settings.MONGO_AUDIO_TOPIC

        self.mongo_loader = None
        self.consumer = None 


    async def setup(self):
        """setup the consumer for gettings the messages""" 
        self.consumer = MenagesConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.metadata_topic
        )
        self.producer = MenagesProducer(self.bootstrap_servers, self.mongo_audio_topic)
        self.mongo_client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_name]

    async def manage_file(self, file_dict: dict):
        try:
            self.mongo_loader = MongoLoader(
                db=self.db, 
                file_path=file_dict.get('path'), 
                filename=file_dict.get('filename')
                )
            id = file_dict.get('id')

            await self.mongo_loader.send_file(id)
            await self.producer.send_messege(file_dict)

        except Exception as e:
            logger.error(e)

        finally:
            self.producer.close()


    async def run(self):
        await self.setup()
        logger.info("the program set up seccessfully")

        await self.consumer.consumer_loop(self.manage_file)  # type: ignore
        
    async def main(self):
        await self.run() 

if __name__ == "__main__":
    manager = Manager()
    asyncio.run(manager.main())