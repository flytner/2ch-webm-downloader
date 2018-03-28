import requests
import os
import sys
import time

url = input("Input thread url: ")
while not (url.endswith(".html") and (url.startswith("https://") or url.startswith("http://"))):
    url = input("Input correct thread url!!!: ")
url = url.replace("html", "json")

try:
    r = requests.get(url)
    r.raise_for_status()
except requests.RequestException as e:
    exit(e)

d = r.json()
start = time.time()
total = 0
total_kb = 0
title = d['title']
thread_id = d['current_thread']
directory = title + ' id' + thread_id

print('GET ', title)
if not os.path.exists(directory):
    print("Make dir: ", directory, "\n")
    os.makedirs(directory)
else:
    print("The directory is already exist. Downloading the rest videos...\n")

for i in d['threads'][0]['posts']:
    if i['files']:
        each_post = [x['name'] for x in i['files']]
        for each_file in each_post:
            if 'webm' in each_file or 'mp4' in each_file:
                if os.path.exists(os.path.join(directory, each_file)):
                    print(each_file, "already downloaded", end='\r')
                    time.sleep(0.01)
                    continue
                total += 1
                dl = 0
                r = requests.get('https://2ch.hk/b/src/' + thread_id + '/' + each_file, stream=True)
                length = int(r.headers.get('content-length'))
                total_kb += length
                with open(os.path.join(directory, each_file), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=1024):
                        dl += len(chunk)
                        fd.write(chunk)
                        done = int(25 * dl / length)

                        print("%s: %s [%s%s] %s KB / %s KB" % (total, each_file, '=' * done,\
                        ' ' * (25 - done), int(dl / 1024), int(length / 1024)), end='\r')


print("\nDone, files: ", total)
print(time.time() - start, "seconds")
print(total_kb, "KB")
