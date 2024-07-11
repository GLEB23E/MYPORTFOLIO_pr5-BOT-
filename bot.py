import telebot
from telebot import types
import qrcode
from io import BytesIO

# your token 
token = "7073904415:AAHATSpoPu4ZnKJ36b2ecbHISOd88CxNMns"
bot = telebot.TeleBot(token)

# Хранилище состояний
user_states = {}

@bot.message_handler(commands=["start"])
def start_message2(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton(text="qr")
    keyboard.add(button1)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "qr")
def request_link(message):
    bot.send_message(message.chat.id, "Please send the link you want to turn into a QR code.")
    user_states[message.chat.id] = 'awaiting_link'

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_link')
def generate_qr(message):
    url = message.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    bot.send_photo(message.chat.id, byte_io, caption="Here is your QR code.")
    user_states[message.chat.id] = None

if __name__ == '__main__':
    bot.infinity_polling()
