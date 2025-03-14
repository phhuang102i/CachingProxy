from fastapi import FastAPI
import json
import redis
import httpx
import hashlib
import logging

app = FastAPI()
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
FORWARDING_PATH = "http://dummyjson.com"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def generate_cache_key(url: str):
    return hashlib.sha256(url.encode()).hexdigest()

@app.get("/{full_path:path}")
async def catch_all(full_path):
    forwarding_url = f"{FORWARDING_PATH}/{full_path}"
    logger.debug(f"Forwarding{full_path}")

    cache_key = generate_cache_key(forwarding_url)
    cached_response = redis_client.get(cache_key)
    if cached_response:
        logger.info("X-Cache: HIT")
        try:
            return json.loads(cached_response)
        except json.JSONDecodeError:
            return cached_response


    logger.info("X-Cache: MISS")
    async with httpx.AsyncClient() as client:
        response = await client.get(forwarding_url)

    try:
        response_content = response.json()
        data_to_cache = json.dumps(response_content)
    except ValueError:
        response_content = response.text
        data_to_cache = response_content

    redis_client.setex(cache_key, 60, data_to_cache)

    return response_content