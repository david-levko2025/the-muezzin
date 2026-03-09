import speech_recognition as sr

from share.log.logs import Logger 

logger = Logger.get_logger()
class Singleton:
    _instance = None 

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.r = sr.Recognizer()  # type: ignore
        return cls._instance 
class SpeechManager(Singleton):
    def recognition_from_file(self, path):
        try:
            with sr.AudioFile(path) as source:
                audio = self.r.record(source)     # type: ignore
            logger.info(f"convert the audio to text ")
            audio = self.r.recognize_google(audio)     # type: ignore
            logger.info(f'text: {audio}')
            return audio

        except Exception as e:
            logger.error(f"Exception {str(e)}")
            return f"Exception: {str(e)}"