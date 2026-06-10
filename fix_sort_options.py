content = open('/root/books/webapp/app.js').read()
old = """  { key: 'recommended', label: 'Рекомендованные' },
  { key: 'newer',       label: 'Новее → Старее' },
  { key: 'older',       label: 'Старее → Новее' },
  { key: 'az',          label: 'По названию А → Я' },
  { key: 'za',          label: 'По названию Я → А' },
  { key: 'author',      label: 'По автору А → Я' },
  { key: 'authorza',    label: 'По автору Я → А' },
  { key: 'read',        label: 'Прочитанные' },
  { key: 'unread',      label: 'Не прочитанные' },"""
new = """  { key: 'recommended', label: 'Рекомендованные' },
  { key: 'read',        label: 'Прочитанные' },
  { key: 'unread',      label: 'Не прочитанные' },
  { key: 'newer',       label: 'Новее → Старее' },
  { key: 'older',       label: 'Старее → Новее' },
  { key: 'az',          label: 'По названию А → Я' },
  { key: 'za',          label: 'По названию Я → А' },
  { key: 'author',      label: 'По автору А → Я' },
  { key: 'authorza',    label: 'По автору Я → А' },"""
content = content.replace(old, new)
open('/root/books/webapp/app.js', 'w').write(content)
print('done')
