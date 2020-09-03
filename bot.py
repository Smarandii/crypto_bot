from telebot import TeleBot
from buttons import *
from content import BotContent, TOKEN
from currency import *
from models import *
from database import *
from functions import *
from datetime import datetime


class Bot:
    def __init__(self, telebot, msg=None, curr_bot=None, call=None):
        self.tgbot = telebot
        if msg is not None:
            self.user = self.add_new_user(msg)
        else:
            self.user = self.add_new_user(call=call)
        self.user.pull_requests(self.database.get_requests(self.user))
        self.user_menu = UserMenu()
        self.operator_menu = OperatorMenu()
        self.admin_menu = AdminMenu()
        self.crypto_menu = CryptoMenu()
        self.personal_menu = PersonalMenu()
        self.currency_bot = curr_bot
        self.message_parser = MessageParser(msg)
        self.call_parser = CallParser(call)
        self.content = BotContent()
        self.database = None
        self.operators = get_operators_list()

    def return_is_possible(self, return_value):
        return float(self.user.balance) > return_value and self.return_value_is_acceptable(return_value)

    def get_balance_available_for_return(self):
        return self.user.balance * self.content.RETURN_PERCENT

    def return_value_is_acceptable(self, return_value) -> bool:
        return self.content.MIN_VALUE_FOR_RETURN <= return_value <= self.content.MAX_VALUE_FOR_RETURN

    def get_last_cur_update(self):
        return self.currency_bot.last_cur_update

    def send_request_to_operators(self, text, request):
        # TODO
        rq_id = request[0]
        if 'help_request' not in request[3]:
            operator_buttons = keyboard_maker(2, ['Пользователь оплатил', 'Пользователь не оплатил'],
                                              [f'confirm {rq_id}', f'cancel {rq_id}'])

        else:
            operator_buttons = keyboard_maker(2, ['Ответить на вопрос', 'Удалить вопрос'],
                                              [f'answer {rq_id}', f'cancel_question {rq_id}'])
        for operator in self.operators:
            self.tgbot.send_message(operator, text=text,
                                    reply_markup=operator_buttons)

    def show_all_requests_to_operators(self, requests):
        for request in requests:
            text = get_request_text(request)
            self.send_request_to_operators(text=text, request=request)

    def check_user_is_follower(self, user_id):
        # group_status = tgbot.get_chat_member(chat_id=GROUP, user_id=user_id)
        # channel = tgbot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        # if "'status': 'left'" in str(group_status):
        #     if "'status': 'left'" in str(channel):
        #         return 0
        return 1

    def add_new_help_request(self):
        request = (self.user.telegram_id, 'H: wait_for_question',
                   'help_request', str(datetime.now()), 'None', 'None')
        self.database.add_request_to_db(request)

    def add_new_trade_request(self, key=None, curr_price=None):
        request = (self.user.telegram_id,
                   "T: wait for trade value",  # status
                   f'trade {key} {curr_price}',  # type
                   str(datetime.now()),  # when created
                   'None',  # comment
                   'None')  # wallet
        self.database.add_request_to_db(request)

    def add_new_service_request(self, status):
        request = (self.user.telegram_id,
                   status,  # status
                   'service_request',   # type
                   str(datetime.now()),  # when created
                   'None',  # comment
                   'None')  # wallet
        self.database.add_request_to_db(request)

    def add_new_user(self, user_message=None, call=None):
        if call is None:
            user_id = user_message.chat.id
            follow_status = self.check_user_is_follower(user_id)
            invited_by = self.message_parser.get_invitation(user_message)
            user = self.database.add_new_user_to_db(user_id, follow_status, invited_by)
            return user
        else:
            user_id = call.from_user.telegram_id
            return self.database.get_user_by_telegram_id(user_id)

    def add_new_admin(self,):
        if " " in self.message_parser.user_message.text and self.user.is_admin:
            admin_id = self.message_parser.get_command_value()
            add_admin(admin_id)
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['new_admin'])

    def add_new_operator(self):
        if " " in self.message_parser.user_message.text and self.user.is_admin:
            command, operator_id = self.message_parser.get_command_value()
            add_operator(operator_id)
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['new_operator'])

    def delete_operator(self):
        if " " in self.message_parser.user_message.text and self.user.is_admin:
            command, operator_id = self.message_parser.get_command_value()
            delete_operator(operator_id)
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['delete_operator'])

    def delete_admin(self):
        if " " in self.message_parser.user_message.text and self.user.is_admin:
            command, admin_id = self.message_parser.get_command_value()
            delete_admin(admin_id)
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['delete_admin'])

    def send_main_menu(self):
        markup = self.user_menu.get_menu_markup()
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['menu_arrow'],
                                reply_markup=markup)

    def send_o_menu(self):
        if self.user.is_operator:
            markup = self.operator_menu.get_menu_markup()
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['menu_arrow'], reply_markup=markup)

    def send_a_menu(self):
        if self.user.is_admin:
            markup = self.admin_menu.get_menu_markup()
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['menu_arrow'], reply_markup=markup)

    def send_start(self):
        if self.user.is_follower:
            markup = self.user_menu.get_menu_markup()
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['menu_arrow'], reply_markup=markup)
        else:
            markup = self.user_menu.suggestion_menu()
            self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['channel_suggest'], reply_markup=markup)
            markup = self.user_menu.get_menu_markup()
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['menu_arrow'], reply_markup=markup)

    def send_buy_crypto(self):
        markup = self.crypto_menu.get_menu_markup()
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['choose_crypto'], reply_markup=markup)

    def send_partnership(self):
        text = self.database.get_partnership_text(self.user)
        self.tgbot.send_message(self.user.telegram_id, text=text)

    def send_help(self):
        # TODO
        request = self.database.get_request_by_telegram_id(self.user.telegram_id, rq_type='help_request')
        if request is not None:
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                                    text='Вы уже оставили нам вопрос, желаете его удалить?',
                                    reply_markup=SHOW_OR_CANCEL_HELP_ORDER)
        else:
            self.add_new_help_request()
            self.tgbot.send_message(self.user.telegram_id,
                                    text="Задайте ваш вопрос прямо в чат с ботом, мы ответим как-только сможем!", )

    def send_personal_cabinet(self):
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['personal_cabinet'], reply_markup=self.personal_menu.get_menu_markup())

    def send_replenish_balance(self):
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['replenish_balance'].format(self.user.balance),
                                reply_markup=REPLENISH_BALANCE)

    def send_current_balance(self):
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['current_balance'].format(self.user.status, self.user.balance),
                                reply_markup=RETURN_MONEY)

    def send_start_trade_rq(self, key):
        curr_price = self.currency_bot.get_curr_by_key(key)
        if self.user.trade_request is not None and self.user.trade_request.status != 'user_confirmed':
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                                    text=self.content.MESSAGES['request_exist_warning'],
                                    reply_markup=SHOW_OR_CANCEL_TRADE_ORDER)
        else:
            # TODO ввод в рублях или в выбранной валюте
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                                    text=self.content.MESSAGES['start_trade_rq'].format(self.content.EXAMPLE[key], key),
                                    reply_markup=CANCEL_ORDER)
            self.add_new_trade_request(key, curr_price)

    def send_raw_requests(self):
        requests = self.database.get_all_requests()
        self.show_all_requests_to_operators(requests)
        if not requests:
            tgbot.send_message(self.user.telegram_id,
                               text='Заявки не найдены.')

    def send_replenish_user_balance(self):
        self.add_new_service_request('S: wait_for_user_replenish')
        tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_replenish'])

    def send_unreplenish_user_balance(self):
        self.add_new_service_request('S: wait_for_user_unreplenish')
        tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_replenish'])

    def send_message_to_user(self):
        self.add_new_service_request('S: wait_for_msg')
        tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_replenish'])

    def send_addoper(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /addoper")

    def send_addadmin(self):
        tgbot.send_message(self.user.telegram_id, text="Используй команду /addadmin")

    def send_deloper(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /deloper")

    def send_deladmin(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /deladmin")

    def send_return_impossible_message(self):
        self.tgbot.send_message(
            text=self.content.MESSAGES['return_failure'].format(self.get_balance_available_for_return(),
                                                                self.content.MIN_VALUE_FOR_RETURN,
                                                                self.content.MAX_VALUE_FOR_RETURN),
            chat_id=self.user.telegram_id)
        self.database.delete_request_from_db(self.user.return_request.db_id)

    def send_return_possible_message(self, return_value):
        self.user.return_request.comment = f"Вывод {return_value}"
        self.database.update_request_in_db(self.user.return_request)
        choose_return_keyboard = keyboard_maker(2, ['Сбербанк', 'QIWI'],
                                                [f'return_sber {self.user.return_request.db_id}',
                                                 f'return_qiwi {self.user.return_request.db_id}'])
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['where_return'],
                                reply_markup=choose_return_keyboard)

    def confirm_return_requisites(self):
        user_requisites = self.message_parser.user_message
        self.user.return_request.wallet = user_requisites
        self.database.update_request_in_db(self.user.return_request)
        tgbot.send_message(self.user.telegram_id,
                           text=self.content.MESSAGES['confirm_requisites'].format(user_requisites),
                           reply_markup=REQUISITES_CONFIRM_KEYBOARD)

    def return_request_processing(self):
        if self.user.return_request.type == "R: wait for return value":
            return_value = self.message_parser.get_value_from_message()
            if self.return_is_possible(return_value):
                self.send_return_possible_message(return_value)
            else:
                self.send_return_impossible_message()
        if self.user.return_request == "R: wait for return requisites":
            self.confirm_return_requisites()
        self.database.update_request_in_db(self.user.return_request)

    def send_confirm_answer_message(self):
        answer = self.message_parser.user_message
        send_msg_to_user = keyboard_maker(2,
                                          ['Да',
                                           'Нет, ввести заново'],
                                          [f'sendanswer {self.user.service_request.telegram_id} {answer}',
                                           f'answer']
                                          )
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['confirm_send_answer'].format(answer),
                                reply_markup=send_msg_to_user)

    def send_confirm_direct_message(self):
        client_id, message = self.message_parser.get_receiver_id_and_message()
        send_msg_to_user = one_button_keyboard("Подтвердить", f'send_msg:{client_id}:{message}')
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['confirm_send_message'],
                                reply_markup=send_msg_to_user)

    def send_confirm_user_balance_replenish(self):
        client_id, amount = self.message_parser.user_message.text.split(" ")
        replenish_user_balance = one_button_keyboard("Подтвердить",
                                                     f'replenish_user_balance {client_id} {amount}')
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['confirm_user_balance_replenish'].format(client_id, amount),
                                reply_markup=replenish_user_balance)

    def send_confirm_user_balance_unreplenish(self):
        client_id, amount = self.message_parser.user_message.text.split(" ")
        unreplenish_user_balance = one_button_keyboard("Подтвердить",
                                                       f'unreplenish_user_balance {client_id} {amount}')
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['confirm_user_balance_unreplenish'].format(client_id, amount),
                                reply_markup=unreplenish_user_balance)

    def service_request_processing(self):
        if self.user.service_request.status == "S: wait_for_answer":
            self.send_confirm_answer_message()
        if self.user.service_request.status == "S: wait_for_msg":
            self.send_confirm_direct_message()
        if self.user.service_request.status == "S: wait_for_user_replenish":
            self.send_confirm_user_balance_replenish()
        if self.user.service_request.status == "S: wait_for_user_unreplenish":
            self.send_confirm_user_balance_unreplenish()
        self.database.update_request_in_db(self.user.service_request)

    def send_confirm_user_question(self):
        question = self.message_parser.user_message
        self.user.help_request.status = 'H: user_wait_for_response'
        self.user.help_request.comment = question
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['confirm_user_question'],
                                reply_markup=CANCEL_HELP_RQ)

    def help_request_processing(self):
        if self.user.help_request.status == 'H: wait_for_question':
            self.send_confirm_user_question()
        self.database.update_request_in_db(self.user.help_request)

    def send_confirm_user_replenish(self):
        replenish_value = self.message_parser.get_value_from_message()
        if self.message_parser.replenish_value_is_acceptable():
            self.user.replenish_request.type = f'replenish {replenish_value}'
            self.user.replenish_request.comment = f"Пополнение баланса на сумму: {replenish_value} ₽"
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['confirm_user_replenish'].format('replenish_value'),
                                    reply_markup=REPLENISH_CONFIRM_KEYBOARD)

        else:
            self.send_unacceptable_value_message()

    def send_replenish_methods(self):
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['choose_payment_method'],
                                reply_markup=REPLENISH_METHODS)

    def replenish_request_processing(self):
        if self.user.replenish_request.status == "B: wait for replenish value":
            self.send_confirm_user_replenish()
        elif self.user.replenish_request.status == "B: waiting_for_purchase":
            self.send_replenish_methods()
        self.database.update_request_in_db(self.user.replenish_request)

    def send_promotion(self):
        self.tgbot.send_message(self.user,
                                self.content.MESSAGES['promotion_message'].format(self.user.quantity_of_trades + 1))

    def send_trade_request_prepayment_message(self, key, curr_price):
        trade_value = self.message_parser.get_value_from_message()
        user_price, user_curr, promotion = self.content.get_user_price(curr_price, self.user, trade_value, key)
        if promotion is not None:
            self.send_promotion()
        message = self.content.get_prepayment_message(user_curr, trade_value, user_price, key)
        tgbot.send_message(self.user.telegram_id, text=message, reply_markup=CANCEL_ORDER)
        self.user.trade_request.status = 'T: waiting_for_usr_wallet'
        self.user.trade_request.comment = f"Покупка {trade_value} {key}, К оплате: {user_price}"
        self.user.trade_request.type = f'trade {trade_value} {key} {user_curr}'

    def send_unacceptable_value_message(self):
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['unacceptable_value'])

    def send_trade_wallet_confirm(self, user_wallet):
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['confirm_user_wallet'].format(user_wallet),
                                reply_markup=WALLET_CONFIRM_KEYBOARD)
        self.user.trade_request.wallet = user_wallet

    def send_unacceptable_wallet_message(self):
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['unacceptable_wallet'])

    def send_choose_commission_message(self):
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['choose_commission'],
                                reply_markup=REQUEST_PRIORITIES)

    def send_payment_methods(self):
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['choose_payment_method'],
                                reply_markup=PAYMENT_METHODS)

    def trade_request_processing(self):
        if self.user.trade_request.status == "T: wait for trade value":
            key, curr_price = self.user.trade_request.get_key_and_curr_price_from_rq()
            if self.message_parser.trade_value_is_acceptable(key):
                self.send_trade_request_prepayment_message(key, curr_price)
            else:
                self.send_unacceptable_value_message()
        elif self.user.trade_request.status == "T: waiting_for_usr_wallet":
            user_wallet = self.message_parser.user_message
            if self.currency_bot.check_adress(user_wallet):
                self.send_trade_wallet_confirm(user_wallet)
            else:
                self.send_unacceptable_wallet_message()
        elif self.user.trade_request.status == "T: waiting_for_priority":
            self.send_choose_commission_message()
        elif self.user.trade_request.status == "T: waiting_for_purchase":
            self.send_payment_methods()
        self.database.update_request_in_db(self.user.trade_request)

    def send_message_from_operator(self):
        call_data, client_id, message = self.call_parser.call.data.split(':')
        self.tgbot.send_message(client_id,
                                self.content.MESSAGES['message_from_operator_notification'].format(message))
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['message_sent_notification'])
        self.database.delete_request_from_db(self.user.service_request.db_id)

    def send_status_from_operator(self):
        client_id, message = self.database.get_status_message(self.call_parser.call)
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['message_sent_notification'])
        self.tgbot.send_message(client_id, text=message)

    def send_answer_from_operator(self):
        call_data, client_id, answer = self.call_parser.call.data.split(' ')
        client_request = self.database.get_request_by_telegram_id(client_id, rq_type='help_request')
        self.tgbot.send_message(client_id,
                                self.content.MESSAGES['question_answered_notification'].format(answer))
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['message_sent_notification'])
        self.database.delete_request_from_db(client_request.db_id)
        self.database.delete_request_from_db(self.user.service_request.db_id)

    def send_wait_for_operator_answer(self):
        self.add_new_service_request('S: wait_for_answer')
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['wait_for_operator_answer'])


