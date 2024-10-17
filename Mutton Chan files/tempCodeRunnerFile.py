from datetime import datetime, timedelta

# Get the current time
current_time = datetime.now()

# Set a specific time (you can replace this with your desired time)
specific_time = datetime(current_time.year, current_time.month, current_time.day, 10, 30, 0)

# Calculate the time difference
time_difference = specific_time - current_time

# Format the time difference as desired
formatted_time_difference = str(time_difference)

# Print the formatted time difference
print(formatted_time_difference)