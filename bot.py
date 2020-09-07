from telebot import TeleBot
from modules.currency import CurrencyBot
from modules.database import DataBase
from modules.telegram_bot import Bot

TOKEN = 'telegram_bot_token'
    
tgbot = TeleBot(TOKEN)
currency_bot = CurrencyBot()


@tgbot.message_handler(content_types=['sticker', 'file', 'photo', 'video', 'audio'])
def send_u_menu(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.send_main_menu()


@tgbot.message_handler(commands=['user'])
def send_u_menu(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.send_main_menu()


@tgbot.message_handler(commands=['operator'])
def send_operator_menu(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.send_o_menu()


@tgbot.message_handler(commands=['admin'])
def send_admin_menu(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.send_a_menu()


@tgbot.message_handler(commands=['addadmin'])
def add_new_admin(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.add_new_admin()


@tgbot.message_handler(commands=['addoper'])
def add_new_operator(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.add_new_operator()


@tgbot.message_handler(commands=['deloper'])
def delete_operator(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.delete_operator()


@tgbot.message_handler(commands=['deladmin'])
def delete_admin(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.delete_admin()


@tgbot.message_handler(commands=['start'])
def start_menu(msg):
    bot = Bot(tgbot, msg, currency_bot, database=DataBase())
    bot.database = DataBase()
    bot.send_start()


@tgbot.message_handler(content_types=['text'])
def msg_analyzer(msg):
    bot = Bot(tgbot, msg=msg, curr_bot=currency_bot, database=DataBase())
    print(bot.user.trade_request, 'found trade')
    print(bot.user.help_request, 'found help')
    print(bot.user.replenish_request, 'found replenish')
    print(bot.user.service_request, 'found service')
    print(bot.user.return_request, 'found return')
    bot.message_processor()


@tgbot.callback_query_handler(func=lambda call: True)
def buttons_stuff(call):
    bot = Bot(tgbot, currency_bot, call=call, database=DataBase())
    bot.database = DataBase()

    print('calldata:', bot.call_parser.data)
    print(bot.user.trade_request, 'found trade (buttons)')
    print(bot.user.help_request, 'found help (buttons)')
    print(bot.user.replenish_request, 'found replenish (buttons)')
    print(bot.user.service_request, 'found service (buttons)')
    print(bot.user.return_request, 'found return (buttons)')
    if bot.user.is_admin or bot.user.is_operator:
        bot.operator_call_data_handler()
    bot.user_call_data_handler()


@tgbot.channel_post_handler(content_types=['text'])
def get_channel_id(msg):
    chat_id = msg.chat.id
    print(chat_id)


if __name__ == "__main__":
    try:
        tgbot.polling()
    except Exception as er:
        print(er)
        tgbot.send_message(231584958,
                           text=er)
