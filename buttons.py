from telebot import types
from content import BotContent


def one_button_keyboard(text, callback_line, url=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text=text, callback_data=callback_line, url=url)
    keyboard.add(button)
    return keyboard


def keyboard_maker(number_of_buttons: int, text_for_each_button: list, callback_data: list):
    keyboard = types.InlineKeyboardMarkup()
    if number_of_buttons > 1:
        butt1 = types.InlineKeyboardButton(text=text_for_each_button[0], callback_data=callback_data[0])
        keyboard.add(butt1)
    if number_of_buttons >= 2:
        butt2 = types.InlineKeyboardButton(text=text_for_each_button[1], callback_data=callback_data[1])
        keyboard.add(butt2)
    if number_of_buttons >= 3:
        butt3 = types.InlineKeyboardButton(text=text_for_each_button[2], callback_data=callback_data[2])
        keyboard.add(butt3)
    if number_of_buttons >= 4:
        butt4 = types.InlineKeyboardButton(text=text_for_each_button[3], callback_data=callback_data[3])
        keyboard.add(butt4)
    return keyboard


REQUISITES_CONFIRM_KEYBOARD = keyboard_maker(2, ['⚒ Изменить реквизиты', '👌 Всё верно'], ['edit_requisites', 'requisites_correct'])
RETURN_MONEY = one_button_keyboard(text='Вывести деньги со счёта', callback_line='return_money')
RETURN_MONEY_CONFIRM_KEYBOARD = keyboard_maker(2, ['👌 Всё верно', '🚫 Отменить заявку'], ['return_confirmed', 'cancel_return'])
REPLENISH_CONFIRM_KEYBOARD = keyboard_maker(2, ['👌 Всё верно', '🚫 Отменить заявку'], ['replenish_confirmed', 'cancel_replenish'])
REPLENISH_INSTEAD_REPLENISH = keyboard_maker(3, ['🚫 Отменить завявку и пополнить баланс', '🕐 Не удалять заявку', '❌ Просто отменить'], ['replenish_instead', 'user_confirmed_payment', 'cancel_replenish_anyway'])
REPLENISH_INSTEAD_RETURN = keyboard_maker(3, ['🚫 Отменить завявку и пополнить баланс', '🕐 Не удалять заявку', '❌ Просто отменить'], ['replenish_instead', 'user_confirmed_payment', 'cancel_return_anyway'])
REPLENISH_INSTEAD_TRADE = keyboard_maker(3, ['🚫 Отменить завявку и пополнить баланс', '🕐 Не удалять заявку', '❌ Просто отменить'], ['replenish_instead', 'user_confirmed_payment', 'cancel_trade_anyway'])
REPLENISH_BALANCE = one_button_keyboard(text="Пополнить баланс", callback_line='replenish_balance')
REPLENISH_BALANCE_FROM_NEW_MSG = one_button_keyboard(text="Пополнить баланс", callback_line='replenish_balance_nwmsg')
CANCEL_ORDER = one_button_keyboard(text="🚫 Отменить заявку", callback_line='cancel_trade')
CANCEL_HELP_RQ = one_button_keyboard(text="🚫 Удалить вопрос", callback_line='cancel_help_rq')
CANCEL_REPLENISH = one_button_keyboard(text='🚫 Отменить заявку', callback_line='cancel_replenish')
CANCEL_RETURN = one_button_keyboard(text='🚫 Отменить заявку', callback_line='cancel_return')
SHOW_OR_CANCEL_TRADE_ORDER = keyboard_maker(2, ['🚫 Отменить заявку', '❓ Показать заявку'], ['cancel_trade', 'show_trade'])
SHOW_OR_CANCEL_REPLENISH_ORDER = keyboard_maker(2, ['🚫 Отменить заявку', '❓ Показать заявку'], ['cancel_replenish', 'show_replenish'])
SHOW_OR_CANCEL_HELP_ORDER = keyboard_maker(2, ['🚫 Удалить вопрос', '❓ Показать вопрос'], ['cancel_help_request', 'show_help_request'])
SHOW_OR_CANCEL_RETURN_ORDER = keyboard_maker(2, ['🚫 Отменить заявку', '❓ Показать заявку'], ['cancel_return', 'show_return'])
WALLET_CONFIRM_KEYBOARD = keyboard_maker(2, ['⚒ Изменить кошелёк', '👌 Всё верно'], ['edit_wallet', 'wallet_correct'])
PURCHASE_CONFIRM_KEYBOARD = keyboard_maker(2, ['👌 Оплатил', '🚫 Отменить заявку'], ['user_confirmed_payment', 'cancel_trade'])
BALANCE_PAY_CONFIRM_KEYBOARD = keyboard_maker(2, ['👌 Оплатить', '🚫 Отменить заявку'], ['user_confirmed_blnc', 'cancel'])

PAYMENT_METHODS = keyboard_maker(4, ['Сбербанк', 'Яндекс.Деньги', 'AdvCash', 'Списать деньги с баланса'],
                                 ['pay_sber', 'pay_yandex', 'pay_advcash', 'pay_balance'])
CANCEL = types.InlineKeyboardButton(text='🚫 Отменить заявку', callback_data='cancel_trade')
PAYMENT_METHODS.add(CANCEL)

