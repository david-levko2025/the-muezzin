from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from share.log.logs import Logger 

logger = Logger.get_logger()
class MongoLoader:
    def __init__(self, db, file_path, filename):
        self.db = db  
        self.file_path = file_path
        self.filename = filename 

    async def send_file(self, file_id):
        bucket = AsyncIOMotorGridFSBucket(self.db)
        try:
            with open(self.file_path, 'rb') as file_data:
                await bucket.upload_from_stream_with_id(
                    file_id=file_id,
                    filename=self.filename, 
                    source=file_data
                )
            logger.info(f"file uploaded with fild_id {file_id}")
        except Exception as e:
            logger.error(e)

            