import telebot
import sqlite3
import requests
from telebot import types

bot = telebot.TeleBot('7127901125:AAET69Nhu65t7IUsYfqWVc__XBrhOxEmSMY')

# /start - butttons + edit
# /help
# /photo3to5 /instax /fullPhoto
# /question
# /locations
# /prices
# /examples
# /print - buttons + edit
# /clear - очистити чат
# не забути додати команди через botfather.



@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect('study.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Instax')
    markup.add(btn1)
    msg = bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} (@{message.from_user.username})!", reply_markup=markup)
    bot.register_next_step_handler(msg, on_click)


    msg = bot.send_message(message.chat.id, "PLease, enter your name")
    bot.register_next_step_handler(msg, handle_name)

def handle_name(message):
     global enteredName
     enteredName = message.text.strip()
     msg = bot.send_message(message.chat.id, 'Enter yout password:')
     bot.register_next_step_handler(msg, handle_pass)

def handle_pass(message):
    enteredPassword = message.text.strip()
    conn = sqlite3.connect('study.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES( '%s', '%s')" % (enteredName, enteredPassword))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Show list of all users', callback_data='show_users'))
    bot.send_message(message.chat.id, 'Thanks! Your account has been registered successfully.', reply_markup=markup)

def on_click(message):
    bot.send_message(message.chat.id, "You've clicked keyboard button!")

@bot.message_handler(commands=['sendPhoto'])
def send_photo(message):
    file = open('./liana.jpg', 'rb')
    bot.send_photo(message.chat.id, file, )
    msg = bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} (@{message.from_user.username})!")


@bot.message_handler(commands=['help'])
def main(message):
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Examples', callback_data='Show examples')
    btn2 = types.InlineKeyboardButton('Boo!', callback_data='scary_face')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, '<b>Command</b> info', parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Show examples':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'show_users':
        conn = sqlite3.connect('study.db')
        cur = conn.cursor()
        cur.execute('SELECT * from users;')
        users = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    
    for el in users:
        bot.send_message(callback.message.chat.id, f'Id: {el[0]} name: {el[1]} pass: {el[2]}')

# FILE DOWNLOADING-------------------------------
@bot.message_handler(commands=['photo3to5', 'instax', 'fullPhoto'])
def folderName(message):
    global file_path
    if message.text == '/photo3to5':
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\photo3to5'
    elif message.text == '/instax':
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\instax'
    elif message.text == '/fullPhoto':
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\fullPhoto'
    msg = bot.send_message(message.chat.id, 'Send your photo please')
    bot.register_next_step_handler(msg, handle_photos)

def handle_photos(message):
    file_info = None
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)  # Get the highest resolution photo
        file_id = message.photo[-1].file_id
        file_name = f"{file_id}_{message.from_user.username}.jpg"
    
    if file_info:
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        
        # Download the file
        response = requests.get(file_url)
        
        # Save the file locally
        with open(f'{file_path}\\{file_name}', 'wb') as file:
            file.write(response.content)
        
        bot.reply_to(message, f"File downloaded successfully: {file_name}")
    else:
        bot.reply_to(message, "Unsupported file type.")

@bot.message_handler(commands=['message'])
def show_message(message):
    bot.send_message(message.chat.id, message)

#Text handling
@bot.message_handler()
def info(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} (@{message.from_user.username})!")
    elif message.text.lower() == 'name':
        bot.reply_to(message, message.from_user.first_name)



bot.polling(non_stop=True)