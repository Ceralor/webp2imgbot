from bottle import Bottle, request, response
from helpers import send_image, send_chat_action
appplication = Bottle()

@application.route('/', method='POST')
def message_handler():
    message = request.json['message']
    chat_id = message['chat']['id']
    sticker_file_id = None
    message_id = 0
    if 'sticker' in message.keys() and 'emoji' not in message['sticker'].keys():
        sticker_file_id = message['sticker']['file_id']
        message_id = message['message_id']
    if 'reply_to_message' in message.keys() and \
        "@autowebp2imgbot" in message["text"] and \
        'sticker' in message['reply_to_message'].keys():
        sticker_file_id = message['reply_to_message']['sticker']['file_id']
        message_id = message['reply_to_message']['message_id']
    if sticker_file_id is not None:
        send_chat_action(chat_id,'upload_photo')
        send_image(chat_id,message_id,sticker_file_id)
    response.type = 'application/json'
    response.status = 200
    return '{}'

application.run(server="paste")
