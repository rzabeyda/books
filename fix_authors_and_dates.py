import json

def fmt(d):
    """Convert '10 июля 1856' to '10.07.1856'"""
    months = {
        'января':1,'февраля':2,'марта':3,'апреля':4,'мая':5,'июня':6,
        'июля':7,'августа':8,'сентября':9,'октября':10,'ноября':11,'декабря':12
    }
    parts = d.strip().split()
    if len(parts) == 3:
        day, mon, year = parts
        m = months.get(mon)
        if m:
            return f"{int(day):02d}.{m:02d}.{year}"
    return d

def fmt_range(s):
    """Convert full date string with optional death date"""
    if ' — ' in s:
        a, b = s.split(' — ', 1)
        return fmt(a) + ' — ' + fmt(b)
    # Check if it's already in DD.MM.YYYY format or special text
    if s[0].isdigit() and '.' not in s[:3]:
        return fmt(s)
    return s

# author = profession for история успеха
professions = {
    168: "Изобретатель и учёный",
    169: "Автомобильный магнат",
    170: "Изобретатель",
    171: "Изобретатель телефона",
    172: "Основатель ВКонтакте и Telegram",
    173: "Президент России",
    174: "Основатель МММ",
    175: "Сооснователь Google",
    176: "Основатель Facebook",
    177: "Основатель Microsoft",
    178: "Основатель Apple",
    179: "Основатель KFC",
    180: "Модельер",
    181: "Основатель Louis Vuitton",
    182: "Основатель Starbucks",
    183: "Основатель IKEA",
    184: "Телеведущая и медиамагнат",
    185: "Модельер",
    186: "Писательница",
    187: "Основатель Alibaba",
    188: "Предприниматель",
    189: "Основатель WhatsApp",
    190: "Основательница Estée Lauder",
    191: "Основатель Nike",
    192: "Основатель Walmart",
    193: "Рэпер и блогер",
    194: "Певица и телеведущая",
    195: "Блогер и предприниматель",
    196: "Рэпер и блогер",
    197: "Блогер",
    198: "Телеведущая и блогер",
    199: "Журналист и телеведущая",
    200: "Певица",
    201: "Блогер",
    202: "Психолог и блогер",
    203: "Журналист и блогер",
    204: "Блогер",
    205: "Блогер и урбанист",
    206: "Техноблогер",
    207: "Дизайнер",
    208: "Комик и блогер",
    209: "Кинокритик и блогер",
    210: "Блогер",
    211: "Актёр и блогер",
    212: "Рэпер и блогер",
    213: "Блогер",
    214: "Блогер о суперкарах",
    215: "Основатель Тинькофф Банка",
    216: "Комик",
    217: "Комик и актёр",
    218: "Блогер",
    219: "Рейв-группа",
    220: "Рэпер",
    221: "Поэт и комик",
    222: "Комик",
    223: "Комик",
    224: "Комик",
    225: "Комик и телеведущий",
    226: "Детский блогер",
}

with open('/root/books/webapp/books.json') as f:
    books = json.load(f)

updated = 0
for b in books:
    bid = b.get('id')
    if bid in professions:
        b['author'] = professions[bid]
        updated += 1
    if b.get('born') and b['genre'] == 'история успеха':
        b['born'] = fmt_range(b['born'])

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print('Updated:', updated)

# Verify a few
with open('/root/books/webapp/books.json') as f:
    books = json.load(f)
for b in books:
    if b.get('id') in [178, 173, 203]:
        print(b['title'], '|', b['author'], '|', b.get('born',''))
