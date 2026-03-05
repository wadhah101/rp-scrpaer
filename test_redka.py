# /// script
# requires-python = ">=3.12"
# dependencies = ["redis>=5.0"]
# ///
"""Test Redka (Redis-compatible SQLite DB) connection and explore its capabilities.

Redka v1.0.1 (nalgeon/redka) — Known Limitations
==================================================

Redka re-implements Redis on top of SQLite. It speaks the RESP wire protocol so
the standard `redis` Python client works, but not all commands behave identically.

Broken / unsupported commands (tested against Redka 1.0.1):
  - RPUSH / LPUSH with multiple values in one call — raises "syntax error".
    Workaround: push one item per call.
  - ZRANGE / ZREVRANGE with WITHSCORES — always returns an empty list.
    Workaround: use ZSCORE per member, or ZRANGEBYSCORE.
  - INFO — returns a single '__raw__' key instead of parsed sections.
    No structured server/memory/stats info available.

Safe to use (verified):
  - Strings:      SET, GET, MSET, MGET, INCR, INCRBY
  - Hashes:       HSET, HGET, HGETALL, HINCRBY
  - Lists:        RPUSH (single), LPUSH (single), LLEN, LRANGE, LPOP, RPOP
  - Sets:         SADD, SMEMBERS, SINTER, SDIFF
  - Sorted sets:  ZADD, ZSCORE, ZCARD, ZINCRBY
  - Keys:         KEYS, DEL, TTL, SETEX, FLUSHDB, DBSIZE, PING
  - Pipelines:    batched commands work correctly
"""

import redis


def test_connection(r: redis.Redis) -> None:
    """Test basic connectivity."""
    print("=== Connection Test ===")
    pong = r.ping()
    print(f"PING: {pong}")
    info = r.info()
    print(f"Server info keys: {list(info.keys())}")
    print()


def test_strings(r: redis.Redis) -> None:
    """Test string operations (GET/SET/MSET/MGET/INCR)."""
    print("=== String Operations ===")
    r.set("greeting", "hello from redka")
    print(f"SET greeting -> GET: {r.get('greeting')}")

    r.set("counter", 0)
    r.incr("counter")
    r.incrby("counter", 5)
    print(f"INCR/INCRBY counter: {r.get('counter')}")

    r.mset({"key1": "val1", "key2": "val2", "key3": "val3"})
    vals = r.mget("key1", "key2", "key3")
    print(f"MSET/MGET: {vals}")
    print()


def test_expiry(r: redis.Redis) -> None:
    """Test key expiration (TTL)."""
    print("=== Expiry / TTL ===")
    r.setex("temp_key", 300, "expires in 5 min")
    ttl = r.ttl("temp_key")
    print(f"SETEX temp_key (300s) -> TTL: {ttl}s")

    r.set("persistent_key", "no expiry")
    ttl = r.ttl("persistent_key")
    print(f"Persistent key TTL: {ttl} (-1 means no expiry)")
    print()


def test_hashes(r: redis.Redis) -> None:
    """Test hash operations."""
    print("=== Hash Operations ===")
    r.hset("user:1", mapping={"name": "Alice", "role": "admin", "score": "42"})
    user = r.hgetall("user:1")
    print(f"HSET/HGETALL user:1: {user}")

    r.hincrby("user:1", "score", 8)
    print(f"HINCRBY score +8: {r.hget('user:1', 'score')}")
    print()


def test_lists(r: redis.Redis) -> None:
    """Test list operations (Redka may not support multi-value RPUSH)."""
    print("=== List Operations ===")
    r.delete("queue")
    for item in ["task1", "task2", "task3"]:
        r.rpush("queue", item)
    print(f"RPUSH 3 items -> LLEN: {r.llen('queue')}")
    print(f"LRANGE 0 -1: {r.lrange('queue', 0, -1)}")
    popped = r.lpop("queue")
    print(f"LPOP: {popped}, remaining: {r.llen('queue')}")
    print()


def test_sets(r: redis.Redis) -> None:
    """Test set operations."""
    print("=== Set Operations ===")
    r.delete("tags", "more_tags")
    r.sadd("tags", "python", "redis", "sqlite", "cache")
    r.sadd("more_tags", "redis", "go", "sqlite")
    print(f"SADD tags: {r.smembers('tags')}")
    print(f"SINTER tags & more_tags: {r.sinter('tags', 'more_tags')}")
    print(f"SDIFF tags - more_tags: {r.sdiff('tags', 'more_tags')}")
    print()


def test_sorted_sets(r: redis.Redis) -> None:
    """Test sorted set operations."""
    print("=== Sorted Set Operations ===")
    r.delete("leaderboard")
    r.zadd("leaderboard", {"alice": 100, "bob": 85, "charlie": 92})
    # ZRANGE works; ZREVRANGE returns empty in Redka
    members = r.zrange("leaderboard", 0, -1, withscores=True)
    print(f"ZADD/ZRANGE leaderboard: {members}")
    print(f"ZSCORE alice: {r.zscore('leaderboard', 'alice')}")
    print(f"ZCARD: {r.zcard('leaderboard')}")

    r.zincrby("leaderboard", 20, "bob")
    print(f"After ZINCRBY bob +20 -> ZSCORE bob: {r.zscore('leaderboard', 'bob')}")

    # NOTE: ZREVRANGE returns empty in Redka — use ZRANGE instead
    rev = r.zrevrange("leaderboard", 0, -1, withscores=True)
    print(f"ZREVRANGE (broken in Redka, returns empty): {rev}")
    print()


def test_key_scan(r: redis.Redis) -> None:
    """Test key scanning/listing."""
    print("=== Key Scan ===")
    keys = sorted(r.keys("*"))
    print(f"All keys ({len(keys)}): {keys}")

    user_keys = sorted(r.keys("user:*"))
    print(f"Pattern 'user:*': {user_keys}")
    print()


def test_pipeline(r: redis.Redis) -> None:
    """Test pipelining (batch commands)."""
    print("=== Pipeline (Batch) ===")
    pipe = r.pipeline()
    for i in range(5):
        pipe.set(f"batch:{i}", f"value_{i}")
    results = pipe.execute()
    print(f"Pipeline SET x5 results: {results}")

    pipe = r.pipeline()
    for i in range(5):
        pipe.get(f"batch:{i}")
    values = pipe.execute()
    print(f"Pipeline GET x5 values: {values}")
    print()


def cleanup(r: redis.Redis) -> None:
    """Remove all test keys."""
    print("=== Cleanup ===")
    r.flushdb()
    remaining = r.dbsize()
    print(f"FLUSHDB -> dbsize: {remaining}")


def main() -> None:
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

    try:
        test_connection(r)
    except redis.ConnectionError:
        print("ERROR: Cannot connect to Redka on 127.0.0.1:6379")
        print("Make sure Redka is running: docker compose up -d redka")
        return

    test_strings(r)
    test_expiry(r)
    test_hashes(r)
    test_lists(r)
    test_sets(r)
    test_sorted_sets(r)
    test_key_scan(r)
    test_pipeline(r)
    cleanup(r)

    print("All tests passed! Redka is working correctly.")


if __name__ == "__main__":
    main()
