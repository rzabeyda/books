content = open('/etc/nginx/sites-enabled/books').read()

old = '''    location /subscription/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }'''

new = '''    location /subscription/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }

    location /suggest {
        proxy_pass http://127.0.0.1:5000/suggest;
        proxy_set_header Host $host;
    }

    location /tribute-webhook {
        proxy_pass http://127.0.0.1:5000/tribute-webhook;
        proxy_set_header Host $host;
    }'''

if old in content:
    content = content.replace(old, new)
    open('/etc/nginx/sites-enabled/books', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
