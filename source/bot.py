import telebot as tb
import telebot.types as types
import camera
import utils
import time

import tokens

tconv = lambda x: time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime(x))

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
""", reply_markup = '')
    
@bot.message_handler(commands=['photo'])
def send_photo(message):
    bot.send_message(message.chat.id, 'Делаю фотографию 📸, секунду')
    result, name = camera.capture_photo(f'{message.chat.id}_{tconv(message.date)}.png')
    if result:
        file = open(name, 'rb')
        bot.send_message(message.chat.id, 'Вот фото')
        bot.send_photo(message.chat.id, file)
        # camera.remove(name)
    if result == camera.CAMERA_CAPTURE_ERROR:
        bot.send_message(message.chat.id, 'Ошибка камеры, попробуйте позже')
    if result == camera.CAMERA_CAPTURE_ERROR_BUSY:
        bot.send_message(message.chat.id, 'Камера сейчас занята, попробуйте позже')
        
@bot.message_handler(commands=['video'])
def ask_lenght(message):
    length_keyboard = tb.types.ReplyKeyboardMarkup()
    but5 = types.KeyboardButton('5')
    but10 = types.KeyboardButton('10')
    but15 = types.KeyboardButton('15')
    but30 = types.KeyboardButton('30')
    length_keyboard.add(but5, but10)
    length_keyboard.add(but15, but30)
    bot.send_message(message.chat.id, 'Сколько секунд записать? ⏲', reply_markup=length_keyboard)
    bot.register_next_step_handler(message, send_video)

def send_video(message):
    # Проверка разумности длины видео
    res, length = utils.convertStr(message.text)
    if res:
        if length < 1:
            bot.send_message(message.chat.id, f'🤨🤨🤨', reply_markup = types.ReplyKeyboardRemove())
            return
        if length > 60:
            bot.send_message(message.chat.id, f'У меня нету датацентра для всех этих видео, давай покороче там', reply_markup = types.ReplyKeyboardRemove())
            return
        # Запись и отправка видео
        bot.send_message(message.chat.id, '🔴 Записываю видео', reply_markup = types.ReplyKeyboardRemove())
        result, name = camera.capture_video(f'{message.chat.id}_{tconv(message.date)}.mp4', length)
        if result:
            bot.send_message(message.chat.id, '✅ Готово, отправляю')
            file = open(name, 'rb')
            bot.send_video(message.chat.id, file)
            # camera.remove(name)
        if result == camera.CAMERA_CAPTURE_ERROR:
            bot.send_message(message.chat.id, 'Ошибка камеры, попробуйте позже')
        if result == camera.CAMERA_CAPTURE_ERROR_BUSY:
            bot.send_message(message.chat.id, 'Камера сейчас занята, попробуйте позже')
    else: 
        bot.send_message(message.chat.id, f'Ну ты такой смешной, я не могу. Сам записывай видео в "{message.text}" секунд', reply_markup = types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    print('Starting bot...')
    bot.infinity_polling()

