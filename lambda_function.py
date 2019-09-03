import json
from PIL import Image
from io import BytesIO
from botocore.vendored import requests
import os

bot_api_key = os.environ['BOT_API_KEY']
bot_api_url = "https://api.telegram.org/bot{0}".format(bot_api_key)

def lambda_handler(event, context):
    message = json.loads(event['body'])['message']
    chat_id = message['chat']['id']
    sticker_file_id = None
    message_id = 0
    if 'sticker' in message.keys():
    	sticker_file_id = message['sticker']['file_id']
    	message_id = message['message_id']
    if ('reply_to_message' in message.keys() and 'sticker' in message['reply_to_message'].keys()):
    	sticker_file_id = message['reply_to_message']['sticker']['file_id']
    	message_id = message['reply_to_message']['message_id']
    if sticker_file_id is not None:
    	send_chat_action(chat_id,'upload_photo')
    	send_image(chat_id,message_id,sticker_file_id)
    return {
        'statusCode': 200,
        'body': ''
    }

def send_image(chat_id,message_id,file_id):
	getFile_url = "{0}/getFile".format(bot_api_url)
	getFile_req = requests.post(getFile_url, data={'file_id':file_id}).json()
	if getFile_req['ok'] == False:
		return False
	file_path = getFile_req['result']['file_path']
	file_url = "https://api.telegram.org/file/bot{0}/{1}".format(bot_api_key,file_path)
	r = requests.get(file_url)
	im = Image.open(BytesIO(r.content))
	rgb_im = im.convert('RGB')
	imgfile = BytesIO()
	rgb_im.save(imgfile, "PNG")
	imgfile.seek(0)
	send_body = {
		'chat_id': chat_id,
		'reply_to_message_id': message_id
	}
	sendPhoto_url = "{0}/sendPhoto".format(bot_api_url)
	send_chat_action(chat_id,'upload_photo')
	r = requests.post(sendPhoto_url, files={'photo':imgfile}, data=send_body)
	if r.status_code != 200:
		print(r.content)

def send_chat_action(chat_id,action):
	requests.post("{0}/sendChatAction".format(bot_api_url), 
		json={'chat_id':chat_id,'action':action})
