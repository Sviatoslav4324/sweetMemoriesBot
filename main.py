import telebot
import requests
import sqlite3
from telebot import types


bot = telebot.TeleBot('7127901125:AAET69Nhu65t7IUsYfqWVc__XBrhOxEmSMY')

# /start - buttons + edit (done)
# /help ()
# /photo3to5 /instax /fullPhoto (done)
# /locations (done)
# /prices  (done)
# /examples (done)
# /print - buttons (done)
# /admin_help (done)
# /all_orders - show all orders
# /order - show orders from particular userID


class User:
    def __init__(self, name, username, userID, chatID):
        self.name = name
        self.username = username
        self.userID = userID
        self.chatID = chatID

cur_user = User(None, None, None, None)

class Order:
    def __init__(self, username, chatID, userID, format, image_name, status, print_number):
        self.username = username
        self.userID = userID
        self.chatID = chatID
        self.format = format
        self.image_name = image_name
        self.status = status
        self.print_number = print_number


def define_user(message):
    cur_user.name = message.from_user.first_name
    cur_user.username = message.from_user.username
    cur_user.userID = message.from_user.id
    cur_user.chatID = message.chat.id

@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect('mySweetMemories.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id int IDENTITY(1,1) primary key,
        name text(50),
        username text(100),
        userID int,
        chatID int
    );

    CREATE TABLE IF NOT EXISTS orders (
        id int auto_increment primary key,
        username text(100),
        chatID int,
        userID int,
        format text(50),
        image_name text(200),
        status text(150),
        print_number int
    );
                  
    CREATE TABLE IF NOT EXISTS admins (
        id int auto_increment primary key,
        name text(50),
        username text(100),
        userID int
    );
    ''')


    define_user(message)
    cur.execute("insert into users(name, username, userID, chatID) values('%s', '%s', '%d', '%d')" % (cur_user.name, cur_user.username, cur_user.userID, cur_user.chatID))
    
    conn.commit()
    cur.close()
    conn.close()
     
    markup = types.InlineKeyboardMarkup()
    examples_btn = types.InlineKeyboardButton('Show examples of formats', callback_data='show_examples')
    markup.row(examples_btn)
    bot.send_message(message.chat.id, f'''Hello!

I'm bot of "mySweetMemories" 🦾

I can help you with printing your photos.
Here are my basic commands:
/photo3to5 - print your photo at 3x5 format
/instax - print your photo in "instax" format
/fullPhoto - print your photo in 3:2 aspect ratio
/locations - list of our locations in NYC
/help - get a list of commands
/prices - pricelist of our print
/examples - show examples of how formats look like
/print - menu to choose your format

If you're ready to choose - press the button below👇👇👇''', reply_markup=markup)
    

@bot.message_handler(commands=['help'])
def main(message):
    define_user(message)
    bot.send_message(message.chat.id, '''      
💡What I can do:               
/photo3to5 - print your photo at 3x5 format
/instax - print your photo in "instax" format
/fullPhoto - print your photo in 3:2 aspect ratio
/locations - list of our locations in NYC
/prices - pricelist of our print
/examples - show examples of how formats look like
/print - menu to choose your format''')

@bot.message_handler(commands=['locations'])
def show_locations(message):
    define_user(message)
    markup = types.InlineKeyboardMarkup()
    maps_btn = types.InlineKeyboardButton('Open on Google Maps🌎', url='https://www.google.com/maps/place/%D0%9D%D1%8C%D1%8E-%D0%99%D0%BE%D1%80%D0%BA,+%D0%A1%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D1%96+%D0%A8%D1%82%D0%B0%D1%82%D0%B8+%D0%90%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B8/@40.7343958,-73.9900086,14.57z/data=!4m6!3m5!1s0x89c24fa5d33f083b:0xc80b8f06e177fe62!8m2!3d40.7127753!4d-74.0059728!16zL20vMDJfMjg2?authuser=0&entry=ttu')
    markup.row(maps_btn)
    bot.send_message(message.chat.id, '''Here you can find our locations📍

📌 140 E 14th St, New York
📌225 Park Ave S, New York
📌175 8th Ave, New York''', reply_markup=markup)

