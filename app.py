from bottle import Bottle, request, response
from helpers import send_image, send_chat_action
app = Bottle()

@app.route('/')
def greeter():
    response.status = 200
    return "Hello"

@app.route('/procimg', method='POST')
def message_handler():
    message = request.json['message']
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
    response.type = 'text/plain'
    response.status = 200
    return ''
