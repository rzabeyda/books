import json, sys

with open('/root/books/webapp/books.json', 'r') as f:
    data = json.load(f)

missing = [
    {"id":52,"title":"Бхагавад-гита","author":"Вьяса","cover":"bhagavad.jpg","world_reads":500000000,"world_reads_label":"500 млн+ копий","genre":"religion","thoughts":[]},
    {"id":53,"title":"Типитака","author":"Будда","cover":"tripitaka.jpg","world_reads":300000000,"world_reads_label":"300 млн+ копий","genre":"religion","thoughts":[]},
    {"id":54,"title":"Капитал","author":"Карл Маркс","cover":"capital.jpg","world_reads":10000000,"world_reads_label":"10 млн+ копий","genre":"politics","thoughts":[]},
    {"id":55,"title":"Манифест Коммунистической партии","author":"Карл Маркс, Фридрих Энгельс","cover":"manifest.jpg","world_reads":500000000,"world_reads_label":"500 млн+ копий","genre":"politics","thoughts":[]},
    {"id":56,"title":"Происхождение видов","author":"Чарльз Дарвин","cover":"proishozhdenie_vidov.jpg","world_reads":5000000,"world_reads_label":"5 млн+ копий","genre":"nonfiction","thoughts":[]},
    {"id":57,"title":"Цитатник Мао Цзэдуна","author":"Мао Цзэдун","cover":"mao.jpg","world_reads":900000000,"world_reads_label":"900 млн+ копий","genre":"politics","thoughts":[]},
    {"id":58,"title":"1984","author":"Джордж Оруэлл","cover":"1984.jpg","world_reads":30000000,"world_reads_label":"30 млн+ копий","genre":"fiction","thoughts":[]},
    {"id":59,"title":"Искусство войны","author":"Сунь-цзы","cover":"iskusstvo_voiny.jpg","world_reads":10000000,"world_reads_label":"10 млн+ копий","genre":"nonfiction","thoughts":[]}
]

existing_ids = {b['id'] for b in data}
added = 0
for b in missing:
    if b['id'] not in existing_ids:
        data.append(b)
        added += 1

data.sort(key=lambda x: x['id'])

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',',':'))

sys.stdout.buffer.write(f'OK: {len(data)} книг, добавлено {added}\n'.encode())
