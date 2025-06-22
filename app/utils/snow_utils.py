import time

# 起始时间戳，可自定义，这里使用 2025-01-01 00:00:00 的时间戳
START_TIMESTAMP = 1735660800000

# 数据中心 ID 所占位数
DATACENTER_ID_BITS = 5
# 机器 ID 所占位数
WORKER_ID_BITS = 5
# 序列号所占位数
SEQUENCE_BITS = 12

# 数据中心 ID 最大值
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)  # 2^5 - 1 = 31
# 机器 ID 最大值
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2^5 - 1 = 31
# 序列号最大值
MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)  # 2^12 - 1 = 4095

# 机器 ID 向左移位数
WORKER_ID_SHIFT = SEQUENCE_BITS
# 数据中心 ID 向左移位数
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
# 时间戳向左移位数
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS


class SnowflakeIDGenerator:
    def __init__(self, datacenter_id, worker_id):
        # 检查数据中心 ID 和机器 ID 是否合法
        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"Datacenter ID must be between 0 and {MAX_DATACENTER_ID}")
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"Worker ID must be between 0 and {MAX_WORKER_ID}")

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1

    @classmethod
    def _get_current_timestamp(cls):
        # 获取当前时间戳（毫秒级）
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp):
        # 等待下一毫秒
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp

    def generate_id(self):
        timestamp = self._get_current_timestamp()

        # 处理时钟回拨问题
        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id for {} milliseconds".format(
                self.last_timestamp - timestamp))

        if timestamp == self.last_timestamp:
            # 同一毫秒内，序列号递增
            self.sequence = (self.sequence + 1) & MAX_SEQUENCE
            if self.sequence == 0:
                # 序列号达到最大值，等待下一毫秒
                timestamp = self._wait_for_next_millis(self.last_timestamp)
        else:
            # 不同毫秒，序列号重置为 0
            self.sequence = 0

        self.last_timestamp = timestamp

        # 生成最终的 ID
        new_id = (
                ((timestamp - START_TIMESTAMP) << TIMESTAMP_LEFT_SHIFT)
                | (self.datacenter_id << DATACENTER_ID_SHIFT)
                | (self.worker_id << WORKER_ID_SHIFT)
                | self.sequence
        )

        return new_id


snowflake_generator = SnowflakeIDGenerator(1, 1)

if __name__ == "__main__":
    for _ in range(5):
        print(snowflake_generator.generate_id())
