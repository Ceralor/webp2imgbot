import requests, subprocess, os

bot_api_key = os.environ['BOT_API_KEY']
bot_api_url = "https://api.telegram.org/bot{0}".format(bot_api_key)

def send_image(chat_id,message_id,file_id):
	getFile_url = "{0}/getFile".format(bot_api_url)
	getFile_req = requests.post(getFile_url, data={'file_id':file_id}).json()
	if getFile_req['ok'] == False:
		return False
	file_path = getFile_req['result']['file_path']
	file_url = "https://api.telegram.org/file/bot{0}/{1}".format(bot_api_key,file_path)
	in_file = "/tmp/{0}.webp".format(file_id)
	out_file = "/tmp/{0}.png".format(file_id)
	with open(in_file,'wb') as fd:
		fd.write(requests.get(file_url).content)
	subprocess.run(['bin/dwebp', '-o',out_file,'--',in_file])
	send_body = {
		'chat_id': chat_id,
		'reply_to_message_id': message_id
	}
	files_body = { 'photo' : open(out_file,'rb') }
	sendPhoto_url = "{0}/sendPhoto".format(bot_api_url)
	send_chat_action(chat_id,'upload_photo')
	r = requests.post(sendPhoto_url, files=files_body, data=send_body)

def send_chat_action(chat_id,action):
	requests.post("{0}/sendChatAction".format(bot_api_url), 
		json={'chat_id':chat_id,'action':action})