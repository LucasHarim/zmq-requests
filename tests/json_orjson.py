import time
import json
import orjson
import datetime

data = {
    "type": "job",
    "created_at": f'{datetime.datetime(1970, 1, 1)}',
    "status": "ok",
    "payload": [i for i in range(10)],
}

def time_dumps(data: dict, dump_method, n_loops = 1000) -> float:

    now = time.time()

    for _ in range(n_loops):
        dump_method(data)

    return time.time() - now

def time_loads(data: str | bytes, loads_method, n_loops = 1000) -> float:
    now = time.time()

    for _ in range(n_loops):
        loads_method(data)
    
    return time.time() - now
    
if __name__ == '__main__':

    dt_json = time_dumps(data, lambda x: json.dumps(x), 10000)
    dt_orjson = time_dumps(data, lambda x: orjson.dumps(x).decode(), 10000)
    
    dt_loads_json = time_loads(json.dumps(data), lambda x: json.loads(x), 10000)
    dt_loads_orjson = time_loads(json.dumps(data), lambda x: orjson.loads(x), 10000)

    print(f'Timing dumps methods.\nBuilt in Json: {dt_json} s\nOrjson: {dt_orjson} s')
    print()
    print(f'Timing loads methods.\nBuilt in Json: {dt_loads_json} s\nOrjson: {dt_loads_orjson} s')