import time
import uuid
from typing import Dict, List, Optional, Union

import redis

from app.core.config import settings
from app.utils.log_utils import logger


class _RedisClient:
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


redis_client = _RedisClient()


class RedisLock:
    def __init__(self, lock_key: str, expire_nx: int = 10):
        self.client = redis_client.client
        self.lock_key = lock_key
        self.expire_nx = expire_nx
        self.lock_value = str(uuid.uuid4())  # 用唯一值标识这个客户端持有的锁
    
    def acquire(self, timeout: int = None) -> bool:
        start_time = time.time()
        while True:
            # 尝试获取锁
            if self.client.set(self.lock_key, self.lock_value, nx=True, ex=self.expire_nx):
                return True

            # 如果 timeout=None，就立即返回 False（非阻塞模式）
            if timeout is None:
                return False

            # 如果超时了，返回 False
            if (time.time() - start_time) >= timeout:
                return False

            # 否则继续循环尝试
            time.sleep(0.05)  # 避免忙等

    def release(self):
        # 释放锁时必须保证是自己的锁
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        release = self.client.register_script(lua_script)
        return release(keys=[self.lock_key], args=[self.lock_value])


# 示例用法
if __name__ == "__main__":
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
