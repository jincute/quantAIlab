import time,datetime
import telepot
from telepot.loop import MessageLoop

now = datetime.datetime.now()

# def action(msg):
#     chat_id = msg['chat']['id']
#     command = msg['text']
#     print('Received: %s' % command)
    
telegram_bot = telepot.Bot('1690062356:AAFFxkzkjW4dPOBKSuxq8BY5Bwepzp2zDao')
# print(telegram_bot.getMe())

test_text = 'trial msg'
telegram_bot.sendMessage('351230752',test_text) #chat_id