from aiogram.types import Message

def check_name(message: Message) -> bool:
    if len(message.text.split()) in [2, 3]:
        return True
    return False




def get_str_numbers():
    res = '\n'
    dct = {
        'Вилоят штаби': ['+998652231445', '+998652231447'],
        'Бухоро шаҳар': ['+998652230433', '+998652239883'],
        'Когон шаҳар': '+998655243307',
        'Бухоро тумани': '+998655425119',
        'Вобкент тумани': '+998653321175',
        'Ғиждувон тумани': '+998655727003',
        'Жондор тумани': '+998655821792',
        'Когон тумани': '+998655247536',
        'Қоракўл тумани': '+998655652038',
        'Қоровулбозор тумани': '+998653641725',
        'Олот тумани': '+998653422431',
        'Пешку тумани': '+998653531145',
        'Ромитан тумани': '+998655521837',
        'Шофиркон тумани': '+998655024076'
    }
    for a, b in dct.items():
        c = (a +':').ljust(20, " ")
        if isinstance(b, list):
            res += f'{c}{b[0]}, {b[1]}\n'
        else:
            res += f'{c}{b}\n'
    print(res)
    return res
            
