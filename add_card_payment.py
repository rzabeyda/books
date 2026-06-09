content = open('/root/books/webapp/index.html').read()

old = '''        <div class="sub-block sub-block--soon">
          <div class="sub-block-title">💳 Картой / Криптой</div>
          <div class="sub-soon-text">Скоро</div>
        </div>'''

new = '''        <div class="sub-block">
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

if old in content:
    content = content.replace(old, new)
    open('/root/books/webapp/index.html', 'w').write(content)
    print('Done')
else:
    print('NOT FOUND')
