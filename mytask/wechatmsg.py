

def format_predictions_for_wechat(predictions_list):
    """
    Format a list of predictions into a table-like text for WeChat.

    Args:
        predictions_list (list): List of prediction dictionaries.

    Returns:
        str: Formatted string for WeChat.
    """
    headers = f"{'Index Code':<10}{'Current Time':<15}{'Current Volume (亿)':<20}{'Target Time':<15}{'Cumulative %':<15}{'Cumulative Volume (亿)':<20}"
    separator = "-" * 95
    rows = []
    for prediction in predictions_list:
        index_code = prediction.get('index_code', 'N/A')
        current_time = prediction.get('current_time', 'N/A')
        current_volume = prediction.get('current_volume', 0) / 1e8  # Convert to billions
        if 'predictions' in prediction:
            for pred in prediction['predictions']:
                row = (
                    f"{index_code:<10}{current_time:<15}{current_volume:<20.2f}"
                    f"{pred['target_time']:<15}{pred['predicted_cumulative_percentage'] * 100:<15.1f}"
                    f"{pred['predicted_cumulative_volume'] / 1e8:<20.2f}"
                )
                rows.append(row)
        else:
            row = f"{index_code:<10}{current_time:<15}{current_volume:<20.2f}{'N/A':<15}{'N/A':<15}{'N/A':<20}"
            rows.append(row)
    return f"{headers}\n{separator}\n" + "\n".join(rows)