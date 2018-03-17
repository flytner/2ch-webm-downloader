import requests
import os

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
total = 0
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
                    print(each_file, "is already exist, going to the next video")
                    continue
                total += 1
                print('Downloading', total, '--->', each_file)
                print('test', end='\r')
                r = requests.get('https://2ch.hk/b/src/' + thread_id + '/' + each_file)
                with open(os.path.join(directory, each_file), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
print("Done, total downloaded: ", total)
