import requests, io
from PIL import Image
from config import bot_api_key

bot_api_url = "https://api.telegram.org/bot{0}".format(bot_api_key)

def send_image(chat_id,message_id,file_id):
    getFile_url = "{0}/getFile".format(bot_api_url)
    getFile_req = requests.post(getFile_url, data={'file_id':file_id}).json()
    if getFile_req['ok'] == False:
        return False
    file_path = getFile_req['result']['file_path']
    file_url = "https://api.telegram.org/file/bot{0}/{1}".format(bot_api_key,file_path)
    in_file = io.BytesIO()
    out_file = io.BytesIO()
    in_file.write(requests.get(file_url).content)
    in_file.seek(0)
    im = Image.open(in_file).convert('RGBA')
    im.save(out_file,'png',optimize=True)
    out_file.seek(0)
    send_body = {
        'chat_id': chat_id,
        'reply_to_message_id': message_id,
        'disable_notification': True
    }
    files_body = { 'document' : ("%s.png"%(file_id,), out_file, 'image/png' )}
    sendPhoto_url = "{0}/sendDocument".format(bot_api_url)
    send_chat_action(chat_id,'upload_photo')
    r = requests.post(sendPhoto_url, files=files_body, data=send_body)

def send_chat_action(chat_id,action):
    requests.post("{0}/sendChatAction".format(bot_api_url), 
        json={'chat_id':chat_id,'action':action})