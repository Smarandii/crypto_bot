import coinaddr

from database import get_requests
from secrets import PERCENTS, DISCOUNTS, OPERATORS_LIST, ADMINS_LIST, MIN_VALUE_FOR_RETURN, MAX_VALUE_FOR_RETURN, \
    ADV_PRIORITY_PRICE, MAX_PRIORITY_PRICE


def get_prepayment_message(user_curr, trade_value, user_price, key) -> str:
    messages = {'Bitcoin': f"Курс: {user_curr} руб.\n"
                                          f"Покупка {trade_value} {key}\n"
                                          f"К оплате: {user_price} руб.\n"
                                          f"Следующим сообщением отправьте нам ваш криптокошелёк.\n"
                                          f"Пример: 3GncF7muEw1oayeuH33rxahdmtHSWoj4tw",
                'LiteCoin': f"Курс: {user_curr} руб.\n"
                                          f"Покупка {trade_value} {key}\n"
                                          f"К оплате: {user_price} руб.\n"
                                          f"Следующим сообщением отправьте нам ваш криптокошелёк.\n"
                                          f"Пример: MDwCMAofN9K4U8e9EPMzs57Asams2AFBen",
                'ExmoRUB': f"Курс: {user_curr} руб.\n"
                                          f"Покупка {trade_value} {key}\n"
                                          f"К оплате: {user_price} руб.\n",
                'Ethereum': f"Курс: {user_curr} руб.\n"
                                          f"Покупка {trade_value} {key}\n"
                                          f"К оплате: {user_price} руб.\n"
                                          f"Следующим сообщением отправьте нам ваш криптокошелёк.\n"
                                          f"Пример: 0x2Fe62eae2fB629808C94E55AF69fB373FD959980",
                'Bitcoin Cash': f"Курс: {user_curr} руб.\n"
                                          f"Покупка {trade_value} {key}\n"
                                          f"К оплате: {user_price} руб.\n"
                                          f"Следующим сообщением отправьте нам ваш криптокошелёк.\n"
                                          f"Пример: 3GncF7muEw1oayeuH33rxahdmtHSWoj4tw",
                }
    return messages[key]


def get_price_from_request(request):
    price = request[5].split(': ')[1]
    return float(price)


def change_request_comment_price(request, amount: float):
    price = get_price_from_request(request)
    price = round(price + amount, 2)
    if amount == ADV_PRIORITY_PRICE:
        request[5] = request[5].split(': ')[0] + f': {price} Комиссия повышенная'
    if amount == MAX_PRIORITY_PRICE:
        request[5] = request[5].split(': ')[0] + f': {price} Комиссия максимальная'
    return request[5]


def check_address(address):
    try:
        address = bytes(address, 'ascii')
        if coinaddr.validate('btc', address):
            return True
    except Exception:
        try:
            if coinaddr.validate('ltc', address):
                return True
        except Exception:
            try:
                if coinaddr.validate('bch', address):
                    return True
            except Exception:
                try:
                    if coinaddr.validate('eth', address):
                        return True
                except Exception:
                    return False


def parse_msg(msg):
    words = msg.text.split(" ")
    client_id = words.pop(0)
    message = get_message(words)
    return client_id, message


def get_message(words):
    m = ''
    for w in words:
        m += w + " "
    return m


def get_type(rq_type):
    spaces = rq_type.count(' ')
    base_type, curr_name, curr_price, payment_method = 'none', 'none', 'none', 'none'
    trade_value = ''
    sep = ''
    if spaces == 2:
        base_type, curr_name, curr_price = rq_type.split(" ")
    if spaces == 3:
        base_type, trade_value, curr_name, curr_price = rq_type.split(" ")
    if spaces == 4:
        base_type, trade_value, curr_name, curr_price, payment_method = rq_type.split(" ")

    if trade_value != '':
        sep = " "

    basic_types = {'trade': "Покупка",
                   'none': 'Произошла ошибка'}
    payment_methods = {'pay_sber': "Сбербанк",
                       'pay_yandex': "Яндекс.Деньги",
                       'pay_advcash': "AdvCash",
                       'pay_balance': "баланс бота",
                       'none': "не указана"}
    text = f"{basic_types[base_type]}{' ' + str(trade_value) + sep}{curr_name} по курсу: {curr_price}. " \
           f"Оплата: {payment_methods[payment_method]}"
    return text


