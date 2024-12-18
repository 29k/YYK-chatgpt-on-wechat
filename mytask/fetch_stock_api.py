import akshare as ak
import pandas as pd
from datetime import datetime
from loguru import logger

# get HSI index realtime data
def fetch_stock_hk_index_spot_em_df():
    try:
        df = ak.stock_hk_index_spot_em()
        timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hsi_index_data = df[df['代码'].isin(['HSI'])]
        # Add a new column 'datetime' with the current timestamp in Asia/Shanghai timezone

        hsi_index_data = hsi_index_data.copy()  # Ensure we're working with a copy
        hsi_index_data['datetime'] = timenow
        return hsi_index_data 
    except Exception as e:
        # Handle the exception (e.g., log the error or return a default value)
        print(f"An error occurred while fetching the stock data: {e}")
        return None  # You can choose an appropriate return value for error scenarios


# get stock SH SZ index realtime data
def fetch_stock_sh_sz_spot_em():
    try:
        df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
        timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sh_sz_index_data = df[df['代码'].isin(['000001','399001'])]
        # Add a new column 'datetime' with the current timestamp in Asia/Shanghai timezone

        sh_sz_index_data = sh_sz_index_data.copy()  # Ensure we're working with a copy
        sh_sz_index_data['datetime'] = timenow
        return sh_sz_index_data 
    except Exception as e:
        # Handle the exception (e.g., log the error or return a default value)
        print(f"An error occurred while fetching the stock data: {e}")
        return None  # You can choose an appropriate return value for error scenarios

def get_sh_sz_index_volume(index_code: str, stock_data: pd.DataFrame) -> dict:
    """
    Get the volume for a specific stock index from the provided DataFrame.

    Args:
        index_code (str): The index code (e.g., '000001' for Shanghai or '399001' for Shenzhen).
        stock_data (pd.DataFrame): The DataFrame returned by fetch_stock_sh_sz_spot_em.

    Returns:
        dict: A dictionary containing the index code and its corresponding volume.
              Example: {"index_code": "000001", "volume": 12345678.0}
    """

    try:
        if stock_data is None or stock_data.empty:
            raise ValueError("The provided stock data is empty or invalid.")
        
        # Filter for the specified index_code
        filtered_data = stock_data[stock_data['代码'] == index_code]
        
        if filtered_data.empty:
            raise ValueError(f"No data found for index code: {index_code}")
        
        # Extract the volume (assuming the volume column is named '成交量')
        volume = filtered_data['成交量'].values[0]
        
        return {"index_code": index_code, "volume": volume}
    except Exception as e:
        print(f"An error occurred while fetching volume for index {index_code}: {e}")
        return {"index_code": index_code, "volume": None}  # Return None if there's an error


def update_payload(payload, sh_sz_data, hk_data):
    """
    Update the payload with the current time, current volume, and filter target_times based on the current time.

    Args:
        payload (dict): The input payload containing index_code, current_time, current_volume, and target_times.
        sh_sz_data (pd.DataFrame): DataFrame with SH and SZ stock data fetched using fetch_stock_sh_sz_spot_em().
        hk_data (pd.DataFrame): DataFrame with HK stock data fetched using fetch_stock_hk_index_spot_em_df().

    Returns:
        dict: Updated payload with the latest current_time, current_volume, and filtered target_times.
    """
    try:
        # Update current time to now

        # for test set time manally
        current_time = datetime.now().strftime('%H:%M:%S')
        #current_time = "10:50:00"
        payload["current_time"] = current_time

        # Update current_volume based on the index_code
        index_code = payload["index_code"]
        if index_code in ["000001", "399001"]:
            volume_data = sh_sz_data[sh_sz_data["代码"] == index_code]
            if not volume_data.empty:
                payload["current_volume"] = volume_data["成交额"].values[0]
                #payload["current_volume"] = 30000000000
            else:
                payload["current_volume"] = None  # Default if no data found
        elif index_code == "HSI":
            volume_data = hk_data[hk_data["代码"] == index_code]
            if not volume_data.empty:
                payload["current_volume"] = volume_data["成交额"].values[0]
            else:
                payload["current_volume"] = None  # Default if no data found

        # Filter target_times to include only times after the current time
        current_datetime = datetime.strptime(current_time, '%H:%M:%S')
        payload["target_times"] = [
            target_time for target_time in payload["target_times"]
            if datetime.strptime(target_time, '%H:%M:%S') > current_datetime
        ]
        #logger.info("update_payload >>> " + str(payload))
        return payload

    except Exception as e:
        print(f"An error occurred while updating the payload: {e}")
        return payload  # Return the original payload in case of error

