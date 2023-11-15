import datetime
import json


def get_current_time():
    time_info = {
        "time": str(datetime.datetime.now()),
    }
    return json.dumps(time_info)


if __name__ == "__main__":
    print(get_current_time())
