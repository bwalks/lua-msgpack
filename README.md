# lua-msgpack
Python example for using MessagePack to serialize Redis Hash.

```
import msgpack
import redis
from time import time

client = redis.StrictRedis(host='localhost', port=7200)

# Scripts are passed in two argument lists: KEYS and ARGV

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

key = '12345'
def with_script():
  s = time()
  _ = msgpack.unpackb(script(keys=[key]), use_list=False)
  print time() - s

def with_hgetall():
  s = time()
  _ = client.hgetall(key)
  print time() - s```
