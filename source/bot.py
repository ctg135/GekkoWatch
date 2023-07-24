import telebot as tb
import camera
import time

import tokens

tconv = lambda x: time.strftime("%H-%M-%S_%d-%m-%Y", time.localtime(x))

API_TOKEN = tokens.bot

bot = tb.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
🦎 GekkoWatch 🦎
Короче наблюдаю за Арахисом, пока никого нету дома 😁
👀 Команды:
/photo - сделать фото
/video - записать видео
        
Да, звука в видео нету, не спрашивай почему. 🤨
""")
    
@bot.message_handler(commands=['photo'])
def send_photo(message):
    bot.send_message(message.chat.id, 'Делаю фотографию 📸, секунду')
    result, name = camera.capture_photo(f'{message.chat.id}_{tconv(message.date)}.png')
    if result:
        file = open(name, 'rb')
        bot.send_message(message.chat.id, 'Вот фото')
        bot.send_photo(message.chat.id, file)
    if result == camera.CAMERA_CAPTURE_ERROR:
        bot.send_message(message.chat.id, 'Ошибка камеры, попробуйте позже')
    if result == camera.CAMERA_CAPTURE_ERROR_BUSY:
        bot.send_message(message.chat.id, 'Камера сейчас занята, попробуйте позже')
        
@bot.message_handler(commands=['video'])
def send_photo(message):
    bot.send_message(message.chat.id, '🔴 Записываю видео')
    result, name = camera.capture_video(f'{message.chat.id}_{tconv(message.date)}.mp4', 5)
    if result:
        bot.send_message(message.chat.id, '✅ Готово, отправляю')
        file = open(name, 'rb')
        bot.send_video(message.chat.id, file)
    if result == camera.CAMERA_CAPTURE_ERROR:
        bot.send_message(message.chat.id, 'Ошибка камеры, попробуйте позже')
    if result == camera.CAMERA_CAPTURE_ERROR_BUSY:
        bot.send_message(message.chat.id, 'Камера сейчас занята, попробуйте позже')
    
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

print('Starting bot...')
bot.infinity_polling()
