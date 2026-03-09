import asyncio
from share.kafka.kafka_consumer import MenagesConsumer
from share.core.config import settings 
from process_info.elastic_search import ElasticSearch
from share.log.logs import Logger
from process_info.analysis import BDSAnalyzer
from process_info.querys import ElasticQueries

logger = Logger.get_logger()

class Manager:
    def __init__(self):
        self.bootstrap_servers = settings.BOOTSTRAP_SERVERS
        self.topics = [settings.TRANSCRIPTION_TOPIC]
        self.group_id = settings.PROCESSING_GROUP_ID 

        self.index_name = settings.ELASTIC_INDEX_NAME 
        self.elastic_url = settings.ELASTIC_URL

        self.consumer: MenagesConsumer = None   # type: ignore
        self.elastic_con: ElasticSearch = None  # type: ignore 
        self.analyzer = BDSAnalyzer()
        self.queries = ElasticQueries()

    async def setup(self):
        self.consumer = MenagesConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.topics
        )
        self.elastic_con = ElasticSearch(
            index_name=self.index_name, 
            hosts=settings.ELASTIC_URL
        )

    async def show_stats_report(self):
        try:
            dist = self.queries.get_threat_distribution()
            top = self.queries.get_top_danger_podcasts(1)

            logger.info(f"total Documents: {sum(dist.values())}")
            logger.info(f"distribution: {dist}")
            if top:
                logger.info(f"most Hostile: {top[0]['filename']} ({top[0]['precent_bds']}%)")
        except Exception as e:
            logger.error(f"failed to generate stats report: {e}")

    async def manage_index(self, data_dict):
        transcript_text = data_dict.get('text', "")

        precent, is_bds, level = self.analyzer.analyze(transcript_text)
        
        data_dict['precent_bds'] = precent
        data_dict['bds_is'] = is_bds
        data_dict['level_threat_bds'] = level

        logger.info(f"REAL ANALYSIS: {level}({precent}%) for file {data_dict.get('name')}")

        self.elastic_con.create_index(data_dict)
        await self.show_stats_report()

    async def run(self):
        await self.setup()
        logger.info("the program start...")
        await self.show_stats_report()
        await asyncio.sleep(1)
        await self.consumer.consumer_loop(self.manage_index)

    async def main(self):
        await self.run()

if __name__ == "__main__":    
        manager = Manager()
        asyncio.run(manager.run())