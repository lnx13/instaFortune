import json
import codecs
import console
import time
import random
from instagram_private_api import Client
	
def from_json(json_object):
	if '__class__' in json_object and json_object['__class__'] == 'bytes':
		return codecs.decode(json_object['__value__'].encode(), 'base64')
	return json_object

def print_banner():
	console.clear()
	console.set_color(1,0,0)
	console.set_font("Menlo-Bold", 30)
	print("Insta Fortune!", end="")
	print("=" * 14)
	console.set_color(1,1,1)
	console.set_font()
	
def print_stats():
	console.set_font("Menlo-Bold", 14)
	print('Всего коментариев: ')
	console.set_font()
	print(len(all_comments))
	console.set_font("Menlo-Bold", 14)
	print('Хотят открытку: ')
	console.set_font()
	print(len(comments))
	console.set_font("Menlo-Bold", 14)
	console.set_color(1,0,0)
	print('-' * 14)
	console.set_color(1,1,1)
	console.set_font()

with open("login.json") as saved_sattings:
	cached_settings = json.load(saved_sattings, object_hook=from_json)


print_banner()

api = Client(None, None,
	settings=cached_settings)

last_post = api.self_feed()['items'][0]
last_post_id = last_post['id']
last_post_comment_count = last_post['comment_count']

post_likers = [ x['username']  for x in api.media_likers(last_post_id)['users']]

all_comments = api.media_n_comments(last_post_id, n=last_post_comment_count)

comments = []
for comment in all_comments:
	if '#хочуоткрытку' in comment['text']:
		comments.append(comment)

print_stats()
print()
console.set_color(1,0,0)
print('-' * 14)
console.set_color(1,1,1)
time.sleep(1)

while True:
	for x in range(1,7):
		rand = random.randint(0, len(comments)-1)
		comment = comments[rand]
		
		print_banner()
		print_stats()
		print('🎲' * x)
		console.set_color(1,0,0)
		print('-' * 14)
		console.set_color(1,1,1)
		
		console.set_font("Menlo-Bold", 15)
		print('@{0}({1}):'.format(
			comment['user']['username'], 
			comment['user']['full_name']))
		console.set_font()
		print(comment['text'])
		time.sleep(0.4 + (x**2)/20)
		x += 1
		
	print()
	
	like = comment['user']['username'] in post_likers
	subscribe = api.friendships_show(comment['user_id'])['followed_by']
	
	print("Лайк:{}, Подписка:{}".format("✅" if like else "❌", "✅" if subscribe else "❌"))
	console.set_font("Menlo-Bold", 20)
	if like and subscribe:
		print("🎉" * 10)
		break
	else:
		print("😢" * 10)
		time.sleep(3)
	console.set_font()
