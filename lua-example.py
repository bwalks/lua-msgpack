from time import time

import msgpack
import redis

client = redis.StrictRedis(host='localhost', port=7200)

# Script will cache the results with a TTL
lua = """
local hash_key = KEYS[1]
local cached_key = hash_key .. ':cached'
local ttl = ARGV[1] or 2
if redis.call('exists', cached_key) == 1 then
  return redis.call('get', cached_key)
else
  local mspack_val = cmsgpack.pack(redis.call('hgetall', hash_key))
  redis.call('setex', cached_key, ttl, mspack_val)
  return mspack_val
end"""
script = client.register_script(lua)

key = 'hashkey'

def with_script():
  s = time()
  _ = msgpack.unpackb(script(keys=[key], args=[2]), use_list=False)
  return time() - s

def with_hgetall():
  s = time()
  _ = client.hgetall(key)
  return time() - s

print "With MessagePack: " , with_script()
print "With HGETALL: " , with_hgetall()
