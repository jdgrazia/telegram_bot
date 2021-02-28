  
#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

import csv
import os.path


API_TOKEN = '1698815983:AAGNd-4pLqLw35cL8dJH-3CQLl520KhqAi4'

bot = telebot.TeleBot(API_TOKEN)
grouplist = []
userlist = []
botlist = []

def send_to_grouplist(message):
    for group in grouplist:
        bot.send_message(group,message)

def send_to_userlist(message):
    for user in userlist:
        bot.send_message(user, message)

def send_to_all(message):
    send_to_grouplist(message)
    send_to_userlist(message)

    
def write_id(id, type):
    with open("id.csv", "r") as fp:
        rd = csv.reader(fp, delimiter=",")
        for row in rd:
            if id == row[1]:
                return
    if type == 'group':
        global grouplist
        grouplist.append(id)
        idlist = ['groupid',id]
    if type == 'bot':
        botlist.append(id)
        idlist = ['botid', id]
    if type == 'userid':
        userlist.append(id)
        idlist = ['userid:', id]
    with open("id.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(idlist)

def read_ids():
    fname = "id.csv"
    if not os.path.isfile(fname):
        return

    
    with open("id.csv","r") as fp:
        rd = csv.reader(fp, delimeter=",")
        for row in rd:
            if(row[0] == "groupid"):
                global grouplist
                grouplist.append(row[1])
            if(row[0] == "userid"):
                global userlist
                userlist.append(row[1])
            if(row[0] == "bitid"):
                global botlist
                botlist.append(row[1])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

# Handle '/start' and '/help'
@bot.message_handler(commands=['setgroup'])
def set_group(message):
    bot.send_message(message.chat.id, 'ok this is where ill send shit')
    write_id(message.chat.id,"groupid")
 
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.from_user.is_bot == True:
        bot.send_message(message.chat.id, '/start')
        write_id(message.chat.id,"botid")
        send_to_grouplist("a bot tried to touch my nono parts")
    else:
        bot.send_message(message.chat.id, 'hello human')
    send_to_grouplist(message)
    print(message)

read_ids()

bot.polling()