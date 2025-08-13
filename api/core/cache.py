"""
JarvisFi - Redis Cache Management
High-performance caching for improved response times
"""

import redis.asyncio as redis
import json
import pickle
import hashlib
import logging
from typing import Any, Optional, Union, Dict, List
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Global Redis connection
redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    
    try:
        # Create Redis connection
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        # Test connection
        await redis_client.ping()
        logger.info("✅ Redis cache initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Redis initialization failed: {e}")
        # Continue without cache if Redis is not available
        redis_client = None


async def close_redis():
    """Close Redis connection"""
    global redis_client
    
    try:
        if redis_client:
            await redis_client.close()
            logger.info("✅ Redis connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing Redis: {e}")


def get_redis() -> Optional[redis.Redis]:
    """Get Redis client"""
    return redis_client


class CacheManager:
    """Advanced cache management with multiple strategies"""
    
    def __init__(self):
        self.client = redis_client
        self.default_ttl = settings.CACHE_TTL
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        if kwargs:
            key_data += f":{json.dumps(kwargs, sort_keys=True)}"
        
        # Hash long keys
        if len(key_data) > 250:
            key_data = f"{prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"
        
        return key_data
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        if not self.client:
            return default
        
        try:
            value = await self.client.get(key)
            if value is None:
                return default
            
            # Try to deserialize JSON first, then pickle
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                try:
                    return pickle.loads(value.encode('latin1'))
                except:
                    return value
                    
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return default
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.client:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            
            # Serialize value
            if isinstance(value, (dict, list, tuple)):
                serialized_value = json.dumps(value, default=str)
            elif isinstance(value, (str, int, float, bool)):
                serialized_value = json.dumps(value)
            else:
                serialized_value = pickle.dumps(value).decode('latin1')
            
            await self.client.setex(key, ttl, serialized_value)
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.client:
            return False
        
        try:
            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.client:
            return False
        
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration for key"""
        if not self.client:
            return False
        
        try:
            return await self.client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Cache expire error for key {key}: {e}")
            return False
    
    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values from cache"""
        if not self.client or not keys:
            return {}
        
        try:
            values = await self.client.mget(keys)
            result = {}
            
            for key, value in zip(keys, values):
                if value is not None:
                    try:
                        result[key] = json.loads(value)
                    except (json.JSONDecodeError, TypeError):
                        try:
                            result[key] = pickle.loads(value.encode('latin1'))
                        except:
                            result[key] = value
            
            return result
            
        except Exception as e:
            logger.error(f"Cache get_many error: {e}")
            return {}
    
    async def set_many(self, mapping: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set multiple values in cache"""
        if not self.client or not mapping:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            pipe = self.client.pipeline()
            
            for key, value in mapping.items():
                # Serialize value
                if isinstance(value, (dict, list, tuple)):
                    serialized_value = json.dumps(value, default=str)
                elif isinstance(value, (str, int, float, bool)):
                    serialized_value = json.dumps(value)
                else:
                    serialized_value = pickle.dumps(value).decode('latin1')
                
                pipe.setex(key, ttl, serialized_value)
            
            await pipe.execute()
            return True
            
        except Exception as e:
            logger.error(f"Cache set_many error: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern"""
        if not self.client:
            return 0
        
        try:
            keys = await self.client.keys(pattern)
            if keys:
                return await self.client.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache delete_pattern error for pattern {pattern}: {e}")
            return 0
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter"""
        if not self.client:
            return None
        
        try:
            return await self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.client:
            return {}
        
        try:
            info = await self.client.info()
            return {
                "used_memory": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": (
                    info.get("keyspace_hits", 0) / 
                    max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1)
                ) * 100
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {}
    
    async def flush_all(self) -> bool:
        """Flush all cache data"""
        if not self.client:
            return False
        
        try:
            await self.client.flushall()
            logger.warning("Cache flushed - all data cleared")
            return True
        except Exception as e:
            logger.error(f"Cache flush error: {e}")
            return False


# Global cache manager instance
cache_manager = CacheManager()


# Decorator for caching function results
def cached(prefix: str, ttl: Optional[int] = None, key_func: Optional[callable] = None):
    """Decorator for caching function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# Rate limiting using Redis
class RateLimiter:
    """Redis-based rate limiter"""
    
    def __init__(self):
        self.client = redis_client
    
    async def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Check if request is allowed within rate limit"""
        if not self.client:
            return True  # Allow if Redis is not available
        
        try:
            current = await self.client.incr(key)
            if current == 1:
                await self.client.expire(key, window)
            
            return current <= limit
            
        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            return True  # Allow on error
    
    async def get_remaining(self, key: str, limit: int) -> int:
        """Get remaining requests in current window"""
        if not self.client:
            return limit
        
        try:
            current = await self.client.get(key)
            if current is None:
                return limit
            
            return max(0, limit - int(current))
            
        except Exception as e:
            logger.error(f"Rate limiter get_remaining error: {e}")
            return limit


# Global rate limiter instance
rate_limiter = RateLimiter()
