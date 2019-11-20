import telegram
from telegram import InputMediaPhoto
import  vk_api
import time

def two_factor():
    code = input('Code?')
    return code, True

chat_id = '@testchannel_darov'
token = open('token').read().strip()
login, password = open('vk').read().strip().split(' ')

try:
    last_timestamp = int(open('timestamp').read().strip())
except:
    with open('timestamp', 'w') as f:
        last_timestamp = int(time.time())
        f.write(str(last_timestamp))

# Create telegram bot
tg = telegram.Bot(token=token)

# Authenticate and get api
vk_session = vk_api.VkApi(login, password, auth_handler=two_factor)
vk_sessoin = vk_session.auth()
vk = vk_session.get_api()

# Create vk tools for posts collecting
vk_tools = vk_api.tools.VkTools(vk)

# Get the posts (Count after multiplies on 25. E.g. count = 1 => 25 posts)
values = {'domain': 'yumemirukusuri', 'count': 1, 'filter': 'owner'}
response = vk_tools.get_all('wall.get', 1, values=values, limit=1)

# Get the new posts
new_posts = [p for p in response['items'][1:] if p['date'] > last_timestamp]
if len(new_posts) != 0:
    last_timestamp = max([p['date'] for p in new_posts]) + 1

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
        tg.send_photo(chat_id=chat_id, media=imgs[0], caption=text)
    if 2 <= len(imgs) <= 10:
        tg.send_media_group(chat_id=chat_id, media=imgs, caption=text)
    if 10 < len(imgs):
        tg.send_media_group(chat_id=chat_id, media=imgs[:10], caption=text)

# Update timestamp
with open('timestamp', 'w') as f:
    f.write(str(last_timestamp))
