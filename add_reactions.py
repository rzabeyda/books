
# 1. Patch server.py — add reactions endpoint
with open('/root/books/server.py', 'r') as f:
    s = f.read()

# Add REACTIONS_FILE constant after SUBS_FILE
old = "SUBS_FILE = '/root/books/subscriptions.json'"
new = "SUBS_FILE = '/root/books/subscriptions.json'\nREACTIONS_FILE = '/root/books/reactions.json'"
s = s.replace(old, new, 1)

# Add load/save reactions after save_reads
old = "def save_reads(data):\n    with open(READS_FILE, 'w') as f:\n        json.dump(data, f)"
new = (
    "def save_reads(data):\n    with open(READS_FILE, 'w') as f:\n        json.dump(data, f)\n\n"
    "def load_reactions():\n"
    "    try:\n"
    "        with open(REACTIONS_FILE, 'r') as f:\n"
    "            return json.load(f)\n"
    "    except Exception:\n"
    "        return {}\n\n"
    "def save_reactions(data):\n"
    "    with open(REACTIONS_FILE, 'w') as f:\n"
    "        json.dump(data, f)"
)
s = s.replace(old, new, 1)

# Add GET /reactions endpoint
old = "        elif path.startswith('/subscription/'):"
new = (
    "        elif path == '/reactions':\n"
    "            self.send_json(200, load_reactions())\n"
    "        elif path.startswith('/subscription/'):"
)
s = s.replace(old, new, 1)

# Add POST /react/<id>/<type> endpoint
old = "        elif path == '/suggest':"
new = (
    "        elif path.startswith('/react/'):\n"
    "            parts = path.split('/')\n"
    "            if len(parts) == 4:\n"
    "                book_id, rtype = parts[2], parts[3]\n"
    "                if rtype in ('up', 'down'):\n"
    "                    reactions = load_reactions()\n"
    "                    if book_id not in reactions:\n"
    "                        reactions[book_id] = {'up': 0, 'down': 0}\n"
    "                    reactions[book_id][rtype] = reactions[book_id].get(rtype, 0) + 1\n"
    "                    save_reactions(reactions)\n"
    "                    self.send_json(200, reactions[book_id])\n"
    "                else:\n"
    "                    self.send_json(400, {'error': 'invalid type'})\n"
    "            else:\n"
    "                self.send_json(400, {'error': 'invalid path'})\n"
    "        elif path == '/suggest':"
)
s = s.replace(old, new, 1)

with open('/root/books/server.py', 'w') as f:
    f.write(s)

print('server.py patched OK')

# 2. Patch app.js — load reactions, show buttons
with open('/root/books/webapp/app.js', 'r') as f:
    js = f.read()

# Add reactions state after readBooks
old = "var readBooks = new Set(JSON.parse(localStorage.getItem('readBooks') || '[]'));"
new = (
    "var readBooks = new Set(JSON.parse(localStorage.getItem('readBooks') || '[]'));\n"
    "var allReactions = {};\n"
    "var myVotes = JSON.parse(localStorage.getItem('myVotes') || '{}');"
)
js = js.replace(old, new, 1)

# Load reactions in init — find where allBooks is fetched
old = "allBooks = await response.json();"
new = (
    "allBooks = await response.json();\n"
    "    try {\n"
    "      var rResp = await fetch(API + '/reactions');\n"
    "      allReactions = await rResp.json();\n"
    "    } catch(e) { allReactions = {}; }"
)
js = js.replace(old, new, 1)

