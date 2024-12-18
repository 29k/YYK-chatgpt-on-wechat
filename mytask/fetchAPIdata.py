import requests
import numpy as np
from mytask.wechatmsg import  format_predictions_for_wechat
from datetime import datetime
from mytask.fetch_stock_api import fetch_stock_hk_index_spot_em_df, fetch_stock_sh_sz_spot_em, get_sh_sz_index_volume, update_payload


payload_list = [
        {"index_code": "000001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "399001", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "15:00:00"]},
        {"index_code": "HSI", "current_time": "9:50:00", "current_volume": 8000000, "target_times": ["11:30:00", "16:15:00"]}
    ]

def update_payload_list(payload_list):
    new_payload_list = []
    sh_sz_data = fetch_stock_sh_sz_spot_em()
    hk_data = fetch_stock_hk_index_spot_em_df()
    for payload in payload_list:
        new_payload_list.append(update_payload(payload, sh_sz_data=sh_sz_data,hk_data=hk_data))
    return new_payload_list

def send_prediction_request(payload):
    """
    Send a prediction request to the FastAPI server.

    Args:
        payload (dict): The request payload containing index_code, current_time, current_volume, and target_times.

    Returns:
        dict: The response JSON from the API if successful.

    Raises:
        Exception: If the API call fails or returns a non-200 status code.
    """
    
    # Request payload
    # payload = {
    #     "index_code": "000001",
    #     "current_time": "9:50:00",
    #     "current_volume": 8000000,
    #     "target_times": ["15:00:00"]
    # }
    
    # API endpoint
    url = "http://127.0.0.1:8000/predict/"
    j_data = payload
    try:

        # Ensure all payload values are JSON-serializable
        payload = {key: (int(value) if isinstance(value, (np.int64, np.int32)) else value)
                   for key, value in payload.items()}
        # Send the POST request
        response = requests.post(url, json=payload, proxies={"http": None, "https": None})
        
        #j_data = payload
        # Check response
        if response.status_code == 200:
            j_data = response.json()
            j_data["index_code"] = payload["index_code"]
            j_data["current_time"] = payload["current_time"]
            j_data["current_volume"] = payload["current_volume"]
            j_data["IsPredicted"] = True
            return j_data  # Successful response
        else:
            # Include error details in j_data
            j_data["index_code"] = payload["index_code"]
            j_data["current_time"] = payload["current_time"]
            j_data["current_volume"] = payload["current_volume"]
            j_data["IsPredicted"] = False
            j_data["ErrorMsg"] = f"Error: {response.status_code}, {response.text}"
            return j_data  # Successful response
            #raise Exception(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        
        j_data["index_code"] = payload["index_code"]
        j_data["current_time"] = payload["current_time"]
        j_data["current_volume"] = payload["current_volume"]
        j_data["IsPredicted"] = False
        # Include exception details in j_data
        j_data["ErrorMsg"] = f"Failed to send prediction request: {str(e)}"
        return j_data  # Successful response
        #raise Exception(f"Failed to send prediction request: {str(e)}")


def get_predict_volume(payload_list):
    predictions_list = []
    for payload in payload_list:
        print(payload)
        predictions_list.append(send_prediction_request(payload))
    return predictions_list




# fetch sh data
payload_sh = {
    "index_code": "000001",
    "current_time": "9:50:00",
    "current_volume": 8000000,
    "target_times": ["14:00:00","15:00:00"]
}
# fetch sz data
payload_sz = {
    "index_code": "399001",
    "current_time": "9:50:00",
    "current_volume": 8000000,
    "target_times": ["14:00:00","15:00:00"]
}
# fetch hsi data
payload_hsi = {
    "index_code": "HSI",
    "current_time": "9:50:00",
    "current_volume": 8000000,
    "target_times": ["15:00:00","16:0:00"]
}
