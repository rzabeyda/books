import paramiko

key = paramiko.RSAKey.from_private_key_file(r'C:\Users\rzabe\.ssh\id_rsa')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('84.200.33.70', username='root', pkey=key)

sftp = client.open_sftp()

files = [
    'freud_dreams.jpg',
    'freud_intro.jpg',
    'freud_ego.jpg',
    'freud_psychopathology.jpg',
    'freud_pleasure.jpg',
]

for f in files:
    sftp.put(f'C:/books/books/{f}', f'/root/books/webapp/books/{f}')
    print('uploaded:', f)

sftp.close()
client.close()
print('all done')
