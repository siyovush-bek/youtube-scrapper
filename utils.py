import csv
import os
from youtube import extract_data, search, youtube

def get_video_ids(query, max_count=30):
    max_count = os.environ.get('MAXRESULTS') or max_count
    response = search(youtube, q=query, maxResults=max_count)
    items = response.get("items")
    return [
        item["id"]["videoId"] for item in items if item["id"].get('videoId')
    ]

def save_to_csv(entries: list, filename: str) -> None:
    keys = entries[0].keys()
    
    with open(f'{filename}.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(entries)

def extract_and_save(query, filename):
    datas = []
    ids = get_video_ids(query)
    print(f'{len(ids)} videos found')
    for video_id in ids:
        data = extract_data(video_id)
        datas.append(data)
    print('Videos parsed')
    print(f'Saving to {filename}.csv')
    save_to_csv(datas, filename)
    print('Saved')

