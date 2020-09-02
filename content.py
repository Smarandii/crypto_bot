TOKEN = '1111584809:AAHpcR7604kJstmh-k7w0qhApYret_P81g4'
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




    'delete_admin': 'Админ успешно удалён!',
    'delete_operator': 'Оператор успешно удалён!',
    'new_operator': 'Новый оператор успешно добавлен!',
    'new_admin': 'Новый админ успешно добавлен!',
    'request_exist_warning': 'У вас уже есть заявка, желаете её отменить?'
}