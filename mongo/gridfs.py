from gridfs import GridFSBucket

from share.log.logs import Logger
logger = Logger.get_logger()

class MongoLoader:
    def __init__(self, db, file_path, filename):
        self.db = db  
        self.file_path = file_path
        self.filename = filename 

    def send_file(self, file_id):
        bucket = GridFSBucket(self.db)
        try:
            with open(self.file_path, 'rb') as file_data:
                bucket.upload_from_stream_with_id(
                    file_id=file_id,
                    filename=self.filename, 
                    source=file_data
                )
            logger.info(f"file uploaded with fild_id {file_id}")
        except Exception as e:
            logger.error(e)