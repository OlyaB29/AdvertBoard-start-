  # -- coding: utf-8 --

characters = {
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'JO',
    'Ж': 'ZH',
    'З': 'Z',
    'И': 'I',
    'Й': 'J',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'KH',
    'Ц': 'TS',
    'Ч': 'CH',
    'Ш': 'SH',
    'Щ': 'SCH',
    'Ъ': '',
    'Ы': 'Y',
    'Ь': '',
    'Э': 'E',
    'Ю': 'JU',
    'Я': 'JA',
    ' ': '_'
}

def transliteration(text):
   # Транслитерация русского в английский
    converted_text = '{}'.format(text).upper()
    return ''.join(characters.get(x, x) for x in converted_text).lower()