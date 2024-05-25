from config import *
from logic import *
import telebot

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    promt = message.text
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '14D00C6007D350CBE2D1077F04C59209', 'C24698960344CE8247EB986B33B32925')
    model_id = api.get_model()
    uuid = api.generate(promt, model_id)
    images = api.check_generation(uuid)[0]
    path = f'{message.from_user.id}.png'
    api.convert_to_img(images, path)
    photo = open(path, 'rb')
    bot.send_photo(message.chat.id, photo)

bot.infinity_polling()