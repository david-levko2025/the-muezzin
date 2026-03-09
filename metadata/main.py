import os 
import asyncio
import uuid  

from share.core.config import settings
from share.kafka.kafka_producer import MenagesProducer  
from .file_handling import FileMetadata
from share.log.logs import Logger

logger =  Logger.get_logger()
class Manager:
    def __init__(self):
        self.folder = settings.DATA
        self.metadata_topic = settings.METADATA_TOPIC
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.producer: MenagesProducer = None  # type: ignore
        self.file_handling: FileMetadata = None  # type: ignore

    def setup(self):
        self.producer = MenagesProducer(self.bootstrap_servers, self.metadata_topic) 

    async def run(self):
        try:
            for i in os.listdir(self.folder):
                absulut_path = os.path.join(self.folder, i)

                self.handle_file = FileMetadata(absulut_path)
                file_metadata = self.handle_file.add_metadata()

                file_metadata["path"] = absulut_path 
                file_metadata['id'] = str(uuid.uuid5(uuid.NAMESPACE_DNS,i))
                file_metadata['filename'] = i

                await self.producer.send_messege(file_metadata)
                logger.info(f"the message send successfully,\n file's metadata: {file_metadata} \n topic: {self.metadata_topic}")

        except FileNotFoundError as f:
            logger.error(f"the file {f} not exist")
        finally:
            self.producer.close()
        
    async def main(self):
        self.setup()
        await self.run()

    
if __name__ == "__main__":
    manager = Manager()
    asyncio.run(manager.main())