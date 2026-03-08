import speech_recognition as sr
r = sr.Recognizer()
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import gridfs
import tempfile
import os

from share.core.config import settings
from share.log.logs import Logger
logger = Logger.get_logger()


class PodcastTranscriber:

    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGO_DB]
        self.fs = gridfs.GridFS(self.db)
        self.es = Elasticsearch(settings.ELASTIC_URL)
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, audio_bytes):
        with tempfile.NamedTemporaryFile(suffix=".wav",delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        try:
            with sr.AudioFile(temp_path) as source:
                audio = self.recognizer.record(source)

            return self.recognizer.recognize_google(audio)  # type: ignore

        except sr.UnknownValueError:
            logger.warning("could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Error connecting to Google API: {e}")
            return ""
        except Exception as e:
            logger.error(f"STT error: {e}")
            return ""
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

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
        logger.info(f"the podcasts:{file_id} and the info:\n{transcript}")
        self.update_elasticsearch(file_id, transcript)

        logger.info(f"finished {file_id}")

    def process_all_podcasts(self):
        for file_doc in self.db.fs.files.find():

            try:
                self.process_file(file_doc)

            except Exception as e:
                logger.error(f"error processing {file_doc['_id']} : {e}")