from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    BOOTSTRAP_SERVERS: str = "localhost:9092"
    METADATA_TOPIC: str = "metadata_topic"
    KAFKA_GROUP_ID: str = "metadata_group"
    PROCESSING_GROUP_ID: str = "analysis_"
    MONGO_AUDIO_TOPIC: str = "mongo_audio"
    MONGO_AUDIO_GROUP_ID: str = "mongo_audio"
    DATA: str = "/data/podcasts"
    MONGODB_URL: str = "mongodb://localhost:27017/" 
    MONGO_DB: str = 'the_muezzin'
    MONGO_COLLECTION: str = "podcasts" 
    ELASTIC_URL: str = "http://localhost:9200" 
    ELASTIC_INDEX_NAME: str = 'podcasts' 
    ELASTIC_INDEX_LOGS: str = 'index_log' 
    LOGER_NAME: str = "app.log"
    TRANSCRIPTION_TOPIC: str = "transcription_topic"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings = Settings()
    