@bot.message_handler(commands=['prices'])
def show_prices(message):
    define_user(message)
    bot.send_message(message.chat.id, '''PriceLIST💰

💸Instax - 5$(x1), 10$(x3), 30$(x10)
💸3:5 - 8$(x1), 18$(x3), 65$(x10)
💸3:2 - 8$(x1), 20$(x3), 65$(x10)''')


@bot.message_handler(commands=['examples'])
def show_examples(message):
    define_user(message)
    f_instax = open('./images/examples/instax.jpg', 'rb')
    bot.send_photo(message.chat.id, f_instax)
    bot.send_message(message.chat.id, 'Instax format')

    f_3to5 = open('./images/examples/3to5.jpg', 'rb')
    bot.send_photo(message.chat.id, f_3to5)
    bot.send_message(message.chat.id, '3x5 format')

    f_fullPhoto = open('./images/examples/fullPhoto.jpg', 'rb')
    bot.send_photo(message.chat.id, f_fullPhoto)
    bot.send_message(message.chat.id, 'Full photo format')
    user_print(message)

# Photo DOWNLOADING------------------------------------------------------------
@bot.message_handler(commands=['photo3to5', 'instax', 'fullPhoto'])
def folderName(message):
    global file_path
    global photo_format
    if message.text == '/photo3to5':
        photo_format = 'photo3to5'
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\photo3to5'
    elif message.text == '/instax':
        photo_format = 'instax'
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\instax'
    elif message.text == '/fullPhoto':
        photo_format = 'fullPhoto'
        file_path =  'C:\\Users\\Admin\\Desktop\\bot\\fullPhoto'
    msg = bot.send_message(message.chat.id, 'Send your photo please')
    bot.register_next_step_handler(msg, handle_photos)

def handle_photos(message):
    define_user(message) # цю функцію поставив в handle_photos,  а не folderName, бо в folderName message - йде від бота.
    if message.photo:
        global file_info, file_id, file_name, username, chat_id
        file_info = bot.get_file(message.photo[-1].file_id)  # Get the highest resolution photo
        file_id = message.photo[-1].file_id
        file_name = f"{file_id}_{message.from_user.username}.jpg"
        
        username = message.from_user.username
        chat_id = message.chat.id


        if file_info:
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
            
            # Download the file
            response = requests.get(file_url)
            
            # Save the file locally
            with open(f'{file_path}\\{file_name}', 'wb') as file:
                file.write(response.content)
            
            msg = bot.reply_to(message, '❗️Now, please send number of photos to be printed.')
            bot.register_next_step_handler(msg, db_load)
    else:
        bot.reply_to(message, "Unsupported file type.")


def db_load(message):
        conn = sqlite3.connect('mySweetMemories.sqlite')
        cur = conn.cursor()
        global print_num
        try:
            print_num = int(message.text)            
        except:
            bot.reply_to(message, "⛔️An error occured. Please try again. Send only integer number")
            return
        
        global cur_order
        cur_order = Order(cur_user.username, cur_user.chatID, cur_user.userID, photo_format, file_name, 'undone', print_num)
        cur.execute("insert into orders(username, chatID, userID, format, image_name, status, print_number) values('%s', '%d', '%d', '%s', '%s', '%s', '%d')" % (cur_user.username, cur_user.chatID, cur_user.userID, photo_format, file_name, 'undone', print_num))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "Thanks! Your order is checking.")


@bot.message_handler(commands=['print'])
def user_print(message):
    define_user(message)
    markup = types.InlineKeyboardMarkup()
    instax_btn = types.InlineKeyboardButton('Instax', callback_data='instax')
    fullPhoto_btn = types.InlineKeyboardButton('Full photo (3:2)', callback_data='fullPhoto')
    btn_3to5 = types.InlineKeyboardButton('3:5', callback_data='3to5')
    markup.row(instax_btn, fullPhoto_btn)
    markup.row(btn_3to5)

    bot.send_message(message.chat.id, 'Ready to choose?', reply_markup=markup)



