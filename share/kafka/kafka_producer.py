from confluent_kafka import Producer 
import json 

class MenagesProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.conf = {"bootstrap.servers": bootstrap_servers}
        self.producer = Producer(self.conf)  # type: ignore
        self.topic = topic  
    
    async def send_messege(self, messege: dict): 
        """send a messege to kafka """
        self.producer.produce(
            topic=self.topic,
            value=json.dumps(messege).encode('utf-8')
        )
        self.producer.poll(0) 
    
    def close(self):
        """close the connection to kafka"""
        self.producer.flush(10)
        