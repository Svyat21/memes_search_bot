from states import DarkState
from buttons import choosing_analysis, confirm_input, button_commands

mem_scene = {
    'Добавить_мем': {
        'state': DarkState.STATE_OF_REST,
        'text_before': 'Отправьте в чат фото (нужно отправить именно как фото, не документ)',
        'text_after': 'Фото получено, напишите текст из фото или доверьтесь встроенному анализатору текста\n\n'
                      'P.S. Встроенный анализатор не всегда видит текст на фото',
        'button': choosing_analysis,
    },
    'Написать': {
        'state': DarkState.DESCRIPTION_STATE,
        'text_before': 'Введите текст с картинки',
        'text_after': 'Подтвердите корректность ввода',
        'button': confirm_input,
    },
    'Сканировать': {
        'state': DarkState.DESCRIPTION_STATE,
        'text_before': 'Сканирование с картинки часто получается с неожиданными символами. Скопируйте результат, '
                       'исправьте его и отправьте.',
    },
    'Найти_мем': {
        'state': DarkState.SEARCH_STATE,
        'text_before': 'Введите поисковой запрос',
        'button': None,
    },
}

DEFAULT_ANSWER = {
    'text': 'К сожалению, я бот и не понимаю всех ваших сообщений, выберите одну из следующих команд',
    'button': button_commands
}
