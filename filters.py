from aiogram.types import Message

def check_name(message: Message) -> bool:
    if len(message.text.split()) in [2, 3]:
        return True
    return False




def get_str_numbers():
    res = '\n\n'
    dct = {
        'Viloyat shtabi': ['652231445', '652231447'],
        'Buxoro shahar': ['652230433', '652239883'],
        'Kogon shahar': '655243307',
        'Kogon shahar': '655425119',
        'Vobkent tuman': '653321175',
        'G\'ijduvon tuman': '655727003',
        'Jondor tuman': '655821792',
        'Kogon tuman': '655247536',
        'Qorak\'l tuman': '655652038',
        'Qorovulbozor tuman': '653641725',
        'Olot tuman': '653422431',
        'Peshko\' tuman': '653531145',
        'Romitan tuman': '655521837',
        'Shofirkon tuman': '655024076'
    }
    for a, b in dct.items():
        if isinstance(b, list):
            res += f'<b>{a}</b>:    {b[0]},   {b[1]}\n'
        else:
            res += f'<b>{a}</b>:     {b}\n'
    return res
            
        