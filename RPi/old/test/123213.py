import zmq
import json
import time
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://10.0.0.54:8766")






while True:
    try:
        time.sleep(1)
        key = input()
        key = key.split(':',1)
        dict = {}
        dict[key[0]] = key[1]
        json_sensor = json.dumps(dict)
        time.sleep(0.05)
        sensor_structure = {
            "payload_name": "setting",
            "payload_data": json_sensor
        }
        print(sensor_structure)
        socket.send_json(json.dumps(sensor_structure))
        print("publish")
    except(Exception) as e:
        print(e)