# BUTTONS callbacks -----------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'show_examples':
        f_instax = open('./images/examples/instax.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, f_instax)
        bot.send_message(callback.message.chat.id, 'Instax format')

        f_3to5 = open('./images/examples/3to5.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, f_3to5)
        bot.send_message(callback.message.chat.id, '3x5 format')

        f_fullPhoto = open('./images/examples/fullPhoto.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, f_fullPhoto)
        bot.send_message(callback.message.chat.id, 'Full photo format')

        user_print(callback.message)

    elif callback.data == 'instax':
        callback.message.text = '/instax'
        folderName(callback.message)

    elif callback.data == 'fullPhoto':
        callback.message.text = '/fullPhoto'
        folderName(callback.message)  

    elif callback.data == '3to5':
        callback.message.text = '/photo3to5'
        folderName(callback.message)   



# ADMIN --------------------------------------------------------------------------------------------
admin_access = False
def get_access(message):
    define_user(message)
    
    global admin_access        
    admin_access = False
    conn = sqlite3.connect('mySweetMemories.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT * from admins')
    admins = cur.fetchall() # індекс 2 в підмасиві - username

    cur.close()
    conn.close()

    for admin in admins:
        if admin[3] == message.from_user.id:
            admin_access = True
    if admin_access:
        print('Admin success!')
    else:
        print('Admin no success.')


@bot.message_handler(commands=['admin_help'])
def admin_commands(message):
    get_access(message)
    if admin_access:
        bot.send_message(message.chat.id, '''Here are your admin's commands:
/all_orders - show all orders
/order - show orders from particular userID''')
    else:
        bot.send_message(message.chat.id, "You're not allowed to use this command.")
    
@bot.message_handler(commands=['all_orders'])
def show_orders(message):
    get_access(message)
    if admin_access:
        conn = sqlite3.connect('mySweetMemories.sqlite')
        cur = conn.cursor()

        cur.execute("select * from orders where orders.status = 'undone'")
        undone_orders = cur.fetchall()

        cur.close()
        conn.close()
        if len(undone_orders) > 0:
            for order in undone_orders:
                bot.send_message(message.chat.id, f"<b>Username:</b> @{order[1]} <b>chatID:</b> {order[2]}\n<b>userID:</b> {order[3]} \n<b>Photo format:</b> {order[4]} \n<b>Image:</b> {order[5]} \n\n<b>Order status:</b> {order[6]}\n<b>Print number:{order[7]}</b> ", parse_mode='html')
        else:
            bot.send_message(message.chat.id, "The list is empty! There are no orders yet :(")
    else:
        bot.send_message(message.chat.id, "You're not allowed to use this command.")


@bot.message_handler(commands=['order'])
def get_userID(message):
    get_access(message)
    if admin_access:
        msg = bot.send_message(message.chat.id, "Send userID of which you want to see orders.")
        bot.register_next_step_handler(msg, show_orders)
    else:
        bot.send_message(message.chat.id, "You're not allowed to use this command.")

def show_orders(message):
    if admin_access:
        conn = sqlite3.connect('mySweetMemories.sqlite')
        cur = conn.cursor()

        cur.execute("select * from orders where orders.userID = %d" % int(message.text))
        user_orders = cur.fetchall()

        cur.close()
        conn.close()
        if len(user_orders) > 0:
            for order in user_orders:
                bot.send_message(message.chat.id, f"<b>Username:</b> @{order[1]} <b>chatID:</b> {order[2]}\n<b>userID:</b> {order[3]} \n<b>Photo format:</b> {order[4]} \n<b>Image:</b> {order[5]} \n\n<b>Order status:</b> {order[6]}\n<b>Print number:{order[7]}</b>\n<b>Photo below</b>", parse_mode='html')
                global file_path
                if order[4] == 'photo3to5':
                    file_path =  'C:\\Users\\Admin\\Desktop\\bot\\photo3to5'
                elif order[4] == 'instax':
                    file_path =  'C:\\Users\\Admin\\Desktop\\bot\\instax'
                elif order[4] == 'fullPhoto':
                    file_path =  'C:\\Users\\Admin\\Desktop\\bot\\fullPhoto'

                try:   
                    user_photo = open(f'{file_path}\\{order[5]}', 'rb')
                    bot.send_photo(message.chat.id, user_photo)
                except:
                    bot.send_message(message.chat.id, "Sorry! Cannot load image.")
        else:
            bot.send_message(message.chat.id, "The list is empty! There are no orders of such userID :(")
    else:
        bot.send_message(message.chat.id, "You're not allowed to use this command.")



bot.polling(non_stop=True)