from stt.stt_engine import PodcastTranscriber
from share.log.logs import Logger

logger = Logger.get_logger()

def main():
    logger.info("starting listening to the podcasts ")

    transcriber = PodcastTranscriber()
    
    try:
        transcriber.process_all_podcasts()
        logger.info("all the podcasts completed to readable")
    except KeyboardInterrupt:
        logger.warning("process stopped by the user")
    except Exception as e:
        logger.error(f"system fail: {e}")

if __name__ == "__main__":
    main()