import requests
from mytask.fetchAPIdata import *
from loguru import logger



def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  # Process API response as needed
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
payload_list = [
        {"index_code": "000001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "399001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "HSI", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "16:15:00"]}
    ]


def fetch_volume_predict_data(payload_list):
    try:
        update_pay_load_list = update_payload_list(payload_list)
        logger.info("update_pay_load_list >>>!!! " + str(update_pay_load_list))
        get_predict_volume_data = get_predict_volume(update_pay_load_list)
        logger.info("get_predict_volume >>>" + str(get_predict_volume_data))
        return get_predict_volume_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None