def get_request_text(request):
    text = 'None'
    if request is not None:
        if "trade" in request[3]:
            text = show_request(request)
        elif 'replenish' in request[3]:
            text = show_replenish_request(request)
        elif 'return' in request[3]:
            text = show_return_request(request)
        elif 'help' in request[3]:
            text = show_help_request(request)
        return text


def show_replenish_request(request):
    statuses = {'B: wait for replenish value': 'бот ждёт от вас сумму, на которую вы хотите пополнить баланс',
                'B: wait_for_purchase': 'бот ждёт пока вы выберете способ оплаты',
                'user_confirmed': 'бот проверяет ваш платёж',
                'user_payed': 'бот пополнил ваш баланс',
                "B: waiting_for_priority": 'бот ждёт, пока вы выберите приоритет заявки'
                }
    print(request)
    rq_type = request[5]
    if rq_type is None:
        rq_type = 'Пополнение баланса'
    text = f'🖊 Уникальный № - {1000 + request[0]}\n' \
           f'🛒 Тип - {rq_type}\n' \
           f'🔄 Статус - {statuses[request[2]]}\n' \
           f'🕐 Когда создана - {request[4][:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request[1]}'
    return text


def show_help_request(request):
    statuses = {'H: wait_for_question': 'бот ждёт от вас вопрос, который вы хотите задать.',
                'H: user_wait_for_response': 'вы задали нам вопрос, ожидайте ответ.', }
    text = f'❓ Ваш вопрос - "{request[5]}"\n' \
           f'🖊 Уникальный № - {300 + request[0]}\n' \
           f'🔄 Статус - {statuses[request[2]]}\n' \
           f'🕐 Когда создан - {request[4]}\n' \
           f'🙋 Персональный идентификатор - {request[1]}'

    return text


def show_return_request(request):
    # (id integer PRIMARY KEY, telegram_id text, status text,
    # type text, when_created text, comment text, wallet text)
    statuses = {'R: wait for return value': 'бот ждёт от вас сумму для вывода',
                "R: wait for return requisites": 'бот ждёт от вас ваши реквизиты',
                'user_payed': 'бот отправляет вам валюту',
                "R: waiting_for_priority": 'бот ждёт, пока вы выберите приоритет заявки'}
    text = f'🖊 Уникальный № - {1000 + request[0]}\n' \
           f'🛒 Тип - {request[5]}\n' \
           f'🔄 Статус - {statuses[request[2]]}\n' \
           f'🕐 Когда создан - {request[4][:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request[1]}\n' \
           f'🏦 Реквизиты - {request[6]}\n'

    return text
    pass


def get_return_amount(request):
    return_amount = request[5].split(" ")[0]
    return int(return_amount)


def show_request(request):
    # (id integer PRIMARY KEY, telegram_id text, status text,
    # type text, when_created text, comment text, wallet text)
    statuses = {'T: wait for trade value': 'бот ждёт от вас количество криптоваллюты, которое вы хотите приобрести',
                'T: waiting_for_usr_wallet': 'бот ждёт от вас ваш криптокошелёк',
                'T: waiting_for_purchase': 'бот ждёт, пока вы подтвердите оплату',
                'user_confirmed': 'бот проверяет ваш платёж',
                'user_payed': 'бот отправляет вам криптоваллюту',
                'T: user_not_payed': 'бот не нашёл ваш платёж',
                "T: waiting_for_priority": 'бот ждёт, пока вы выберите приоритет заявки'}
    switcher = {
        'T: wait for trade value': '(указан курс без начисленных процентов)\n',
        'T: waiting_for_usr_wallet': '',
        'T: waiting_for_purchase': '',
        'user_confirmed': '',
        'user_payed': '',
        'T: user_payed': '',
        'T: user_not_payed': ''
    }

    warning = switcher[request[2]]

    text = f'🖊 Уникальный № - {1000 + request[0]}\n' \
           f'🛒 Тип - {get_type(request[3])}\n' \
           f'{warning}' \
           f'🔄 Статус - {statuses[request[2]]}\n' \
           f'🕐 Когда создан - {request[4][:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request[1]}\n' \
           f'🏦 Кошелёк, на который бот отправит криптовалюту - {request[6]}\n'

    return text


