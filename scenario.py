from states import AddMem, SearchMem
from buttons import choosing_analysis, confirm_input, button_commands

search_mem = {
    'Найти_мем': {
        'state': SearchMem.STATE_1,
        'text_before': 'Введите поисковой запрос',
        'button': None,
    },
}

add_mem = {
    'Добавить_мем': {
        'state': AddMem.STATE_1,
        'text_before': 'Отправьте в чат фото (нужно отправить именно как фото, не документ)',
        'text_after': 'Фото получено, напишите текст из фото или доверьтесь встроенному анализатору текста\n\n'
                      'P.S. Встроенный анализатор не всегда видит текст на фото',
        'button': choosing_analysis,
    },
    'Написать': {
        'state': AddMem.STATE_2,
        'text_before': 'Введите текст с картинки',
        'text_after': 'Подтвердите корректность ввода',
        'button': confirm_input,
    },
    'Сканировать': {
        'state': AddMem.STATE_2,
        'text_before': 'Сканирование с картинки часто получается с неожиданными символами. Скопируйте результат, '
                       'исправьте его и отправьте.',
    }
}

DEFAULT_ANSWER = {
    'text': 'К сожалению, я бот и не понимаю всех ваших сообщений, выберите одну из следующих команд',
    'button': button_commands
}
