from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

def get_all_properties():
    # Check if properties are in cache
    properties = cache.get('all_properties')
    if properties is None:
        # Not cached → fetch from database
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties

logger = logging.getLogger(__name__)

def get_all_properties():
    from .models import Property
    from django.core.cache import cache

    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)  # cache 1 hour
    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Logs metrics and returns a dictionary.
    """
    try:
        redis_conn = get_redis_connection("default")
        stats = redis_conn.info("stats")
        hits = stats.get("keyspace_hits", 0)
        misses = stats.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}