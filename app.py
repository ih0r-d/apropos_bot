from flask import Flask, request
import telegram
from bot.credentials import TOKEN, URL, USER_NAME

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    global answer
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    name = update.message.chat.first_name + " " + update.message.chat.last_name
    if text == "/start":
        answer = """Hi, everyone, :) We're at the stage of developing a memento bot, expect a beta release, 
        or more information about commands, please enter /inform """
    elif text == "/inform":
        answer = """
            /set_email - for send emails \n /set_phone - sending an SMS message about the event" \
                 """
    bot.sendMessage(chat_id=chat_id, text=answer, reply_to_message_id=msg_id)

    return 'Ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
