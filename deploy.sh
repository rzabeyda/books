#!/bin/bash
SERVER="root@84.200.33.70"
KEY="~/.ssh/id_rsa"

echo "==> Деплой веб-приложения..."
ssh -i $KEY $SERVER "mkdir -p /root/books/webapp/covers"
scp -i $KEY C:/books/index.html  $SERVER:/root/books/webapp/
scp -i $KEY C:/books/style.css   $SERVER:/root/books/webapp/
scp -i $KEY C:/books/app.js      $SERVER:/root/books/webapp/
scp -i $KEY C:/books/books.json  $SERVER:/root/books/webapp/

echo "==> Деплой иконок..."
scp -i $KEY C:/books/icons/book.png    $SERVER:/root/books/webapp/
scp -i $KEY C:/books/icons/mybook.jpg  $SERVER:/root/books/webapp/
scp -i $KEY C:/books/icons/ok.png      $SERVER:/root/books/webapp/
scp -i $KEY C:/books/icons/sapiens.jpg $SERVER:/root/books/webapp/
scp -i $KEY C:/books/icons/atom.jpg    $SERVER:/root/books/webapp/
scp -i $KEY C:/books/icons/human.jpg   $SERVER:/root/books/webapp/

echo "==> Деплой бекенда и бота..."
scp -i $KEY C:/books/server.py          $SERVER:/root/books/
scp -i $KEY C:/books/bot.py             $SERVER:/root/books/
scp -i $KEY C:/books/.env               $SERVER:/root/books/

echo "==> Деплой конфигов..."
scp -i $KEY C:/books/nginx.conf              $SERVER:/etc/nginx/sites-available/books
scp -i $KEY C:/books/books_bot.service       $SERVER:/etc/systemd/system/
scp -i $KEY C:/books/books_server.service    $SERVER:/etc/systemd/system/

echo "==> Применяем nginx и сервисы..."
ssh -i $KEY $SERVER "
  ln -sf /etc/nginx/sites-available/books /etc/nginx/sites-enabled/books &&
  nginx -t && systemctl reload nginx &&
  systemctl daemon-reload &&
  systemctl enable books_server &&
  systemctl restart books_server &&
  systemctl restart books_bot.service
"

echo "==> Готово!"
