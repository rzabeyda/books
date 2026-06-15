#!/bin/bash
SSH_KEY=~/.ssh/id_rsa
SERVER=root@84.200.33.70
REMOTE=/root/books/webapp/

scp -i $SSH_KEY index.html app.js style.css $SERVER:$REMOTE
echo "✅ Frontend deployed to $REMOTE"

if [ "$1" = "--bot" ]; then
  ssh -i $SSH_KEY $SERVER "systemctl restart books_bot"
  echo "✅ Bot restarted"
fi
