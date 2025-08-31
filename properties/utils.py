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

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Returns a dictionary with hits, misses, and ratio.
    """
    # Get Redis connection
    redis_conn = get_redis_connection("default")
    
    # Get Redis INFO stats
    info = redis_conn.info(section="stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0
    
    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }
    
    logger.info(f"Redis cache metrics: {metrics}")
    
    return metrics