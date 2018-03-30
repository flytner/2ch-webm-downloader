import requests
import os
import time
import threading
from queue import Queue

start = time.time()
def downloader():
    while True:
        file = queue.get()
        r = requests.get('https://2ch.hk/b/src/' + thread_id + '/' + file, stream = True)
        length = r.headers.get('content-length')

        print('{} Downloading: {} ({} KB)'.format(threading.current_thread().name, file, length))

        with open(os.path.join(directory, file), 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

        queue.task_done()

thread_url = input("Input thread url: ")
while not (thread_url.endswith(".html") and (thread_url.startswith("https://") or thread_url.startswith("http://"))):
    thread_url = input("Input correct thread url!!!: ")
thread_url = thread_url.replace("html", "json")

try:
    r = requests.get(thread_url)
    r.raise_for_status()
except requests.RequestException as e:
    exit(e)

d = r.json()
all_files = []
threads = 10
thread_id = d['current_thread']
title = d['title']
directory = title + ' id' + thread_id

print('GET ', title)
if not os.path.exists(directory):
    print("Make dir: ", directory, "\n")
    os.makedirs(directory)
else:
    print("The directory is already exist. Downloading the rest videos...")

for i in d['threads'][0]['posts']:
    if i['files']:
        each_post = [x['name'] for x in i['files']]
        for each_file in each_post:
            if 'webm' in each_file or 'mp4' in each_file:
                all_files.append(each_file)
                if os.path.exists(os.path.join(directory, each_file)):
                    print(each_file, "already downloaded", end='\r')
                    time.sleep(0.01)
                    continue
print("Starting {} threads for {} files".format(threads, len(all_files)))
queue = Queue()

for i in range(threads):
    t = threading.Thread(target=downloader)
    t.setDaemon(True)
    t.start()

for file in all_files:
    queue.put(file)

queue.join()
print('total {}'.format(len(all_files)))
end = time.time()
print(end - start, 'seconds')
