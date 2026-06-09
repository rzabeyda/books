content = open('/etc/nginx/sites-enabled/books.zabeyda.lol').read()

old = '''    location /subscription/ {
        proxy_pass http://127.0.0.1:8081;
    }'''

new = '''    location /subscription/ {
        proxy_pass http://127.0.0.1:8081;
    }

    location /suggest {
        proxy_pass http://127.0.0.1:8081/suggest;
    }

    location /tribute-webhook {
        proxy_pass http://127.0.0.1:8081/tribute-webhook;
    }'''

if old in content:
    content = content.replace(old, new)
    open('/etc/nginx/sites-enabled/books.zabeyda.lol', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
