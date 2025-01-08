import subprocess
import os
import time
import datetime
import threading
import json

def load_rtsp_urls(config_path='config.json'):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

output_dir = "recordings"

os.makedirs(output_dir, exist_ok=True)

def record_stream(camera_name, rtsp_url, duration=60):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    currentday = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(output_dir, currentday, camera_name), exist_ok=True)

    output_file = os.path.join(output_dir, currentday, camera_name, f"{camera_name}_{timestamp}.mp4")

    command = f"ffmpeg -rtsp_transport tcp -use_wallclock_as_timestamps 1 -i '{rtsp_url}' -vcodec copy -acodec copy -t {duration} {output_file}"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Recording {camera_name} saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error recording {camera_name}: {e}")


def start_recording(rtsp_urls):
    threads = []

    for camera_name, rtsp_url in rtsp_urls.items():
        thread = threading.Thread(target=record_stream, args=(camera_name, rtsp_url))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    rtsp_urls = load_rtsp_urls()

    while True:
        print("Starting recording...")
        start_recording(rtsp_urls=rtsp_urls)
