import os
import time
from datetime import datetime, timedelta

# Path to the recordings directory
RECORDINGS_FOLDER = 'recordings'

# Time threshold (30 days ago)

# Function to delete old files
def delete_old_files():
    for root, dirs, files in os.walk(RECORDINGS_FOLDER):
        for file in files:
            time_threshold = datetime.now() - timedelta(days=30)
            print(f"Checking {file}")
            file_path = os.path.join(root, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"File time: {file_time}", time_threshold)
            if file_time < time_threshold:
                os.remove(file_path)
                print(f"Deleted {file_path}")

if __name__ == "__main__":
    while True:
        print("Checking for old files to delete...")
        delete_old_files()

        # Sleep for 1 day before checking again
        time.sleep(86400)  # 86400 seconds = 1 day
