

def format_message(data):
    """
    Format a list of predictions into a natural language-style message for WeChat.

    Args:
        predictions_list (list): List of prediction dictionaries.

    Returns:
        str: Formatted string in natural language.
    """
    # Title
    title = "📊 K的整体预测\n"

    # Initialize variables for SH and SZ totals
    sh_sz_current_volume = 0
    sh_sz_cumulative_volumes = {}

    # Process each index
    messages = []
    for prediction in data:
        index_code = prediction.get('index_code', 'N/A')
        current_time = prediction.get('current_time', 'N/A')
        current_volume = prediction.get('current_volume', 0) / 1e8  # Convert to billions
        
        # Accumulate SH and SZ totals
        if index_code in ["000001", "399001"]:
            sh_sz_current_volume += current_volume
            if 'predictions' in prediction:
                for pred in prediction['predictions']:
                    target_time = pred['target_time']
                    cumulative_volume = pred['predicted_cumulative_volume'] / 1e8  # Convert to billions
                    if target_time not in sh_sz_cumulative_volumes:
                        sh_sz_cumulative_volumes[target_time] = 0
                    sh_sz_cumulative_volumes[target_time] += cumulative_volume
        
        # Format individual index message
        message = f"指数代码 {index_code}：\n" \
                  f"- 当前时间：{current_time}\n" \
                  f"- 当前成交量：{current_volume:.2f} 亿\n"
        
        if 'predictions' in prediction:
            for pred in prediction['predictions']:
                target_time = pred['target_time']
                cumulative_volume = pred['predicted_cumulative_volume'] / 1e8  # Convert to billions
                message += f"  * 预计到 {target_time}：累计成交量为 {cumulative_volume:.2f} 亿\n"
        else:
            message += "  * 无预测数据\n"
        
        messages.append(message.strip())
    
    # Add SH + SZ totals as a separate section
    sh_sz_message = f"沪深两市总计：\n" \
                    f"- 当前时间：{current_time}\n" \
                    f"- 当前成交量：{sh_sz_current_volume:.2f} 亿\n"
    for target_time, cumulative_volume in sh_sz_cumulative_volumes.items():
        sh_sz_message += f"  * 到 {target_time}：累计成交量为 {cumulative_volume:.2f} 亿\n"

    # Add SH + SZ totals before HSI
    messages.insert(2, sh_sz_message.strip())

    # Footer
    footer = "\n仅供学习交流"
    
    return f"{title}\n" + "\n\n".join(messages) + f"\n\n{footer}"