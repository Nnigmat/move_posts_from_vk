import telegram
from telegram import InputMediaPhoto
import  vk_api
import time
import requests

CHAT_ID = '@testchannel_darov'

def read_tokens(path='token'):
    return [token.strip() for token in open(path).readlines()]

def read_timestamp(path='timestamp'):
    try:
        timestamp = int(open('timestamp').read().strip())
    except:
        with open('timestamp', 'w') as f:
            timestamp = int(time.time())
            f.write(str(last_timestamp))
    return timestamp

def wall_request(token=None, domain='yememirukusuri'):
    response = requests.get(f'https://api.vk.com/method/wall.get?domain={domain}&access_token={vk_token}&v=5.103&owner_id=-27943506').json()['response']
    return response

tg_token, vk_token = read_tokens()
timestamp = read_timestamp()

# Create telegram bot
tg = telegram.Bot(token=tg_token)

# Get the posts (Count after multiplies on 25. E.g. count = 1 => 25 posts)
response = wall_request(vk_token)

# Get the new posts
new_posts = [p for p in response['items'][1:] if p['date'] > timestamp]
if len(new_posts) != 0:
    timestamp = max([p['date'] for p in new_posts]) + 1

# Get the texts and images from the posts
texts, images = [], []
for post in new_posts:
    texts.append(post['text'])

    # Take only images
    try:
        images.append([InputMediaPhoto(at['photo']['sizes'][-1]['url'], caption=post['text']) for at in post['attachments']])
    except:
        pass

# Send the posts to the telegram
for text, imgs in zip(texts, images):
    if 1 == len(imgs):
        media = imgs[0]
    if 2 <= len(imgs) <= 10:
        media = imgs
    if 10 < len(imgs):
        media = imgs[:10]

    while True:
        try:
            tg.send_media_group(chat_id=CHAT_ID, media=imgs[:10], caption=text)
            break
        except:
            pass

# Update timestamp
with open('timestamp', 'w') as f:
    f.write(str(timestamp))