REPLENISH_METHODS = keyboard_maker(4, ['Сбербанк', 'Яндекс.Деньги', 'AdvCash', '🚫 Отменить заявку'],
                                 ['pay_sber', 'pay_yandex', 'pay_advcash', 'cancel'])

REQUEST_PRIORITIES = keyboard_maker(3, ['Обычная', 'Повышенная (+80р.)', "Максимальная (+230р.)"],
                                    ['priority_usl', 'priority_adv', 'priority_max'])


class CryptoMenu:
    MENU_BUTTONS = {
                    'btc': 'Bitcoin(BTC)',
                    'ltc': 'LiteCoin(LTC)',
                    'exmo': 'ExmoRUB',
                    'eth': 'Ethereum(ETH)',
                    'bch': 'Bitcoin Cash(BCH)',
                    'main_menu': 'Главное меню'
                    }

    def get_menu_markup(self):
        markup = types.ReplyKeyboardMarkup()
        currency_btn_btc = types.KeyboardButton(self.MENU_BUTTONS['btc'])
        currency_btn_ltc = types.KeyboardButton(self.MENU_BUTTONS['ltc'])
        currency_btn_exmo = types.KeyboardButton(self.MENU_BUTTONS['exmo'])
        currency_btn_eth = types.KeyboardButton(self.MENU_BUTTONS['eth'])
        currency_btn_bch = types.KeyboardButton(self.MENU_BUTTONS['bch'])
        back_btn = types.KeyboardButton(self.MENU_BUTTONS['main_menu'])

        markup.row(currency_btn_btc, currency_btn_exmo)
        markup.row(currency_btn_ltc, currency_btn_eth, currency_btn_bch)
        markup.row(back_btn)
        return markup

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False


class PersonalMenu:
    MENU_BUTTONS = {
        'replenish': 'Пополнить баланс бота',
        'show_balance': 'Показать баланс',
        'back': 'Главное меню'
    }

    def get_menu_markup(self):
        markup = types.ReplyKeyboardMarkup()
        replenish_btn = types.KeyboardButton(self.MENU_BUTTONS['replenish'])
        blnc_btn = types.KeyboardButton(self.MENU_BUTTONS['show_balance'])
        back_btn = types.KeyboardButton(self.MENU_BUTTONS['back'])
        markup.row(replenish_btn, blnc_btn)
        markup.row(back_btn)
        return markup

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False


class UserMenu:
    MENU_BUTTONS = {'buy': 'Купить криптовалюту',
                    'personal_cabinet': 'Личный кабинет',
                    'help': 'Помощь 🆘',
                    'partnership': 'Партнёрка 👥'
                    }

    def get_menu_markup(self):
        markup = types.ReplyKeyboardMarkup()
        trade_btn = types.KeyboardButton(self.MENU_BUTTONS['buy'])
        help_btn = types.KeyboardButton(self.MENU_BUTTONS['help'])
        personal_menu_btn = types.KeyboardButton(self.MENU_BUTTONS['personal_cabinet'])
        partnership_btn = types.KeyboardButton(self.MENU_BUTTONS['partnership'])

        markup.row(trade_btn, help_btn)
        markup.row(partnership_btn, personal_menu_btn)
        return markup

    def suggestion_menu(self):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        group_btn = types.InlineKeyboardButton(text="Наш групповой чат 💬", url=BotContent.URLS['group'])
        channel_btn = types.InlineKeyboardButton(text="Наш канал 📢", url=BotContent.URLS['channel'])
        keyboard.add(group_btn, channel_btn)
        return keyboard

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False


class OperatorMenu:
    MENU_BUTTONS = {'show_n_a_requests': 'Показать заявки, требующие обработки',
                    'replenish_user_balance': 'Пополнить баланс пользователя',
                    'cut_user_balance': 'Списать с баланса пользователя',
                    'send_message_to_user': 'Отправить сообщение пользователю',
                    'main_menu': 'Пользовательское меню'
                    }

    def get_menu_markup(self):
        markup = types.ReplyKeyboardMarkup()
        replenish_user = types.KeyboardButton(self.MENU_BUTTONS['replenish_user'])
        show_n_a_requests = types.KeyboardButton(self.MENU_BUTTONS['show_n_a_requests'])
        cut_user_balance = types.KeyboardButton(self.MENU_BUTTONS['cut_user_balance'])
        h_request = types.KeyboardButton(self.MENU_BUTTONS['h_request'])
        back_btn = types.KeyboardButton(self.MENU_BUTTONS['back'])
        markup.row(replenish_user, show_n_a_requests)
        markup.row(cut_user_balance, h_request)
        markup.row(back_btn)
        return markup

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False


class AdminMenu:
    MENU_BUTTONS = {
                    'a_admin': "Добавить админа",
                    'd_admin': "Удалить админа",
                    'a_oper': 'Добавить оператора',
                    'd_oper': 'Удалить оператора'
                    }

    def get_menu_markup(self):
        markup = types.ReplyKeyboardMarkup()
        r_request = types.KeyboardButton(self.MENU_BUTTONS['a_admin'])
        n_a_requests = types.KeyboardButton(self.MENU_BUTTONS['d_admin'])
        d_request = types.KeyboardButton(self.MENU_BUTTONS['a_oper'])
        h_request = types.KeyboardButton(self.MENU_BUTTONS['d_oper'])
        markup.row(r_request, n_a_requests)
        markup.row(d_request, h_request)
        return markup

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False
