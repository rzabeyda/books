import paramiko

HOST = '84.200.33.70'
KEY  = r'C:\Users\rzabe\.ssh\id_rsa'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username='root', key_filename=KEY)

sftp = client.open_sftp()
path = '/root/books/webapp/index.html'

with sftp.open(path, 'r') as f:
    html = f.read().decode('utf-8')

stars_block = '''        <div class="sub-block">
          <div class="sub-block-title">⭐ Telegram Stars</div>
          <div class="sub-plans">
            <button class="sub-plan" onclick="selectPlan(this,'month')">
              <div class="sub-plan-name">Месяц</div>
              <div class="sub-plan-price">333 ⭐</div>
              <div class="sub-plan-usd">≈ $5</div>
            </button>
            <button class="sub-plan sub-plan--active" onclick="selectPlan(this,'year')">
              <div class="sub-plan-badge">Выгодно</div>
              <div class="sub-plan-name">Год</div>
              <div class="sub-plan-price">3 333 ⭐</div>
              <div class="sub-plan-usd">≈ $50</div>
            </button>
            <button class="sub-plan" onclick="selectPlan(this,'forever')">
              <div class="sub-plan-name">Навсегда</div>
              <div class="sub-plan-price">6 667 ⭐</div>
              <div class="sub-plan-usd">≈ $100</div>
            </button>
          </div>
          <button class="sub-pay-btn" id="sub-pay-btn" onclick="paySelected()">Оплатить Stars</button>
        </div>'''

card_block = '''        <div class="sub-block">
          <div class="sub-block-title">💳 Картой / Криптой</div>
          <div class="sub-plans">
            <a class="sub-plan" href="https://web.tribute.tg/p/xkg" target="_blank">
              <div class="sub-plan-name">Месяц</div>
              <div class="sub-plan-price">$5</div>
              <div class="sub-plan-usd">Картой или криптой</div>
            </a>
            <a class="sub-plan sub-plan--active" href="https://web.tribute.tg/p/xry" target="_blank">
              <div class="sub-plan-badge">Выгодно</div>
              <div class="sub-plan-name">Год</div>
              <div class="sub-plan-price">$50</div>
              <div class="sub-plan-usd">Картой или криптой</div>
            </a>
            <a class="sub-plan" href="https://web.tribute.tg/p/xrz" target="_blank">
              <div class="sub-plan-name">Навсегда</div>
              <div class="sub-plan-price">$100</div>
              <div class="sub-plan-usd">Картой или криптой</div>
            </a>
          </div>
        </div>'''

original = stars_block + '\n\n' + card_block
swapped  = card_block  + '\n\n' + stars_block

if original in html:
    html = html.replace(original, swapped)
    with sftp.open(path, 'w') as f:
        f.write(html.encode('utf-8'))
    print('OK: blocks swapped')
else:
    print('ERROR: pattern not found')
    # Debug
    print('Stars found:', stars_block in html)
    print('Card found:', card_block in html)

sftp.close()
client.close()
