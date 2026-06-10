import paramiko

key = paramiko.RSAKey.from_private_key_file(r'C:\Users\rzabe\.ssh\id_rsa')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('84.200.33.70', username='root', pkey=key)

sftp = client.open_sftp()

import os
desktop = os.path.expanduser('~') + r'\Desktop'

files = {
    'One Hundred Years of Solitude.jpg': 'markes_sto_let.jpg',
    'Love in the Time of Cholera.jpg': 'markes_lyubov.jpg',
    'The Autumn of the Patriarch.jpg': 'markes_osen.jpg',
    'Macbeth.jpg': 'shakespeare_macbeth.jpg',
    'Resurrection.jpg': 'tolstoy_voskresenie.jpg',
    'A Farewell to Arms.jpg': 'hemingway_farewell.jpg',
    'For Whom the Bell Tolls.jpg': 'hemingway_kolokol.jpg',
    'Great Expectations.jpg': 'dickens_expectations.jpg',
    'Oliver Twist.jpg': 'dickens_oliver.jpg',
    'David Copperfield.jpg': 'dickens_copperfield.jpg',
}

for src, dst in files.items():
    sftp.put(f'{desktop}\\{src}', f'/root/books/webapp/books/{dst}')
    print('uploaded:', dst)

sftp.close()
client.close()
print('all done')