# Add react function before openBook
old = "function openBook(id) {"
new = (
    "function react(bookId, type) {\n"
    "  var key = bookId + '_' + type;\n"
    "  var opposite = type === 'up' ? 'down' : 'up';\n"
    "  var oppKey = bookId + '_' + opposite;\n"
    "  if (myVotes[key]) return;\n"
    "  if (!allReactions[bookId]) allReactions[bookId] = {up:0, down:0};\n"
    "  if (myVotes[oppKey]) {\n"
    "    allReactions[bookId][opposite] = Math.max(0, (allReactions[bookId][opposite] || 0) - 1);\n"
    "    delete myVotes[oppKey];\n"
    "  }\n"
    "  allReactions[bookId][type] = (allReactions[bookId][type] || 0) + 1;\n"
    "  myVotes[key] = 1;\n"
    "  localStorage.setItem('myVotes', JSON.stringify(myVotes));\n"
    "  fetch(API + '/react/' + bookId + '/' + type, {method:'POST'}).catch(function(){});\n"
    "  renderReactionBtns(bookId);\n"
    "}\n\n"
    "function renderReactionBtns(bookId) {\n"
    "  var r = allReactions[bookId] || {up:0, down:0};\n"
    "  var upCount = r.up || 0;\n"
    "  var downCount = r.down || 0;\n"
    "  var myUp = myVotes[bookId + '_up'] ? ' voted' : '';\n"
    "  var myDown = myVotes[bookId + '_down'] ? ' voted' : '';\n"
    "  var upEl = document.getElementById('react-up');\n"
    "  var downEl = document.getElementById('react-down');\n"
    "  if (upEl) upEl.innerHTML = '<span class=\"react-icon\">👍</span>' + (upCount > 0 ? '<span class=\"react-count\">' + upCount + '</span>' : '');\n"
    "  if (upEl) upEl.className = 'react-btn react-up' + myUp;\n"
    "  if (downEl) downEl.innerHTML = '<span class=\"react-icon\">👎</span>' + (downCount > 0 ? '<span class=\"react-count\">' + downCount + '</span>' : '');\n"
    "  if (downEl) downEl.className = 'react-btn react-down' + myDown;\n"
    "}\n\n"
    "function openBook(id) {"
)
js = js.replace(old, new, 1)

# Add renderReactionBtns call after openBook sets up the page
# Find where mark-read button is rendered and add reaction buttons
old = "document.getElementById('mark-read-btn').onclick = function() {"
new = (
    "renderReactionBtns(b.id);\n"
    "  document.getElementById('mark-read-btn').onclick = function() {"
)
js = js.replace(old, new, 1)

with open('/root/books/webapp/app.js', 'w') as f:
    f.write(js)

print('app.js patched OK')

# 3. Patch index.html — add reaction buttons around mark-read
with open('/root/books/webapp/index.html', 'r') as f:
    h = f.read()

old = '<button id="mark-read-btn" class="mark-read-btn">'
new = (
    '<div class="react-row">\n'
    '        <button id="react-up" class="react-btn react-up" onclick="react(currentBookId,\'up\')"></button>\n'
    '        <button id="mark-read-btn" class="mark-read-btn">'
)
h = h.replace(old, new, 1)

# Close the react-row div after mark-read-btn closing tag
old = '</button>\n      </div>\n    </div>\n\n    <div id="screen-sub"'
new = (
    '</button>\n'
    '        <button id="react-down" class="react-btn react-down" onclick="react(currentBookId,\'down\')"></button>\n'
    '      </div>\n'
    '      </div>\n'
    '    </div>\n\n    <div id="screen-sub"'
)
h = h.replace(old, new, 1)

with open('/root/books/webapp/index.html', 'w') as f:
    f.write(h)

print('index.html patched OK')

# 4. Add CSS for reaction buttons
with open('/root/books/webapp/style.css', 'r') as f:
    css = f.read()

react_css = """
.react-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px 20px;
  background: #1a1a1a;
}
.react-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: transform 0.15s, opacity 0.15s;
  background: #2a2a2a;
  color: #fff;
  flex-shrink: 0;
}
.react-btn:active { transform: scale(0.92); }
.react-up { color: #4caf50; }
.react-up.voted { background: #1b3a1d; }
.react-down { color: #e53935; }
.react-down.voted { background: #3a1b1b; }
.react-icon { font-size: 20px; line-height: 1; }
.react-count { font-size: 14px; font-weight: 700; }
.react-row .mark-read-btn { flex: 1; margin: 0; }
"""

if '.react-row' not in css:
    css += react_css
    with open('/root/books/webapp/style.css', 'w') as f:
        f.write(css)
    print('style.css patched OK')
else:
    print('style.css already has react styles')
