import json

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer, TopicPartition


class KafkaUtils:
    def __init__(self, group_id: str = None, bootstrap_server: str = 'localhost:9092'):
        self.group_id: str = group_id
        self.bootstrap_server: str = bootstrap_server
        self.producer: KafkaProducer | None = None
        self.consumer: KafkaConsumer | None = None
        self.admin_client: KafkaAdminClient | None = None

    def _get_producer(self):
        self.producer = KafkaProducer(bootstrap_servers=[self.bootstrap_server])
        return self.producer

    def send_message(self, topic: str, message: bytes):
        if self.producer is None:
            self._get_producer()
        self.producer.send(topic, value=message, partition=0)
        self.producer.flush()

    def _get_consumer(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=[self.bootstrap_server],
            group_id=self.group_id,
            auto_offset_reset='earliest',  # 设置为从最早的消息开始消费
            consumer_timeout_ms=6000,  # 设置超时，避免无限等待
            enable_auto_commit=False,  # 禁用自动提交
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # 反序列化 JSON 字符串
        )
        return self.consumer

    def _get_kafka_admin_client(self):
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_server)

    def get_message(self, topic: str, msg_count: int = 1):
        if self.consumer is None:
            self._get_consumer()

        self.consumer.subscribe([topic])  # 确保订阅了主题
        count = 0
        for msg in self.consumer:
            print(f"获取的消息是：{msg.value}, {msg.offset=}")
            self.consumer.commit()
            count += 1
            if count >= msg_count:
                break

    def get_topics(self):
        """获取kafka里面所有的topic"""
        if self.consumer is None:
            self._get_consumer()
        return self.consumer.topics()

    def get_groups(self):
        if self.admin_client is None:
            self._get_kafka_admin_client()
        groups = self.admin_client.list_consumer_groups()
        return [group[0] for group in groups]

    def set_group_id(self, group_id: str):
        self.group_id = group_id

    def get_partitions(self, topic: str) -> list[int]:
        """获取topic下所有的分区"""
        if self.consumer is None:
            self._get_consumer()
        return list(self.consumer.partitions_for_topic(topic))

    def get_commit_and_end_seek(self, topic: str, partitions: list[int]):
        if not partitions:
            raise RuntimeError(f"传入错误的partitions:{partitions}")
        result = {}
        if self.consumer is None:
            self._get_consumer()
        tp_list = [TopicPartition(topic, p) for p in partitions]
        self.consumer.assign(tp_list)

        # 遍历每个分区并计算未消费的消息数量
        for tp in tp_list:
            # 获取最新的位点（log end offset）
            end_offset = self.consumer.end_offsets([tp])[tp]
            # 获取当前消费者组的已提交位点（committed offset）
            committed_offset = self.consumer.committed(tp) or 0  # 如果没有已提交的位点则为 0
            # 计算未消费的消息数量
            unconsumed_messages = end_offset - committed_offset
            result[tp.partition] = {
                'end_offset': end_offset,
                'committed_offset': committed_offset,
                'unconsumed_messages': unconsumed_messages
            }
        return result

    def set_commit_seek(self, topic: str, partition: int, offset: int):
        if self.consumer is None:
            self._get_consumer()
        tp = TopicPartition(topic, partition)
        self.consumer.assign([tp])

        # 手动设置偏移量
        self.consumer.seek(tp, offset)
        # 手动提交新的偏移量
        self.consumer.commit()  # 提交当前设置的偏移量，使其在消费者组内生效

    def close_consumer(self):
        if self.consumer is None:
            return
        self.consumer.close()
        self.consumer = None

    def close_producer(self):
        if self.producer is None:
            return
        self.producer.close()
        self.producer = None
