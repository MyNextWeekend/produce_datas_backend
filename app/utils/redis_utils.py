from typing import Dict, List, Optional, Union

import redis

from app.core.config import settings
from app.utils.log_utils import Log

logger = Log().get_logger()


class RedisClient:
    def __init__(self):
        self.client = redis.from_url(settings.redis.uri)

    def set(self, key: str, value: Union[str, int, float], ex_seconds: Optional[int] = None) -> bool:
        """设置键值对，可选过期时间（秒）"""
        return self.client.set(key, value, ex=ex_seconds)

    def get(self, key: str) -> Optional[str]:
        """获取键的值"""
        return self.client.get(key)

    def delete(self, key: str) -> int:
        """删除一个或多个键"""
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.client.exists(key)

    def incr(self, key: str, amount: int = 1) -> int:
        """原子递增键的值"""
        return self.client.incr(key, amount)

    def decr(self, key: str, amount: int = 1) -> int:
        """原子递减键的值"""
        return self.client.decr(key, amount)

    def hset(self, name: str, key: str, value: Union[str, int, float]) -> int:
        """设置哈希表中的字段值"""
        return self.client.hset(name, key, value)

    def hget(self, name: str, key: str) -> Optional[str]:
        """获取哈希表中的字段值"""
        return self.client.hget(name, key)

    def hgetall(self, name: str) -> Dict[str, str]:
        """获取哈希表中的所有字段值"""
        return self.client.hgetall(name)

    def lpush(self, key: str, *values: str) -> int:
        """从左侧推入列表"""
        return self.client.lpush(key, *values)

    def rpush(self, key: str, *values: str) -> int:
        """从右侧推入列表"""
        return self.client.rpush(key, *values)

    def lpop(self, key: str) -> Optional[str]:
        """从左侧弹出一个元素"""
        return self.client.lpop(key)

    def rpop(self, key: str) -> Optional[str]:
        """从右侧弹出一个元素"""
        return self.client.rpop(key)

    def lrange(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        """获取列表的范围内元素"""
        return self.client.lrange(key, start, end)

    def close(self):
        """关闭 Redis 连接"""
        self.client.close()


# 示例用法
if __name__ == "__main__":
    redis_client = RedisClient(db=0)

    # 字符串操作
    redis_client.set("mykey", "value", ex_seconds=60)
    logger.info(f"获取redis中的数据:{redis_client.get('mykey')}")

    # 哈希表操作
    redis_client.hset("myhash", "field1", "value1")
    logger.info(f"获取redis中 哈希表 的数据:{redis_client.hget('myhash', 'field1')}")
    logger.info(f"获取redis中 哈希表 的所有的数据:{redis_client.hgetall('myhash')}")

    # 列表操作
    redis_client.lpush("mylist", "item1", "item2")
    logger.info(f"获取redis中 列表 的所有的数据:{redis_client.lrange('mylist')}")

    redis_client.close()
