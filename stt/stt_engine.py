import speech_recognition as sr

from share.core.config import settings
from share.log.logs import Logger

logger = Logger.get_logger()
r = sr.Recognizer()

import gridfs
import tempfile


from pymongo import MongoClient
from elasticsearch import Elasticsearch




class PodcastTranscriber:

    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGO_DB]
        self.fs = gridfs.GridFS(self.db)
        self.es = Elasticsearch(settings.ELASTIC_URL)
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, audio_bytes):
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            f.write(audio_bytes)
            f.flush()

            with sr.AudioFile(f.name) as source:
                audio = self.recognizer.record(source)

        try:
            return self.recognizer.recognize_google(audio)  # type: ignore

        except sr.UnknownValueError:
            logger.warning("could not understand audio")
            return ""

        except Exception as e:
            logger.error(f"STT error: {e}")
            return ""

    def update_elasticsearch(self, file_id, transcript):

        self.es.update(
            index=settings.ELASTIC_INDEX_NAME,
            id=str(file_id),
            doc={
                "transcript": transcript
            }
        )

    def process_file(self, file_doc):

        file_id = file_doc["_id"]

        logger.info(f"processing file {file_id}")

        grid_out = self.fs.get(file_id)
        audio_bytes = grid_out.read()

        transcript = self.transcribe_audio(audio_bytes)

        self.update_elasticsearch(file_id, transcript)

        logger.info(f"finished {file_id}")

    def process_all_podcasts(self):

        for file_doc in self.db.fs.files.find():

            try:
                self.process_file(file_doc)

            except Exception as e:
                logger.error(f"error processing {file_doc['_id']} : {e}")
