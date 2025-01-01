import schedule
import time
from mytask.api_handler import fetch_data, fetch_volume_predict_data
from mytask.itchat_handler import send_message, get_group_ids
from mytask.message_manager import format_message
from mytask.config import API_URL, GROUP_NAMES,FETCH_INTERVAL
from loguru import logger


def task():
    print("Task fetch_data is running... ")
    data = fetch_data(API_URL)
    if data:
        message = format_message(data)
        group_ids = get_group_ids(GROUP_NAMES)
        for group_name, group_id in group_ids.items():
            send_message(group_id, message)


payload_list = [
        {"index_code": "000001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "399001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "HSI", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "16:15:00"]}
    ]

def task_volume_predict():
    print("task_volume_predict fetch_data is running... ")
    data = fetch_volume_predict_data(payload_list)
    if data:
        message = format_message(data)
        group_ids = get_group_ids(GROUP_NAMES)
        for group_name, group_id in group_ids.items():
            logger.info("group_id >>> " +  str(group_id))
            send_message(group_id, message)

def fetch_volume_predict():
    print("fetch_volume_predict_data fetch_data is running... ")
    data = fetch_volume_predict_data(payload_list)
    print("here is data >>>>>>>")
    print(data)
    message = format_message(data)
    return message

def run_scheduler():
    print("Scheduler is start")
    # Schedule tasks
    schedule.every().monday.at("09:26").do(task_volume_predict)
    schedule.every().monday.at("11:35").do(task_volume_predict)
    schedule.every().tuesday.at("09:26").do(task_volume_predict)
    schedule.every().tuesday.at("11:35").do(task_volume_predict)
    schedule.every().wednesday.at("09:26").do(task_volume_predict)
    schedule.every().wednesday.at("11:35").do(task_volume_predict)
    schedule.every().thursday.at("09:26").do(task_volume_predict)
    schedule.every().thursday.at("11:35").do(task_volume_predict)
    schedule.every().friday.at("09:26").do(task_volume_predict)
    schedule.every().friday.at("11:35").do(task_volume_predict)
    #schedule.every(1).minutes.do(task_volume_predict)
    while True:
        print("Task is running... ")
        schedule.run_pending()
        time.sleep(1)
