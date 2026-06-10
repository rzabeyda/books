import json, re

with open('/root/books/webapp/books.json') as f:
    data = json.load(f)

fixed = 0
for b in data:
    label = b.get('world_reads_label', '')
    if not label or label.startswith('Тираж') or 'подписчик' in label or 'Новинка' in label:
        continue
    new_label = re.sub(r'\s*читателей$', '', label).strip()
    new_label = 'Тираж ' + new_label
    print(str(b['id']) + ': ' + repr(label) + ' -> ' + repr(new_label))
    b['world_reads_label'] = new_label
    fixed += 1

with open('/root/books/webapp/books.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

print('Fixed: ' + str(fixed))
