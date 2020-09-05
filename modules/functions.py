from datetime import timedelta, datetime

from modules.models import Request, User


def time_is_come(last_cur_update):
    day, time = str(datetime.now()).split(" ")
    hour, minute, sec = time.split(":")

    last_cur_updt_day, last_cur_updt_time = last_cur_update.split(" ")
    last_cur_updt_hour, last_cur_updt_minute, last_cur_updt_sec = last_cur_updt_time.split(":")

    return day >= last_cur_updt_day and int(minute) - int(last_cur_updt_minute) >= 5 and \
           round(float(sec)) >= round(float(last_cur_updt_sec))


def get_request_from_db(request: tuple) -> Request:
    if len(request) == 7:
        request = Request(
              db_id=request[0],
              telegram_id=request[1],
              status=request[2],
              rq_type=request[3],
              when_created=request[4],
              comment=request[5],
              wallet=request[6])
    elif len(request) == 6:
        request = Request(
            telegram_id=request[0],
            status=request[1],
            rq_type=request[2],
            when_created=request[3],
            comment=request[4],
            wallet=request[5])
    return request


def get_user_from_db(user: tuple) -> User:
    user = User(db_id=user[0],
                telegram_id=user[1],
                balance=user[2],
                status=user[3],
                is_follower=user[4],
                invited_by=user[5],
                quantity_of_trades=user[6],
                earned_from_partnership=user[7]
                )
    return user


def request_time_is_done(request_time):
    # request_time = 2020-08-06 18:33:02.276834
    tdelta = timedelta(hours=1)
    now = datetime.now()

    return request_time < str(now - tdelta)


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
    rq_type = request.comment
    if rq_type is None:
        rq_type = 'Пополнение баланса'
    text = f'🖊 Уникальный № - {1000 + request.db_id}\n' \
           f'🛒 Тип - {rq_type}\n' \
           f'🔄 Статус - {statuses[request.status]}\n' \
           f'🕐 Когда создана - {request.when_created[:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request.telegram_id}'
    return text


def show_help_request(request):
    statuses = {'H: wait_for_question': 'бот ждёт от вас вопрос, который вы хотите задать.',
                'H: user_wait_for_response': 'вы задали нам вопрос, ожидайте ответ.', }
    text = f'❓ Ваш вопрос - "{request.comment}"\n' \
           f'🖊 Уникальный № - {300 + request.db_id}\n' \
           f'🔄 Статус - {statuses[request.status]}\n' \
           f'🕐 Когда создан - {request.when_created}\n' \
           f'🙋 Персональный идентификатор - {request.telegram_id}'

    return text


def show_return_request(request):
    # (id integer PRIMARY KEY, telegram_id text, status text,
    # type text, when_created text, comment text, wallet text)
    statuses = {'R: wait for return value': 'бот ждёт от вас сумму для вывода',
                "R: wait for return requisites": 'бот ждёт от вас ваши реквизиты',
                'user_payed': 'бот отправляет вам валюту',
                "R: waiting_for_priority": 'бот ждёт, пока вы выберите приоритет заявки'}
    text = f'🖊 Уникальный № - {1000 + request.db_id}\n' \
           f'🛒 Тип - {request.comment}\n' \
           f'🔄 Статус - {statuses[request.status]}\n' \
           f'🕐 Когда создан - {request.when_created[:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request.telegram_id}\n' \
           f'🏦 Реквизиты - {request.wallet}\n'

    return text


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
    return_amount = request.comment.split(" ")[0]
    return int(return_amount)


def show_request(request):
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

    warning = switcher[request.status]

    text = f'🖊 Уникальный № - {1000 + request.db_id}\n' \
           f'🛒 Тип - {get_type(request.type)}\n' \
           f'{warning}' \
           f'🔄 Статус - {statuses[request.status]}\n' \
           f'🕐 Когда создан - {request.when_created[:19:].replace("-", ".")}\n' \
           f'🙋 Персональный идентификатор - {request.telegram_id}\n' \
           f'🏦 Кошелёк, на который бот отправит криптовалюту - {request.wallet}\n'

    return text


def get_trade_information(request: Request) -> str:
    trade_information = request.comment.split(', ')[0]
    trade_information += '\n' + request.comment.split(',')[1]
    return trade_information


if __name__ == "__main__":
    pass
