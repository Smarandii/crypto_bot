from models import User

TOKEN = '1111584809:AAHpcR7604kJstmh-k7w0qhApYret_P81g4'


class BotContent:
    BOT_TAG = 'crypto_bot_bot_bot'

    # STATUSES
    BASE_STATUS = 'Серебрянный'
    MEDIUM_STATUS = 'Золотой'
    ADVANCED_STATUS = 'Платиновый'

    # SPECIAL USERS FILES
    ADMINS_LIST = 'admins.txt'
    OPERATORS_LIST = 'operators.txt'

    # GROUP & CHANNEL ID'S
    GROUP = "-498679897"
    CHANNEL = "-1001461384160"

    # SUGGESTION URLS
    URLS = {'group': 'https://t.me/joinchat/JihjtQ9PzjsJBH2Uw2NxFg',
            'channel': 'https://t.me/joinchat/AAAAAFca8-DX0MYpg3nfNA'}

    # SPECIAL INFO FOR BOT
    RETURN_PERCENT = 0.9
    PERCENTS = {'under_5k_f': {'Bitcoin': 0.12,
                               'LiteCoin': 0.10,
                               'Ethereum': 0.11,
                               'Bitcoin Cash': 0.11,
                               'ExmoRUB': 0.10
                               },
                'from_5k_to_10k_f': {'Bitcoin': 0.11,
                                     'LiteCoin': 0.09,
                                     'Ethereum': 0.11,
                                     'Bitcoin Cash': 0.11,
                                     'ExmoRUB': 0.09
                                     },
                'above_10k_f': {'Bitcoin': 0.10,
                                'LiteCoin': 0.08,
                                'Ethereum': 0.10,
                                'Bitcoin Cash': 0.10,
                                'ExmoRUB': 0.085
                                },
                'under_2k': {
                            'Bitcoin': 0.13,
                            'LiteCoin': 0.11,
                            'Ethereum': 0.12,
                            'Bitcoin Cash': 0.12,
                            'ExmoRUB': 0.10
                             },
                'from_2k_to_5k': {
                            'Bitcoin': 0.12,
                            'LiteCoin': 0.11,
                            'Ethereum': 0.11,
                            'Bitcoin Cash': 0.12,
                            'ExmoRUB': 0.10
                                 },
                'from_5k_to_10k': {
                            'Bitcoin': 0.115,
                            'LiteCoin': 0.105,
                            'Ethereum': 0.105,
                            'Bitcoin Cash': 0.115,
                            'ExmoRUB': 0.095
                                 },
                'above_10k': {
                    'Bitcoin': 0.11,
                    'LiteCoin': 0.10,
                    'Ethereum': 0.10,
                    'Bitcoin Cash': 0.11,
                    'ExmoRUB': 0.09
                             },
                }
    DISCOUNTS = {'Серебрянный': 0,
                 'Золотой': 0.005,
                 'Платиновый': 0.01}
    EXAMPLE = {'ExmoRUB': '1000',
               'Bitcoin': '0.001456 BTC\nили\n1000 RUB',
               'Ethereum': '0.001432',
               'Bitcoin Cash': '0.001687',
               'LiteCoin': '0.00987 LTC\nили\n1000 RUB'}

    SBER_REQUISITES = "sbersbersbersbersbersber"
    YANDEX_REQUISITES = "yayayayayayayayayayaya"
    ADVCASH_REQUISITES = "advadvadvadvadvadvadv"
    TO_ACHIEVE_MEDIUM_STATUS = 40
    TO_ACHIEVE_ADVANCED_STATUS = 100
    MIN_VALUE_FOR_RETURN = 100
    MAX_VALUE_FOR_RETURN = 1000
    ADV_PRIORITY_PRICE = 80
    MAX_PRIORITY_PRICE = 230

    MESSAGES = {
        'channel_suggest': "❓ Ещё не подписаны на наш канал и не в групповом чате?\n"
                           "📈 А зря! Всем подписавшимся - более выгодный процент обмена.",
        'partnership': '👥 👥 0.3% от суммы выданной валюты\n🤝 Приглашено пользователей: {}\n💰 Заработано: {} руб.\n'
                       '💳 Доступно на вывод: {} руб.\n* для вывода обращайтесь в тех. поддержку\n➖➖➖➖➖➖➖➖\n'
                       '🔗 Ваша партнерская ссылка:\n{}',
        'choose_crypto': '⬇️ Выберите криптовалюту',
        'replenish_balance': "На данный момент ваш баланс: {} руб.\n",
        'current_balance': "Вы {} пользователь!\nНа данный момент ваш баланс: {} руб.\n",
        'menu_arrow': "⬇️Меню",
        'personal_cabinet': 'Личный кабинет',
        'start_trade_rq': '💰Введи нужную сумму в RUB или в {}\n'
                          'Например: {}',
        'where_return': 'Выберите куда возвращать деньги',
        'return_failure': 'Не удалось отправить заявку.\nНа вашем счёте недостаточно средств.\n'
                          'Доступно для вывода: {} руб.\n'
                          'Минимальная сумма вывода: {}\n'
                          'Максимальная сумма вывода {}\n',
        'confirm_return_requisites': 'Деньги с вашего баланса будут отправлены сюда:\n'
                                     '{}',
        'confirm_user_question': "⏰ Ответ на ваш вопрос будет в чате с ботом, ожидайте!",
        'confirm_user_replenish': "Пополнение баланса на сумму: {} ₽",
        'unacceptable_value': 'Недопустимое значение, попробуйте снова',
        'choose_payment_method': 'Выберите способ оплаты!',
        'promotion_message': 'Это ваша {} заявка, она будет беспроцентной!',
        'confirm_user_wallet': 'После оплаты, криптоваллюта будет отправлена на этот кошелёк:\n{}',
        'unacceptable_wallet': '🙅‍♂️ Такого кошелька не существует! Попробуйте ещё раз.',
        'choose_commission': 'Выберите желаемую комиссию',
        'message_from_operator_notification': 'Вам написал сотрудник тех. поддержки: {}',
        'message_sent_notification': 'Сообщение отправлено!',
        'question_answered_notification': 'На ваш вопрос ответили!\nОтвет: {}\nВопрос автоматически закрыт',
        'wait_for_operator_answer': "Отправьте ответ на вопрос следующим сообщением!",




        'confirm_user_balance_unreplenish': 'Вы уверены, что хотите списать с баланса этого пользователя '
                                            '{} сумму {}?',
        'confirm_user_balance_replenish': 'Вы уверены, что хотите пополнить баланс этого пользователя?\n'
                                          '{} на сумму {}?',
        'confirm_send_answer': 'Вы уверены, что хотите отправить этот ответ пользователю?\n{}',
        'confirm_send_message': 'Вы уверены, что хотите отправить это сообщение пользователю?\n{}',
        'send_message_to_user': "Отправьте персональный идентификатор "
                                "пользователя и ваше сообщение следующим сообщением!\n"
                                "Вот так:\n"
                                "id message",
        'user_balance_unreplenish': "Отправьте персональный идентификатор "
                                    "пользователя и сумму снятия следующим сообщением!\n"
                                    "Вот так:\n"
                                    "id amount",
        'user_balance_replenish': "Отправьте персональный идентификатор "
                                  "пользователя и сумму пополнения следующим сообщением!\n"
                                  "Вот так:\n"
                                  "id amount",
        'delete_admin': 'Админ успешно удалён!',
        'delete_operator': 'Оператор успешно удалён!',
        'new_operator': 'Новый оператор успешно добавлен!',
        'new_admin': 'Новый админ успешно добавлен!',
        'request_exist_warning': 'У вас уже есть заявка, желаете её отменить?'
    }

    def get_status_discount(self, user: User):
        return self.DISCOUNTS[user.status]

    def get_user_price(self, curr_price, user: User, trade_value, key):
        user_price = float(curr_price) * float(trade_value)
        discount = self.get_status_discount(user)
        promotion = None
        if (user.quantity_of_trades + 1) % 10 == 0 and 1 < user_price < 3000:
            promotion = True
            percent = 1
        elif user.is_follower is True:
            if 1 <= user_price <= 5000:
                percent = self.PERCENTS['under_5k_f'][key]
            elif 5000 < user_price < 10000:
                percent = self.PERCENTS['from_5k_to_10k_f'][key]
            elif 10000 <= user_price:
                percent = self.PERCENTS['above_10k_f'][key]
            else:
                return 'price is too low'
        else:  # if user is not follower
            if 1 <= user_price <= 2000:
                percent = self.PERCENTS['under_2k'][key]
            elif 2000 < user_price < 5000:
                percent = self.PERCENTS['from_2k_to_5k'][key]
            elif 5000 <= user_price < 10000:
                percent = self.PERCENTS['from_5k_to_10k'][key]
            elif 10000 <= user_price:
                percent = self.PERCENTS['above_10k'][key]
            else:
                return 'price is too low'
        user_curr = float(curr_price) + float(curr_price) * percent
        user_price = (user_curr) * float(trade_value)
        if key == "EXMOCoin":
            user_price -= 5
        return round(user_price, 2) - user_price * discount, user_curr, promotion

    def get_prepayment_message(self, user_curr, trade_value, user_price, key) -> str:
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