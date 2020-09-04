
from content import BotContent
from models import Request


def get_price_from_request(request: Request):
    price = request.comment.split(': ')[1]
    return float(price)


def change_request_comment_price(request: Request, amount: float):
    price = get_price_from_request(request)
    price = round(price + amount, 2)
    if amount == 0:
        request.comment = request.comment + ' Обычная комиссия'
    if amount == BotContent.ADV_PRIORITY_PRICE:
        request.comment = request.comment.split(': ')[0] + f': {price} Комиссия повышенная'
    if amount == BotContent.MAX_PRIORITY_PRICE:
        request.comment = request.comment.split(': ')[0] + f': {price} Комиссия максимальная'
    return request.comment


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


def get_request_text(request):
    # TODO переделать
    text = 'None'
    if request is not None:
        if "trade" in request.type:
            text = show_request(request)
        elif 'replenish' in request.type:
            text = show_replenish_request(request)
        elif 'return' in request.type:
            text = show_return_request(request)
        elif 'help' in request.type:
            text = show_help_request(request)
        return text


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


def get_trade_information(request: Request) -> str:
    trade_information = request.comment.split(', ')[0]
    trade_information += '\n' + request.comment.split(',')[1]
    return trade_information


def get_fee(request):
    fee = request[5].split(": ")[1]
    return round(float(fee) * 0.003, 2)


def get_operators_list() -> list:
    operators = []
    with open(BotContent.ADMINS_LIST, 'r') as f:
        for operator in f:
            operators.append(operator[:-1:])
    return operators


def get_admins_list() -> list:
    operators = []
    with open(BotContent.OPERATORS_LIST, 'r') as f:
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