tgbot = TeleBot(TOKEN)
currency_bot = CurrencyBot()


@tgbot.message_handler(content_types=['sticker', 'file', 'photo', 'video', 'audio'])
def send_u_menu(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.send_main_menu()


@tgbot.message_handler(commands=['user'])
def send_u_menu(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.send_main_menu()


@tgbot.message_handler(commands=['operator'])
def send_operator_menu(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.send_o_menu()


@tgbot.message_handler(commands=['admin'])
def send_admin_menu(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.send_a_menu()


@tgbot.message_handler(commands=['addadmin'])
def add_new_admin(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.add_new_admin()


@tgbot.message_handler(commands=['addoper'])
def add_new_operator(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.add_new_operator()


@tgbot.message_handler(commands=['deloper'])
def delete_operator(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.delete_operator()


@tgbot.message_handler(commands=['deladmin'])
def delete_admin(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.delete_admin()


@tgbot.message_handler(commands=['start'])
def start_menu(msg):
    bot = Bot(tgbot, msg, currency_bot)
    bot.database = DataBase()
    bot.send_start()


@tgbot.message_handler(content_types=['text'])
def msg_analyzer(msg):
    bot = Bot(tgbot, msg=msg, curr_bot=currency_bot)
    bot.database = DataBase()

    print(bot.user.trade_request, 'found trade')
    print(bot.user.help_request, 'found help')
    print(bot.user.replenish_request, 'found replenish')
    print(bot.user.service_request, 'found service')
    print(bot.user.return_request, 'found return')

    if bot.user_menu.sent_by_menu(msg.text):
        # User menu
        if bot.user_menu.MENU_BUTTONS['buy'] in msg.text:
            bot.send_buy_crypto()

        elif bot.user_menu.MENU_BUTTONS['partnership'] in msg.text:
            bot.send_partnership()

        elif bot.user_menu.MENU_BUTTONS['help'] in msg.text:
            bot.send_help()

        elif bot.user_menu.MENU_BUTTONS['personal_cabinet'] in msg.text:
            bot.send_personal_cabinet()
        return True

    elif bot.personal_menu.sent_by_menu(msg.text):
        # Personal Menu
        if bot.personal_menu.MENU_BUTTONS['replenish'] in msg.text:
            bot.send_replenish_balance()

        elif bot.personal_menu.MENU_BUTTONS['show_balance'] in msg.text:
            bot.send_current_balance()

        elif bot.personal_menu.MENU_BUTTONS['main_menu'] in msg.text:
            bot.send_main_menu()
        return True

    elif bot.crypto_menu.sent_by_menu(msg.text):
        # Get Crypto menu
        if bot.crypto_menu.MENU_BUTTONS['btc'] in msg.text:
            key = 'Bitcoin'
            bot.send_start_trade_rq(key)

        elif bot.crypto_menu.MENU_BUTTONS['ltc'] in msg.text:
            key = "LiteCoin"
            bot.send_start_trade_rq(key)

        elif bot.crypto_menu.MENU_BUTTONS['exmo'] in msg.text:
            key = "ExmoRUB"
            bot.send_start_trade_rq(key)

        elif bot.crypto_menu.MENU_BUTTONS['eth'] in msg.text:
            key = "Ethereum"
            bot.send_start_trade_rq(key)

        elif bot.crypto_menu.MENU_BUTTONS['bch'] in msg.text:
            key = "Bitcoin Cash"
            bot.send_start_trade_rq(key)

        elif bot.crypto_menu.MENU_BUTTONS['main_menu'] in msg.text:
            bot.send_main_menu()
        return True

    elif bot.operator_menu.sent_by_menu(msg.text) and bot.user.is_admin or bot.user.is_operator:
        # Operator menu
        if bot.operator_menu.MENU_BUTTONS['show_n_a_requests'] in msg.text:
            bot.send_raw_requests()

        elif bot.operator_menu.MENU_BUTTONS['replenish_user'] in msg.text:
            bot.send_replenish_user_balance()

        elif bot.operator_menu.MENU_BUTTONS['cut_user_balance'] in msg.text:
            bot.send_unreplenish_user_balance()

        elif bot.operator_menu.MENU_BUTTONS['send_message_to_user'] in msg.text:
            bot.send_message_to_user()

        elif bot.operator_menu.MENU_BUTTONS['main_menu'] in msg.text:
            bot.send_main_menu()

    elif bot.admin_menu.sent_by_menu(msg.text) and bot.user.is_admin:
        if bot.admin_menu.MENU_BUTTONS['addoper'] in msg.text:
            bot.send_addoper()
        elif bot.admin_menu.MENU_BUTTONS['addadmin'] in msg.text:
            bot.send_addadmin()
        elif bot.admin_menu.MENU_BUTTONS['deloper'] in msg.text:
            bot.send_deloper()
        elif bot.admin_menu.MENU_BUTTONS['deladmin'] in msg.text:
            bot.send_deladmin()
        return True

    else:
        if bot.user.all_requests_is_none():
            bot.send_main_menu()
            return True
        elif bot.user.return_request is not None:
            bot.return_request_processing()
            return True
        elif bot.user.service_request is not None:
            bot.service_request_processing()
            return True
        elif bot.user.help_request is not None:
            bot.help_request_processing()
            return True
        elif bot.user.replenish_request is not None:
            bot.replenish_request_processing()
            return True
        elif bot.user.trade_request is not None:
            bot.trade_request_processing()


@tgbot.callback_query_handler(func=lambda call: True)
def buttons_stuff(call):
    bot = Bot(tgbot, currency_bot, call=call)
    bot.database = DataBase()

    print('calldata: ', call.data)
    print(bot.user.trade_request, 'found trade (buttons)')
    print(bot.user.help_request, 'found help (buttons)')
    print(bot.user.replenish_request, 'found replenish (buttons)')
    print(bot.user.service_request, 'found service (buttons)')
    print(bot.user.return_request, 'found return (buttons)')

    if bot.user.is_admin or bot.user.is_operator:
        if 'send_msg' in call.data:
            bot.send_message_from_operator()
            return True
        elif 'send_status' in call.data:
            bot.send_status_from_operator()
            return True
        elif 'sendanswer' in call.data:
            bot.send_answer_from_operator()
            return True
        elif 'answer' in call.data:
            bot.send_wait_for_operator_answer()
            return True
        elif 'cancel_question' in call.data:
            call_data, rq_id = call.data.split(" ")
            request = get_request_by_id(c, int(rq_id))
            if get_request_by_id(c, rq_id) is not None:
                delete_request_from_db(c, request_id=request[0])
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Вопрос был удалён!')
            else:
                tgbot.send_message(chat_id=user_id,
                                   text="✅ Этот вопрос уже удалён")
            return True
        elif 'cancel ' in call.data:
            call_data, rq_id = call.data.split(" ")
            request = get_request_by_id(c, int(rq_id))
            if request is not None:
                send_msg_to_user = keyboard_maker(3, ['Отправил недостаточно средств', 'Вообще не совершил платёж',
                                                      'Закрыть заявку'],
                                                  [f'send_status {request[0]} {request[1]} not_enough',
                                                   f'send_status {request[0]} {request[1]} no_payment',
                                                   f'send_status {request[0]} {request[1]} close_request']
                                                  )
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Заявка была отменена!\nОтправить сообщение пользователю:',
                                   reply_markup=send_msg_to_user)
            else:
                tgbot.send_message(chat_id=user_id,
                                   text="✅ Эта заявка уже была обработанна!")
            return True
        elif 'confirm ' in call.data:
            call_data, rq_id = call.data.split(" ")
            print(rq_id)
            request = get_request_by_id(c, int(rq_id))
            raise_users_q_of_trades(c, request[1])
            if request is not None:
                send_msg_to_user = keyboard_maker(4, ['Подтвердить перевод',
                                                      'Пользователю отправили криптовалюту',
                                                      'Пополнить баланс пользователю',
                                                      'Закрыть заявку'],
                                                  [f'send_status {request[0]} {request[1]} payment_s',
                                                   f'send_status {request[0]} {request[1]} crypto_sent',
                                                   f'send_status {request[0]} {request[1]} replenish_s',
                                                   f'cancel {rq_id}']
                                                  )
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Отправить сообщение пользователю:',
                                   reply_markup=send_msg_to_user)
            else:
                tgbot.send_message(chat_id=user_id,
                                   text="✅ Эта заявка уже была обработанна!")
            return True
        elif 'unreplenish_user_balance' in call.data:
            call_data, client_id, amount = call.data.split(" ")
            if user_in_db(c, client_id):
                if bot.database.take_money_from_user_balance(c, client_id):
                    tgbot.send_message(user_id,
                                       text='Деньги списаны')
                    tgbot.send_message(client_id,
                                       text=f'С вашего счёта списали {amount}!')
                else:
                    tgbot.send_message(user_id,
                                       text='У пользователя не достаточно денег')
                delete_request_from_db(c, request_id=service_request[0])
            else:
                tgbot.send_message(user_id,
                                   text='Данный пользователь не пользуется ботом')
            return True
        elif 'replenish_user_balance' in call.data:
            call_data, client_id, amount = call.data.split(" ")
            if user_in_db(c, client_id):
                replenish_user_balance(c, client_id, amount)
                tgbot.send_message(user_id,
                                   text='Деньги были зачислены на счёт пользователя')
                tgbot.send_message(client_id,
                                   text=f'{amount} руб. было зачислено на ваш баланс')
                delete_request_from_db(c, request_id=service_request[0])
            else:
                tgbot.send_message(user_id,
                                   text='Данный пользователь не пользуется ботом')
            return True
    # USER SECTION #####################################################################################################
    if call.data == 'none':
        markup = u_menu.get_menu_markup()
        tgbot.send_message(user_id, "⬇️Меню", reply_markup=markup)
    elif 'return_sber' in call.data:
        call_data, rq_id = call.data.split(" ")
        request = get_request_by_id(c, rq_id=rq_id)
        request[2] = "R: wait for return requisites"
        request[5] = "Сбербанк"
        tgbot.send_message(text=f'Введите реквизиты следующим сообщением!',
                           chat_id=user_id)
    elif 'return_qiwi' in call.data:
        call_data, rq_id = call.data.split(" ")
        request = get_request_by_id(c, rq_id=rq_id)
        request[2] = "R: wait for return requisites"
        request[5] = request[5] + " QIWI"
        tgbot.send_message(text=f'Введите реквизиты следующим сообщением!',
                           chat_id=user_id)
    elif call.data == 'edit_requisites':
        return_request[2] = "R: wait for return requisites"
        tgbot.send_message(user_id,
                           text="Введите новые реквизиты следующим сообщением!")
    elif call.data == 'requisites_correct':
        request = return_request
        return_amount = get_return_amount(request)
        user[2] = user[2] - return_amount
        request[2] = "user_payed"
        tgbot.edit_message_text(text='Осталось только подождать! Бот уже отправляет вам деньги',
                                chat_id=user_id, message_id=call.message.message_id)
        text = get_request_text(request) + '\nПользователь ждёт зачисления.'
        send_request_to_operators(text, request)
    elif call.data == 'return_money':
        request = return_request
        if request is not None:
            tgbot.send_message(chat_id=user_id,
                               text='У вас уже есть заявка, желаете её отменить?',
                               reply_markup=SHOW_OR_CANCEL_RETURN_ORDER)
        else:
            request = add_request_to_db(c, [user_id, "R: wait for return value",
                                            'return', str(datetime.now()), 'None', 'None'])
            balance_available_for_return = get_balance_available_for_return(user)
            tgbot.edit_message_text(text=f"Сумма доступная на вывод: {balance_available_for_return}\n"
                                       f"💰 Отправьте сумму в рублях, которую вы хотите вывести"
                                       f"Минимальная сумма вывода: {MIN_VALUE_FOR_RETURN}\n"
                                       f'Максимальная сумма вывода {MAX_VALUE_FOR_RETURN}\n',
                                    chat_id=user_id,
                                    message_id=call.message.message_id)
    elif call.data == 'return_confirmed':
        return_request[2] = 'user_confirmed'
        update_request_in_db(c, return_request)
        tgbot.edit_message_text(text=f'Отлично! Ваша завяка обрабатывается. Уникальный номер заявки: '
                                   f'{1000 + return_request[0]}',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=SHOW_OR_CANCEL_RETURN_ORDER)
        text = get_request_text(return_request) + '\nЗаявка оплачена с баланса бота.'
        send_request_to_operators(text, return_request)

    elif call.data == 'show_help_request':
        request = get_request_by_telegram_id(c, user_id, rq_type='help', status='all')
        text = get_request_text(request)
        if text is not None:
            tgbot.send_message(user_id,
                               text=text,
                               reply_markup=CANCEL_HELP_RQ)
        else:
            tgbot.send_message(
                chat_id=user_id,
                text='Заявка не найдена :('
            )
    elif call.data == 'show_trade':
        request = get_request_by_telegram_id(c, user_id, rq_type='trade', status='all')
        text = get_request_text(request)
        if text is not None:
            tgbot.send_message(user_id,
                               text=text,
                               reply_markup=CANCEL_ORDER)
        else:
            tgbot.send_message(
                chat_id=user_id,
                text='Заявка не найдена :('
            )
    elif call.data == 'show_replenish':
        request = get_request_by_telegram_id(c, user_id, rq_type='replenish', status='all')
        text = get_request_text(request)
        if text is not None:
            tgbot.send_message(user_id,
                               text=text,
                               reply_markup=CANCEL_REPLENISH)
        else:
            tgbot.send_message(
                chat_id=user_id,
                text='Заявка не найдена :('
            )
    elif call.data == 'show_return':
        request = get_request_by_telegram_id(c, user_id, rq_type='return', status='all')
        text = get_request_text(request)
        if text is not None:
            tgbot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=text,
                reply_markup=CANCEL_RETURN
            )
        else:
            tgbot.send_message(
                chat_id=user_id,
                text='Заявка не найдена :('
            )

    elif call.data == 'cancel_trade':
        request = get_request_by_telegram_id(c, user_id, rq_type='trade', status='all')
        if request is not None:
            if request[2] == "user_confirmed" or request[2] == 'user_payed':
                tgbot.edit_message_text(
                    message_id=call.message.message_id,
                    chat_id=user_id,
                    text='Если вы уже перевели деньги по указанным реквизитам, то они зачислятся на ваш баланс.'
                         'Вы уверены, что хотите отменить заявку?',
                    reply_markup=REPLENISH_INSTEAD_TRADE)
            else:

                delete_request_from_db(c, request_id=request[0])
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Ваша заявка была отменена! ⬇️ Меню',
                                   reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')
    elif call.data == 'cancel_help_rq':
        request = get_request_by_telegram_id(c, user_id, rq_type='help', status='all')
        if request is not None:
            delete_request_from_db(c, request_id=request[0])
            tgbot.send_message(chat_id=user_id,
                               text='✅ Ваш вопрос был удалён! ⬇️ Меню',
                               reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')
    elif call.data == 'cancel_return':
        request = get_request_by_telegram_id(c, user_id, rq_type='return', status='all')
        if request is not None:
            if request[2] == 'user_payed':
                tgbot.edit_message_text(
                    message_id=call.message.message_id,
                    chat_id=user_id,
                    text='Деньги уже были списаны с вашего баланса! '
                         'Подождите пока бот отправит их на указанные реквизиты.'
                         'Если вы отмените заявку, то платёж может потеряться! Вы уверены, что хотите отменить заявку?',
                    reply_markup=REPLENISH_INSTEAD_RETURN)
            else:

                delete_request_from_db(c, request_id=request[0])
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Ваша заявка была отменена! ⬇️ Меню',
                                   reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')
    elif call.data == 'cancel_replenish':
        request = get_request_by_telegram_id(c, user_id, rq_type='replenish', status='all')
        if request is not None:
            if request[2] == 'user_confirmed':
                tgbot.edit_message_text(
                    message_id=call.message.message_id,
                    chat_id=user_id,
                    text='Если вы уже перевели деньги по указанным реквизитам, то они зачислятся на ваш баланс.'
                         'Если вы отмените заявку, то платёж может потеряться! Вы уверены, что хотите отменить заявку?',
                    reply_markup=REPLENISH_INSTEAD_REPLENISH)
            else:

                delete_request_from_db(c, request_id=request[0])
                tgbot.send_message(chat_id=user_id,
                                   text='✅ Ваша заявка была отменена! ⬇️ Меню',
                                   reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')

    elif call.data == 'cancel_trade_anyway':
        request = get_request_by_telegram_id(c, user_id, rq_type='trade', status='all')
        if request is not None:
            delete_request_from_db(c, request_id=request[0])
            tgbot.send_message(chat_id=user_id,
                               text='✅ Ваша заявка была отменена! ⬇️ Меню',
                               reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')
    elif call.data == 'cancel_return_anyway':
        request = get_request_by_telegram_id(c, user_id, rq_type='return', status='all')
        if request is not None:
            delete_request_from_db(c, request_id=request[0])
            tgbot.send_message(chat_id=user_id,
                               text='✅ Ваша заявка была отменена! ⬇️ Меню',
                               reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')
    elif call.data == 'cancel_replenish_anyway':
        request = get_request_by_telegram_id(c, user_id, rq_type='replenish', status='all')
        if request is not None:
            delete_request_from_db(c, request_id=request[0])
            tgbot.send_message(chat_id=user_id,
                               text='✅ Ваша заявка была отменена! ⬇️ Меню',
                               reply_markup=u_menu.get_menu_markup())
        else:
            tgbot.send_message(user_id,
                               text='Заявка не найдена :(')

    elif 'priority_usl' == call.data:
        request = trade_request
        request[2] = "T: waiting_for_purchase"
        request[5] = request[5] + ' Обычная комиссия'
        tgbot.edit_message_text(text='Комиссия установлена! Ваша заявка будет обработана как только '
                                   'бот освободится от обработки заявок с более высокими комиссиями.\n'
                                   'Выберите способ оплаты!',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=PAYMENT_METHODS)
    elif 'priority_adv' == call.data:
        request = trade_request
        request[2] = "T: waiting_for_purchase"
        request[5] = change_request_comment_price(request, ADV_PRIORITY_PRICE)
        tgbot.edit_message_text(text='Комиссия установлена! Ваша заявка будет обработана как только '
                                   'бот освободится от обработки заявок с максимальными комиссиями.\n'
                                   'Выберите способ оплаты!',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=PAYMENT_METHODS)
    elif 'priority_max' == call.data:
        request = trade_request
        request[2] = "T: waiting_for_purchase"
        request[5] = change_request_comment_price(request, MAX_PRIORITY_PRICE)
        tgbot.edit_message_text(text='Комиссия установлена! Ваша заявка будет обработана в самое ближайшее время.\n'
                                   'Выберите способ оплаты!',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=PAYMENT_METHODS)

    elif call.data == 'edit_wallet':
        request = trade_request
        request[2] = 'T: waiting_for_usr_wallet'
        tgbot.send_message(user_id,
                           text="Введите новый кошелёк следующим сообщением!")
    elif call.data == 'wallet_correct':
        request = trade_request
        request[2] = "T: waiting for priority"
        tgbot.edit_message_text(text='Выберите желаемую комиссию сети!', chat_id=user_id, message_id=call.message.message_id)
        tgbot.edit_message_reply_markup(user_id, message_id=call.message.message_id, reply_markup=REQUEST_PRIORITIES)

    elif call.data == 'replenish_confirmed':
        request = replenish_request
        request[2] = 'B: waiting_for_purchase'
        tgbot.edit_message_text(text='Выберите способ оплаты!', chat_id=user_id, message_id=call.message.message_id)
        tgbot.edit_message_reply_markup(user_id, message_id=call.message.message_id, reply_markup=REPLENISH_METHODS)
    elif call.data == 'replenish_balance':
        request = replenish_request
        if request is not None and request[2] != 'user_confirmed':
            delete_request_from_db(c, request[0])
            request = add_request_to_db(c, [user_id, "B: wait for replenish value",
                                            'replenish', str(datetime.now()), 'None', 'None'])
        if request is None:
            request = add_request_to_db(c, [user_id, "B: wait for replenish value",
                                            'replenish', str(datetime.now()), 'None', 'None'])
        tgbot.edit_message_text(text=f"💰 Отправьте сумму в рублях, на которую вы хотите пополнить ваш баланс",
                                chat_id=user_id,
                                message_id=call.message.message_id)
    elif call.data == 'replenish_balance_nwmsg':
        request = trade_request
        if request is not None and request[2] != 'user_confirmed':
            delete_request_from_db(c, request[0])
        if request is None:
            request = add_request_to_db(c, [user_id, "B: wait for replenish value",
                                            'replenish', str(datetime.now()), 'None', 'None'])
        tgbot.send_message(text=f"💰 Отправьте сумму в рублях, на которую вы хотите пополнить ваш баланс",
                           chat_id=user_id)
    elif call.data == 'replenish_instead':
        request = trade_request
        comment, user_price = request[5].split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        replenish_value = user_price
        request[5] = f"Пополнение баланса на сумму: {replenish_value}"
        request[2] = 'user_confirmed'
        request[3] = f'replenish {replenish_value}'
        tgbot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=user_id,
            text=f"Пополнение баланса на сумму: {replenish_value} ₽\n"
                 f"Не отменяйте заявку, если передумали пополнять баланс!\n"
                 f"(Ваш платёж потеряется)\n"
                 f"Вы всегда сможете вывести деньги с баланса бота.",
            reply_markup=PURCHASE_CONFIRM_KEYBOARD)
    elif call.data == 'user_confirmed_blnc':
        request = trade_request
        comment, user_price = request[5].split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        user[2] = user[2] - float(user_price)
        update_user_in_db(c, user)
        request[2] = 'user_payed'
        tgbot.edit_message_text(text=f'Отлично! Ваша завяка обрабатывается. Уникальный номер заявки: {1000 + request[0]}',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=SHOW_OR_CANCEL_TRADE_ORDER)
        text = get_request_text(request) + '\nЗаявка оплачена с баланса бота.'
        send_request_to_operators(text, request)
    elif call.data == 'user_confirmed_payment':
        request = trade_request
        request[2] = 'user_confirmed'
        update_request_in_db(c, request)
        tgbot.edit_message_text(text=f'Отлично! Ваша завяка обрабатывается. Уникальный номер заявки: '
                                   f'{1000 + request[0]}',
                                chat_id=user_id,
                                message_id=call.message.message_id,
                                reply_markup=SHOW_OR_CANCEL_TRADE_ORDER)
        text = get_request_text(request)
        send_request_to_operators(text, request)
    elif call.data == 'pay_sber':
        request = trade_request
        request[3] = request[3] + " " + call.data
        trade_information = get_trade_information(request)
        tgbot.edit_message_text(text=f'Реквизиты для оплаты: {SBER_REQUISITES}\n'
                                   f'{trade_information}',
                                reply_markup=PURCHASE_CONFIRM_KEYBOARD,
                                chat_id=user_id,
                                message_id=call.message.message_id)
    elif call.data == 'pay_yandex':
        request = trade_request
        request[3] = request[3] + " " + call.data
        trade_information = get_trade_information(request)
        tgbot.edit_message_text(text=f'Реквизиты для оплаты: {YANDEX_REQUISITES}\n'
                                   f'{trade_information}',
                                reply_markup=PURCHASE_CONFIRM_KEYBOARD,
                                chat_id=user_id,
                                message_id=call.message.message_id)
    elif call.data == 'pay_advcash':
        request = trade_request
        request[3] = request[3] + " " + call.data
        trade_information = get_trade_information(request)
        tgbot.edit_message_text(text=f'Реквизиты для оплаты: {ADVCASH_REQUISITES}\n'
                                   f'{trade_information}',
                                reply_markup=PURCHASE_CONFIRM_KEYBOARD,
                                chat_id=user_id,
                                message_id=call.message.message_id)
    elif call.data == 'pay_balance':
        request = trade_request
        comment, user_price = request[5].split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        request[3] = request[3] + " " + call.data
        if user[2] > float(user_price):
            tgbot.edit_message_text(text=f'Деньги спишутся c вашего баланса в боте: {user[2]}\n',
                                    reply_markup=BALANCE_PAY_CONFIRM_KEYBOARD,
                                    chat_id=user_id,
                                    message_id=call.message.message_id)
        else:
            tgbot.edit_message_text(
                text=f'На вашем счёте недостаточно средств.\n'
                     f'Ваш баланс: {user[2]} руб.\n'
                     f'Выберите другой способ оплаты:',
                reply_markup=REPLENISH_METHODS,
                chat_id=user_id,
                message_id=call.message.message_id
            )
    # USER SECTION #####################################################################################################
    if request is not None:
        update_request_in_db(c, request)


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
