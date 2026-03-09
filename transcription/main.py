import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient 

from .engine import SpeechManager
from .grid0 import MongoDBHandler
from share.kafka.kafka_consumer import MenagesConsumer
from share.kafka.kafka_producer import MenagesProducer
from share.core.config import settings 
from share.log.logs import Logger 


logger = Logger.get_logger()

class Manager:
    def __init__(self):
        self.mongo_db_name = settings.MONGO_DB
        self.mongo_url = settings.MONGODB_URL 
        self.mongo_client: AsyncIOMotorClient = None  # type: ignore
        self.mongo_do: MongoDBHandler = None    # type: ignore
        
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.mongo_audio_topic = [settings.MONGO_AUDIO_TOPIC]
        self.group_id = settings.MONGO_AUDIO_GROUP_ID 
        self.consumer = None 
        self.producer : MenagesProducer | None = None

        self.convert_to_text = None
        self.speech_manager: SpeechManager = None   # type: ignore


    async def setup(self):
        self.consumer = MenagesConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.mongo_audio_topic
        )
        self.mongo_client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.mongo_client[self.mongo_db_name]
        self.collection = self.db.get_collection(settings.MONGO_COLLECTION)
        self.speech_manager = SpeechManager()
        self.mongo_db = MongoDBHandler(self.db)
        self.producer = MenagesProducer(
            bootstrap_servers=self.bootstrap_servers, 
            topic=settings.TRANSCRIPTION_TOPIC
            )
        self.speech_manager = SpeechManager()
        self.mongo_db = MongoDBHandler(self.db)

    async def convert_file_to_text(self, path, speech_manager: SpeechManager):
        try:
            return speech_manager.recognition_from_file(path)
        except Exception as e:
            logger.error(e)

    async def manage_file(self, file_dict: dict):       
        try:
            filename = file_dict.get('filename')
            local_path = f"temp/{filename}" 
            await self.mongo_db.get_file(local_path, filename) 
            
            text_result = await self.convert_file_to_text(local_path, self.speech_manager)
            enriched_data = file_dict.copy()
            enriched_data['text'] = text_result
            if self.producer:
                await self.producer.send_messege(enriched_data)
                logger.info(f"successfuly send transcription for {filename}")
            else:
                logger.error("producer isn't initialized")
            os.remove(local_path)

        except Exception as e:
            logger.error(f"error: {e}")

    async def run(self):
        await self.setup()
        logger.info("the program set up seccessfully")

        await self.consumer.consumer_loop(self.manage_file)  # type: ignore
        
    async def main(self):
        await self.run() 

if __name__ == "__main__":
    manager = Manager()
    asyncio.run(manager.main())