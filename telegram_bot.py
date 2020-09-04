from functions import get_request_text, add_admin, add_operator, delete_operator, delete_admin, get_return_amount, \
    change_request_comment_price, get_trade_information
from datetime import datetime
from models import MessageParser, CallParser, get_admins_list, get_operators_list
from content import BotContent
from buttons import *
from database import Request


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
        self.admins = get_admins_list()

    def send_request_not_found(self):
        self.tgbot.send_message(
            chat_id=self.user.telegram_id,
            text=self.content.MESSAGES['request_not_found']
        )

    def replenish_client_balance(self, client_id, amount):
        user = self.database.get_user_by_telegram_id(client_id)
        if (float(user.balance) - float(amount)) > 0:
            user.balance = float(user.balance) - float(amount)
            self.database.update_user_in_db(user)
            return True
        else:
            return False

    def take_money_from_client_balance(self, client_id, amount: (int or float), ):
        user = self.database.get_user_by_telegram_id(client_id)
        if (float(user.balance) - float(amount)) > 0:
            user.balance = float(user.balance) - float(amount)
            self.database.update_user_in_db(user)
            return True
        else:
            return False

    def raise_users_q_of_trades(self):
        self.user.quantity_of_trades = self.user.quantity_of_trades + 1
        if self.user.quantity_of_trades == self.content.TO_ACHIEVE_MEDIUM_STATUS:
            self.user.status = self.content.MEDIUM_STATUS
        elif self.user.quantity_of_trades == self.content.TO_ACHIEVE_ADVANCED_STATUS:
            self.user.quantity_of_trades = self.content.ADVANCED_STATUS
        self.database.update_user_in_db(self.user)

    def return_is_possible(self, return_value):
        return float(self.user.balance) > return_value and self.return_value_is_acceptable(return_value)

    def get_balance_available_for_return(self):
        return self.user.balance * self.content.RETURN_PERCENT

    def return_value_is_acceptable(self, return_value) -> bool:
        return self.content.MIN_VALUE_FOR_RETURN <= return_value <= self.content.MAX_VALUE_FOR_RETURN

    def get_last_cur_update(self):
        return self.currency_bot.last_cur_update

    def send_request_to_operators_with_comment(self, comment: str):
        text = get_request_text(self.user.return_request) + '\n' + comment
        self.send_request_to_operators(text, self.user.return_request)

    def send_request_to_operators(self, text, request):
        # TODO

        if 'help_request' not in request.type:
            operator_buttons = keyboard_maker(2, ['Пользователь оплатил', 'Пользователь не оплатил'],
                                              [f'confirm {request.db_id}', f'cancel {request.db_id}'])

        else:
            operator_buttons = keyboard_maker(2, ['Ответить на вопрос', 'Удалить вопрос'],
                                              [f'answer {request.db_id}', f'cancel_question {request.db_id}'])
        for operator in self.operators:
            self.tgbot.send_message(operator, text=text,
                                    reply_markup=operator_buttons)

    def show_all_requests_to_operators(self, requests):
        for request in requests:
            text = get_request_text(request)
            self.send_request_to_operators(text=text, request=request)

    def check_user_is_follower(self, user_id):
        group_status = self.tgbot.get_chat_member(chat_id=self.content.GROUP_ID, user_id=user_id)
        channel = self.tgbot.get_chat_member(chat_id=self.content.CHANNEL_ID, user_id=user_id)
        if "'status': 'left'" in str(group_status):
            if "'status': 'left'" in str(channel):
                return 0
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

    def add_new_return_request(self):
        request = (self.user.telegram_id,
                   "R: wait for return value",  # status
                   'return',  # type
                   str(datetime.now()),   # when created
                   'None',   # comment
                   'None')   # wallet
        self.database.add_request_to_db(request)

    def add_new_replenish_request(self):
        request = (self.user.telegram_id,
                   "B: wait for replenish value",   # status
                   'replenish',  # type
                   str(datetime.now()),   # when created
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

    def send_replenish_balance_message(self):
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
            self.tgbot.send_message(self.user.telegram_id,
                                    text=self.content.MESSAGES['requests_not_found'])

    def send_replenish_user_balance(self):
        self.add_new_service_request('S: wait_for_user_replenish')
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_replenish'])

    def send_unreplenish_user_balance(self):
        self.add_new_service_request('S: wait_for_user_unreplenish')
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_unreplenish'])

    def send_message_to_user(self):
        self.add_new_service_request('S: wait_for_msg')
        self.tgbot.send_message(self.user.telegram_id, text=self.content.MESSAGES['user_balance_replenish'])

    def send_addoper(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /addoper")

    def send_addadmin(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /addadmin")

    def send_deloper(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /deloper")

    def send_deladmin(self):
        self.tgbot.send_message(self.user.telegram_id, text="Используй команду /deladmin")

    def send_return_impossible_message(self):
        self.tgbot.send_message(
            text=self.content.MESSAGES['return_failure'].format(self.get_balance_available_for_return(),
                                                                self.content.MIN_VALUE_FOR_RETURN),
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
        self.tgbot.send_message(self.user.telegram_id,
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
        self.tgbot.send_message(self.user.telegram_id, text=message, reply_markup=CANCEL_ORDER)
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
        call_data, client_id, message = self.call_parser.data.split(':')
        self.tgbot.send_message(client_id,
                                self.content.MESSAGES['message_from_operator_notification'].format(message))
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['message_sent_notification'])
        self.database.delete_request_from_db(self.user.service_request.db_id)

    def send_status_from_operator(self):
        client_id, message = self.database.get_status_message(self.call_parser.data)
        self.tgbot.send_message(self.user.telegram_id,
                                self.content.MESSAGES['message_sent_notification'])
        self.tgbot.send_message(client_id, text=message)

    def send_answer_from_operator(self):
        call_data, client_id, answer = self.call_parser.data.split(' ')
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

    def send_question_cancelled_by_operator(self):
        request = self.get_request_from_call_data()
        if request is not None:
            self.database.delete_request_from_db(request.db_id)
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['question_deleted'])
        else:
            self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['question_deleted'])

    def send_request_cancelled_by_operator(self):
        request = self.get_request_from_call_data()
        if request is not None:
            send_msg_to_user = keyboard_maker(3, ['Отправил недостаточно средств', 'Вообще не совершил платёж',
                                                  'Закрыть заявку'],
                                              [f'send_status {request.db_id} {request.telegram_id} not_enough',
                                               f'send_status {request.db_id} {request.telegram_id} no_payment',
                                               f'send_status {request.db_id} {request.telegram_id} close_request']
                                              )
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                               text=self.content.MESSAGES['request_cancelled_by_operator'],
                               reply_markup=send_msg_to_user)
        else:
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                               text=self.content.MESSAGES['request_deleted'])

    def get_request_from_call_data(self):
        call_data, rq_id = self.call_parser.data.split(" ")
        request = self.database.get_request_by_id(rq_id)
        return request

    def send_request_confirmed_by_operator(self):
        request = self.get_request_from_call_data()
        self.raise_users_q_of_trades()
        if request is not None:
            send_msg_to_user = keyboard_maker(4, ['Подтвердить перевод',
                                                  'Пользователю отправили криптовалюту',
                                                  'Пополнить баланс пользователю',
                                                  'Закрыть заявку'],
                                              [f'send_status {request.db_id} {request.telegram_id} payment_s',
                                               f'send_status {request.db_id} {request.telegram_id} crypto_sent',
                                               f'send_status {request.db_id} {request.telegram_id} replenish_s',
                                               f'cancel {request.db_id}']
                                              )
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                               text=self.content.MESSAGES['notify_user'],
                               reply_markup=send_msg_to_user)
        else:
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                               text=self.content.MESSAGES['request_cancelled'])

    def operator_unreplenish_client_balance(self):
        call_data, client_id, amount = self.call_parser.data.split(" ")
        if self.database.user_in_db(self.user.telegram_id):
            if self.take_money_from_client_balance(client_id, amount):
                self.tgbot.send_message(self.user.telegram_id,
                                        text=self.content.MESSAGES['balance_cut'])
                self.tgbot.send_message(client_id,
                                        text=self.content.MESSAGES['balance_cut_notification'].format(amount))
            else:
                self.tgbot.send_message(self.user.telegram_id,
                                        text=self.content.MESSAGES['user_have_low_balance'])
            self.database.delete_request_from_db(request_id=self.user.service_request.db_id)
        else:
            self.send_client_not_found()

    def send_client_not_found(self):
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['user_not_found'])

    def operator_replenish_client_balance(self):
        call_data, client_id, amount = self.call_parser.data.split(" ")
        if self.database.user_in_db(client_id):
            self.replenish_client_balance(client_id, amount)
            self.tgbot.send_message(self.user.telegram_id,
                               text=self.content.MESSAGES['client_balance_replenished'])
            self.tgbot.send_message(client_id,
                               text=self.content.MESSAGES['balance_replenished'].format(amount))
            self.database.delete_request_from_db(request_id=self.user.service_request.db_id)
        else:
            self.send_client_not_found()

    def user_menu_handler(self):
        if self.user_menu.MENU_BUTTONS['buy'] in self.message_parser.user_message.text:
            self.send_buy_crypto()

        elif self.user_menu.MENU_BUTTONS['partnership'] in self.message_parser.user_message.text:
            self.send_partnership()

        elif self.user_menu.MENU_BUTTONS['help'] in self.message_parser.user_message.text:
            self.send_help()

        elif self.user_menu.MENU_BUTTONS['personal_cabinet'] in self.message_parser.user_message.text:
            self.send_personal_cabinet()

    def personal_menu_handler(self):
        if self.personal_menu.MENU_BUTTONS['replenish'] in self.message_parser.user_message.text:
            self.send_replenish_balance_message()

        elif self.personal_menu.MENU_BUTTONS['show_balance'] in self.message_parser.user_message.text:
            self.send_current_balance()

        elif self.personal_menu.MENU_BUTTONS['main_menu'] in self.message_parser.user_message.text:
            self.send_main_menu()

    def crypto_menu_handler(self):
        if self.crypto_menu.MENU_BUTTONS['btc'] in self.message_parser.user_message.text:
            key = 'Bitcoin'
            self.send_start_trade_rq(key)

        elif self.crypto_menu.MENU_BUTTONS['ltc'] in self.message_parser.user_message.text:
            key = "LiteCoin"
            self.send_start_trade_rq(key)

        elif self.crypto_menu.MENU_BUTTONS['exmo'] in self.message_parser.user_message.text:
            key = "ExmoRUB"
            self.send_start_trade_rq(key)

        elif self.crypto_menu.MENU_BUTTONS['eth'] in self.message_parser.user_message.text:
            key = "Ethereum"
            self.send_start_trade_rq(key)

        elif self.crypto_menu.MENU_BUTTONS['bch'] in self.message_parser.user_message.text:
            key = "Bitcoin Cash"
            self.send_start_trade_rq(key)

        elif self.crypto_menu.MENU_BUTTONS['main_menu'] in self.message_parser.user_message.text:
            self.send_main_menu()

    def operator_menu_handler(self):
        if self.operator_menu.MENU_BUTTONS['show_n_a_requests'] in self.message_parser.user_message.text:
            self.send_raw_requests()

        elif self.operator_menu.MENU_BUTTONS['replenish_user'] in self.message_parser.user_message.text:
            self.send_replenish_user_balance()

        elif self.operator_menu.MENU_BUTTONS['cut_user_balance'] in self.message_parser.user_message.text:
            self.send_unreplenish_user_balance()

        elif self.operator_menu.MENU_BUTTONS['send_message_to_user'] in self.message_parser.user_message.text:
            self.send_message_to_user()

        elif self.operator_menu.MENU_BUTTONS['main_menu'] in self.message_parser.user_message.text:
            self.send_main_menu()

    def admin_menu_handler(self):
        if self.admin_menu.MENU_BUTTONS['addoper'] in self.message_parser.user_message.text:
            self.send_addoper()
        elif self.admin_menu.MENU_BUTTONS['addadmin'] in self.message_parser.user_message.text:
            self.send_addadmin()
        elif self.admin_menu.MENU_BUTTONS['deloper'] in self.message_parser.user_message.text:
            self.send_deloper()
        elif self.admin_menu.MENU_BUTTONS['deladmin'] in self.message_parser.user_message.text:
            self.send_deladmin()

    def request_processing(self):
        if self.user.all_requests_is_none():
            self.send_main_menu()
        elif self.user.return_request is not None:
            self.return_request_processing()
        elif self.user.service_request is not None:
            self.service_request_processing()
        elif self.user.help_request is not None:
            self.help_request_processing()
        elif self.user.replenish_request is not None:
            self.replenish_request_processing()
        elif self.user.trade_request is not None:
            self.trade_request_processing()

    def message_processor(self):
        if self.user_menu.sent_by_menu(self.message_parser.user_message.text):
            self.user_menu_handler()
        elif self.personal_menu.sent_by_menu(self.message_parser.user_message.text):
            self.personal_menu_handler()
        elif self.crypto_menu.sent_by_menu(self.message_parser.user_message.text):
            self.crypto_menu_handler()
        elif self.operator_menu.sent_by_menu(self.message_parser.user_message.text) and self.user.is_admin or self.user.is_operator:
            self.operator_menu_handler()
        elif self.admin_menu.sent_by_menu(self.message_parser.user_message.text) and self.user.is_admin:
            self.admin_menu_handler()
        else:
            self.request_processing()

    def operator_call_data_handler(self):
        if 'send_msg' in self.call_parser.data:
            self.send_message_from_operator()
            return True
        elif 'send_status' in self.call_parser.data:
            self.send_status_from_operator()
            return True
        elif 'sendanswer' in self.call_parser.data:
            self.send_answer_from_operator()
            return True
        elif 'answer' in self.call_parser.data:
            self.send_wait_for_operator_answer()
            return True
        elif 'cancel_question' in self.call_parser.data:
            self.send_question_cancelled_by_operator()
            return True
        elif 'cancel ' in self.call_parser.data:
            self.send_request_cancelled_by_operator()
            return True
        elif 'confirm ' in self.call_parser.data:
            self.send_request_confirmed_by_operator()
            return True
        elif 'unreplenish_user_balance' in self.call_parser.data:
            self.operator_unreplenish_client_balance()
            return True
        elif 'replenish_user_balance' in self.call_parser.data:
            self.operator_replenish_client_balance()
            return True

    def send_return_sber(self):
        self.user.return_request.status = "R: wait for return requisites"
        self.user.return_request.comment = "Сбербанк"
        self.tgbot.send_message(text=self.content.MESSAGES['input_requisites_next'],
                                chat_id=self.user.telegram_id)

    def send_return_qiwi(self):
        self.user.return_request.status = "R: wait for return requisites"
        self.user.return_request.comment = self.user.return_request.comment + " QIWI"
        self.tgbot.send_message(text=self.content.MESSAGES['input_requisites_next'],
                           chat_id=self.user.telegram_id)

    def send_edit_requisites(self):
        self.user.return_request.status = "R: wait for return requisites"
        self.tgbot.send_message(self.user.telegram_id,
                           text=self.content.MESSAGES['input_requisites_next'])

    def send_requisites_correct(self):
        return_amount = get_return_amount(self.user.return_request)
        self.user.balance = self.user.balance - return_amount
        self.user.return_request.status = "user_payed"
        self.tgbot.edit_message_text(text=self.content.MESSAGES['wait_after_return'],
                                     chat_id=self.user.telegram_id, message_id=self.call_parser.message.message_id)
        self.send_request_to_operators_with_comment('Пользователь ждёт зачисления.')

    def send_return_money(self):
        if self.user.return_request is not None:
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                                    text=self.content.MESSAGES['already_have_request'],
                                    reply_markup=SHOW_OR_CANCEL_RETURN_ORDER)
        else:
            self.add_new_return_request()
            value_available_for_return = self.user.get_balance_available_for_return()
            self.tgbot.edit_message_text(text=self.content.MESSAGES['return_available'].
                                         format(value_available_for_return,
                                                self.content.MIN_VALUE_FOR_RETURN,
                                                self.content.MAX_VALUE_FOR_RETURN),
                                         chat_id=self.user.telegram_id,
                                         message_id=self.call_parser.message.message_id)

    def send_return_confirmed(self):
        self.user.return_request.type = 'user_confirmed'
        self.database.update_request_in_db(self.user.return_request)
        self.tgbot.edit_message_text(text=self.content.MESSAGES['request_in_progress'].format(1000 + self.user.return_request.db_id),
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=SHOW_OR_CANCEL_RETURN_ORDER)
        self.send_request_to_operators_with_comment('Заявка оплачена с баланса бота.')

    def send_show_help_request(self):
        text = get_request_text(self.user.help_request)
        if text is not None:
            self.tgbot.send_message(self.user.telegram_id,
                                    text=text,
                                    reply_markup=CANCEL_HELP_RQ)
        else:
            self.send_request_not_found()

    def send_show_trade_request(self):
        text = get_request_text(self.user.trade_request)
        if text is not None:
            self.tgbot.send_message(self.user.telegram_id,
                                    text=text,
                                    reply_markup=CANCEL_ORDER)
        else:
            self.send_request_not_found()

    def send_show_replenish_request(self):
        text = get_request_text(self.user.replenish_request)
        if text is not None:
            self.tgbot.send_message(self.user.telegram_id,
                               text=text,
                               reply_markup=CANCEL_REPLENISH)
        else:
            self.send_request_not_found()

    def send_show_return_request(self):
        text = get_request_text(self.user.return_request)
        if text is not None:
            self.tgbot.send_message_text(
                chat_id=self.user.telegram_id,
                text=text,
                reply_markup=CANCEL_RETURN
            )
        else:
            self.send_request_not_found()

    def send_request_cancelled(self):
        self.tgbot.send_message(self.user.telegram_id, self.content.MESSAGES['request_cancelled'])

    def send_cancel_trade_request(self):
        if self.user.trade_request is not None:
            if self.user.trade_request.type == "user_confirmed" or self.user.trade_request.type == 'user_payed':
                self.tgbot.edit_message_text(
                    message_id=self.call_parser.message.message_id,
                    chat_id=self.user.telegram_id,
                    text=self.content.MESSAGES['trade_cancel_warning'],
                    reply_markup=REPLENISH_INSTEAD_TRADE)
            else:
                self.database.delete_request_from_db(request_id=self.user.trade_request.db_id)
                self.send_request_cancelled()
                self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_help_request(self):
        if self.user.help_request is not None:
            self.database.delete_request_from_db(request_id=self.user.help_request.db_id)
            self.tgbot.send_message(chat_id=self.user.telegram_id,
                                    text=self.content.MESSAGES['question_deleted'])
            self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_return_request(self):
        if self.user.return_request is not None:
            if self.user.return_request.status == 'user_payed':
                self.tgbot.edit_message_text(
                    message_id=self.call_parser.message.message_id,
                    chat_id=self.user.telegram_id,
                    text=self.content.MESSAGES['return_cancel_warning'],
                    reply_markup=REPLENISH_INSTEAD_RETURN)
            else:
                self.database.delete_request_from_db(request_id=self.user.trade_request.db_id)
                self.send_request_cancelled()
                self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_replenish_request(self):
        if self.user.replenish_request is not None:
            if self.user.replenish_request.status == 'user_confirmed':
                self.tgbot.edit_message_text(
                    message_id=self.call_parser.message.message_id,
                    chat_id=self.user.telegram_id,
                    text=self.content.MESSAGES['replenish_cancel_warning'],
                    reply_markup=REPLENISH_INSTEAD_REPLENISH)
            else:
                self.database.delete_request_from_db(request_id=self.user.trade_request.db_id)
                self.send_request_cancelled()
                self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_return_request_anyway(self):
        if self.user.return_request is not None:
            self.database.delete_request_from_db(request_id=self.user.return_request.db_id)
            self.send_request_cancelled()
            self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_trade_request_anyway(self):
        if self.user.trade_request is not None:
            self.database.delete_request_from_db(request_id=self.user.trade_request.db_id)
            self.send_request_cancelled()
            self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_cancel_replenish_request_anyway(self):
        if self.user.replenish_request is not None:
            self.database.delete_request_from_db(request_id=self.user.replenish_request.db_id)
            self.send_request_cancelled()
            self.send_main_menu()
        else:
            self.send_request_not_found()

    def send_usual_commission(self):
        self.user.trade_request.status = "T: waiting_for_purchase"
        self.user.trade_request.comment = change_request_comment_price(self.user.trade_request, 0)
        self.tgbot.edit_message_text(text=self.content.MESSAGES['usual_commission'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=PAYMENT_METHODS)

    def send_adv_commission(self):
        self.user.trade_request.status = "T: waiting_for_purchase"
        self.user.trade_request.comment = change_request_comment_price(self.user.trade_request,
                                                                       self.content.ADV_PRIORITY_PRICE)
        self.tgbot.edit_message_text(text=self.content.MESSAGES['adv_commission'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=PAYMENT_METHODS)

    def send_max_commission(self):
        self.user.trade_request.status = "T: waiting_for_purchase"
        self.user.trade_request.comment = change_request_comment_price(self.user.trade_request,
                                                                       self.content.MAX_PRIORITY_PRICE)
        self.tgbot.edit_message_text(text=self.content.MESSAGES['max_commission'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=PAYMENT_METHODS)

    def send_edit_wallet(self):
        self.user.trade_request.status = 'T: waiting_for_usr_wallet'
        self.tgbot.send_message(self.user.telegram_id,
                                text=self.content.MESSAGES['edit_wallet'])

    def send_wallet_correct(self):
        self.user.trade_request.status = "T: waiting for priority"
        self.tgbot.edit_message_text(text=self.content.MESSAGES['wallet_correct'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=REQUEST_PRIORITIES)

    def send_replenish_confirmed(self):
        self.user.replenish_request.status = 'B: waiting_for_purchase'
        self.tgbot.edit_message_text(text=self.content.MESSAGES['choose_payment_method'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id,
                                     reply_markup=REPLENISH_METHODS)

    def send_replenish_balance(self):
        if self.user.replenish_request is not None and self.user.replenish_request.type != 'user_confirmed':
            self.database.delete_request_from_db(self.user.replenish_request.db_id)
            self.add_new_replenish_request()
        if self.user.replenish_request is None:
            self.add_new_replenish_request()
        self.tgbot.edit_message_text(text=self.content.MESSAGES['input_replenish_amount'],
                                     chat_id=self.user.telegram_id,
                                     message_id=self.call_parser.message.message_id)

    def send_replenish_balance_newmsg(self):
        if self.user.trade_request is not None and self.user.trade_request.status != 'user_confirmed':
            self.database.delete_request_from_db(self.user.trade_request.db_id)
            self.add_new_replenish_request()
        if self.user.trade_request is None:
            self.add_new_replenish_request()
        self.tgbot.send_message(text=self.content.MESSAGES['input_replenish_amount'],
                                chat_id=self.user.telegram_id)

    def send_replenish_instead(self):
        comment, user_price = self.user.trade_request.comment.split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        replenish_value = user_price
        self.user.trade_request.comment = f"Пополнение баланса на сумму: {replenish_value}"
        self.user.trade_request.status = 'user_confirmed'
        self.user.trade_request.type = f'replenish {replenish_value}'
        self.tgbot.edit_message_text(
            message_id=self.call_parser.message.message_id,
            chat_id=self.user.telegram_id,
            text=self.content.MESSAGES['replenish_confirm'].format(replenish_value),
            reply_markup=PURCHASE_CONFIRM_KEYBOARD)

    def get_request_number(self, request: Request):
        return self.content.BASE_REQUEST_NUM + request.db_id

    def send_user_confirmed_blnc(self):
        comment, user_price = self.user.trade_request.comment.split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        self.user.balance = self.user.balance - float(user_price)
        self.database.update_user_in_db(self.user)
        self.user.trade_request.status = 'user_payed'
        self.tgbot.edit_message_text(
            text=self.content.MESSAGES['request_processing'].format(self.get_request_number(self.user.trade_request)),
            chat_id=self.user.telegram_id,
            message_id=self.call_parser.message.message_id,
            reply_markup=SHOW_OR_CANCEL_TRADE_ORDER)
        text = get_request_text(self.user.trade_request) + '\nЗаявка оплачена с баланса бота.'
        self.send_request_to_operators(text, self.user.trade_request)

    def send_user_confirmed_payment(self):
        self.user.trade_request.status = 'user_confirmed'
        self.database.update_request_in_db(self.user.trade_request)
        self.tgbot.edit_message_text(
            text=self.content.MESSAGES['request_processing'].format(self.get_request_number(self.user.trade_request)),
            chat_id=self.user.telegram_id,
            message_id=self.call_parser.message.message_id,
            reply_markup=SHOW_OR_CANCEL_TRADE_ORDER)
        text = get_request_text(self.user.trade_request)
        self.send_request_to_operators(text, self.user.trade_request)

    def send_pay(self):
        self.user.trade_request.type = self.user.trade_request.type + " " + self.call_parser.data
        trade_information = get_trade_information(self.user.trade_request)
        self.tgbot.edit_message_text(
            text=self.content.MESSAGES['requisites_for_payment'].format(self.content.REQUISITES[self.call_parser.data],
                                                                        trade_information),
            reply_markup=PURCHASE_CONFIRM_KEYBOARD,
            chat_id=self.user.telegram_id,
            message_id=self.call_parser.message.message_id)

    def send_pay_balance(self):
        comment, user_price = self.user.trade_request.comment.split(': ')
        user_price = user_price.split(" Приоритет ")[0]
        self.user.trade_request.type = self.user.trade_request.type + " " + self.call_parser.data
        if self.user.balance > float(user_price):
            self.tgbot.edit_message_text(
                text=self.content.MESSAGES['pay_balance'].format(self.user.balance),
                reply_markup=BALANCE_PAY_CONFIRM_KEYBOARD,
                chat_id=self.user.telegram_id,
                message_id=self.call_parser.message.message_id)
        else:
            self.tgbot.edit_message_text(
                text=self.content.MESSAGES['balance_is_too_low'].format(self.user.balance),
                reply_markup=REPLENISH_METHODS,
                chat_id=self.user.telegram_id,
                message_id=self.call_parser.message.message_id
            )

    def user_call_data_handler(self):
        if 'return_sber' in self.call_parser.data:
            self.send_return_sber()
        elif 'return_qiwi' in self.call_parser.data:
            self.send_return_qiwi()
        elif self.call_parser.data == 'edit_requisites':
            self.send_edit_requisites()
        elif self.call_parser.data == 'requisites_correct':
            self.send_requisites_correct()
        elif self.call_parser.data == 'return_money':
            self.send_return_money()
        elif self.call_parser.data == 'return_confirmed':
            self.send_return_confirmed()

        elif self.call_parser.data == 'show_help_request':
            self.send_show_help_request()
        elif self.call_parser.data == 'show_trade':
            self.send_show_trade_request()
        elif self.call_parser.data == 'show_replenish':
            self.send_show_replenish_request()
        elif self.call_parser.data == 'show_return':
            self.send_show_return_request()

        elif self.call_parser.data == 'cancel_trade':
            self.send_cancel_trade_request()
        elif self.call_parser.data == 'cancel_help_rq':
            self.send_cancel_help_request()
        elif self.call_parser.data == 'cancel_return':
            self.send_cancel_return_request()
        elif self.call_parser.data == 'cancel_replenish':
            self.send_cancel_replenish_request()

        elif self.call_parser.data == 'cancel_trade_anyway':
            self.send_cancel_trade_request_anyway()
        elif self.call_parser.data == 'cancel_return_anyway':
            self.send_cancel_return_request_anyway()
        elif self.call_parser.data == 'cancel_replenish_anyway':
            self.send_cancel_replenish_request_anyway()

        elif 'priority_usl' == self.call_parser.data:
            self.send_usual_commission()
        elif 'priority_adv' == self.call_parser.data:
            self.send_adv_commission()
        elif 'priority_max' == self.call_parser.data:
            self.send_max_commission()

        elif self.call_parser.data == 'edit_wallet':
            self.send_edit_wallet()
        elif self.call_parser.data == 'wallet_correct':
            self.send_wallet_correct()

        elif self.call_parser.data == 'replenish_confirmed':
            self.send_replenish_confirmed()
        elif self.call_parser.data == 'replenish_balance':
            self.send_replenish_balance()
        elif self.call_parser.data == 'replenish_balance_nwmsg':
            self.send_replenish_balance_newmsg()
        elif self.call_parser.data == 'replenish_instead':
            self.send_replenish_instead()
        elif self.call_parser.data == 'user_confirmed_blnc':
            self.send_user_confirmed_blnc()
        elif self.call_parser.data == 'user_confirmed_payment':
            self.send_user_confirmed_payment()

        elif self.call_parser.data == 'pay_sber':
            self.send_pay()
        elif self.call_parser.data == 'pay_yandex':
            self.send_pay()
        elif self.call_parser.data == 'pay_advcash':
            self.send_pay()
        elif self.call_parser.data == 'pay_balance':
            self.send_pay_balance()