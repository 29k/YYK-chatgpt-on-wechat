

def format_message(data):
    """
    Format a list of predictions into a natural language-style message for WeChat.

    Args:
        data (list): List of prediction dictionaries.

    Returns:
        str: Formatted string in natural language.
    """
    # Title
    title = "📊 YYK的整体预测\n"

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
                  f"- 当前成交额：{current_volume:.2f} 亿\n"
        
        if 'predictions' in prediction:
            # Add 前日对标时间交易量 and 前5日对标时间交易量均值 once per index
            latest_days_volume = prediction['predictions'][0].get('latest_days_volume', 0) / 1e8  # Convert to billions
            mean_volume_5days = prediction['predictions'][0].get('5days_mean_volume', 0) / 1e8  # Convert to billions

            message += f"    - 前日对标时间交易额：{latest_days_volume:.2f} 亿\n" \
                       f"    - 前5日对标时间交易额均值：{mean_volume_5days:.2f} 亿\n"

            for pred in prediction['predictions']:
                target_time = pred['target_time']
                cumulative_volume = pred['predicted_cumulative_volume'] / 1e8  # Convert to billions
                percentage = pred.get('predicted_cumulative_percentage', 0) * 100  # Convert to percentage

                message += f"  * 预计到 {target_time}：\n" \
                           f"    - 累计成交额：{cumulative_volume:.2f} 亿\n" \
                           f"    - 预计累计百分比：{percentage:.1f}%\n"
        else:
            message += "  * 无预测数据\n"

        messages.append(message.strip())

    # Footer
    footer = "\n仅供学习交流"

    return f"{title}\n" + "\n\n".join(messages) + f"\n\n{footer}"
