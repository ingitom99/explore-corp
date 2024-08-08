import matplotlib.pyplot as plt
import datetime

def plot(data : list[tuple[str, float]], title : str, path : str):

    dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in data]
    values = [value for _, value in data]

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o')

    # Customize the plot
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Use a tight layout to prevent the x-label from being cut off
    plt.tight_layout()

    # Display the plot
    plt.savefig(path)