def get_balance_available_for_return(user):
    return user[2] - user[2] * 0.1


def get_status_discount(user):
    return DISCOUNTS[user[3]]


def get_user_price(curr, user, trade_value, key):
    user_price = float(curr) * float(trade_value)
    discount = get_status_discount(user)
    promotion = None
    if (user[6] + 1) % 10 == 0 and 1 < user_price < 3000:
        promotion = True
        percent = 1
    elif user[3] is True:  # if user is follower
        if 1 <= user_price <= 5000:
            percent = PERCENTS['under_5k_f'][key]
        elif 5000 < user_price < 10000:
            percent = PERCENTS['from_5k_to_10k_f'][key]
        elif 10000 <= user_price:
            percent = PERCENTS['above_10k_f'][key]
        else:
            return 'price is too low'
    else:  # if user is not follower
        if 1 <= user_price <= 2000:
            percent = PERCENTS['under_2k'][key]
        elif 2000 < user_price < 5000:
            percent = PERCENTS['from_2k_to_5k'][key]
        elif 5000 <= user_price < 10000:
            percent = PERCENTS['from_5k_to_10k'][key]
        elif 10000 <= user_price:
            percent = PERCENTS['above_10k'][key]
        else:
            return 'price is too low'
    user_curr = float(curr) + float(curr) * percent
    user_price = (user_curr) * float(trade_value)
    if key == "EXMOCoin":
        user_price -= 5
    return round(user_price, 2) - user_price * discount, user_curr, promotion


def get_trade_information(request) -> str:
    trade_information = request[5].split(', ')[0]
    trade_information += '\n' + request[5].split(',')[1]
    return trade_information


def get_fee(request):
    fee = request[5].split(": ")[1]
    return round(float(fee) * 0.003, 2)


def get_value(trade_value):
    if not trade_value.isalpha():
        if ',' in trade_value:
            return float(trade_value.replace(",", "."))
        else:
            return float(trade_value)
    return 0


def trade_value_is_acceptable(trade_value, key):
    if key == "ExmoRUB":
        return 5 < trade_value <= 100000
    if key == 'Bitcoin':
        return 0 < trade_value <= 0.02
    if key == 'Ethereum':
        return 0 < trade_value <= 0.02
    if key == 'Bitcoin Cash':
        return 0 < trade_value <= 0.02
    if key == 'Ethereum':
        return 0 < trade_value <= 0.02


def all_requests_is_none(c, user_id):
    trade_request, help_request, replenish_request, service_request, return_request = get_requests(c, user_id)
    return trade_request is None and replenish_request is None and help_request is None and service_request is \
           None and return_request is None


def return_value_is_acceptable(return_value) -> bool:
    return MIN_VALUE_FOR_RETURN <= return_value <= MAX_VALUE_FOR_RETURN


def replenish_value_is_acceptable(replenish_value):
    return 0 < replenish_value


def get_operators_list() -> list:
    operators = []
    with open(ADMINS_LIST, 'r') as f:
        for operator in f:
            operators.append(operator[:-1:])
    return operators


def get_admins_list() -> list:
    operators = []
    with open(OPERATORS_LIST, 'r') as f:
        for operator in f:
            operators.append(operator[:-1:])
    return operators


def add_admin(new_admin_id: str):
    new_admin_id = str(new_admin_id)
    with open(ADMINS_LIST, 'a') as f:
        f.write(new_admin_id + "\n")


def add_operator(new_operator_id: str):
    new_operator_id = str(new_operator_id)
    with open(OPERATORS_LIST, 'a') as f:
        f.write(new_operator_id + "\n")


def delete_admin(admin_id):
    admin_id = str(admin_id)
    admins = get_admins_list()
    with open(ADMINS_LIST, 'w') as f:
        for admin in admins:
            if admin != admin_id:
                continue
            else:
                f.write(admin_id + "\n")


def delete_operator(operator_id):
    operator_id = str(operator_id)
    operators = get_admins_list()
    with open(OPERATORS_LIST, 'w') as f:
        for operator in operators:
            if operator != operator_id:
                continue
            else:
                f.write(operator + "\n")


if __name__ == "__main__":
    pass
