# -*- coding: utf-8 -*-
"""Regenerate the Spanish page's FAQPage and HowTo schema from its visible markup.

Google requires the question, answer and step text in structured data to appear on
the page. Editing a FAQ answer without regenerating the JSON-LD silently breaks that,
and nothing in the browser complains. Run this after touching any FAQ or the ordering
steps, then run build_en.py.

    python tools/sync_schema.py            # rewrite and report
    python tools/sync_schema.py --check    # exit 1 if out of sync, change nothing
"""
import re, json, os, sys, html as H

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'index.html')
BASE = 'https://www.housebarf.com/'
sys.stdout.reconfigure(encoding='utf-8')

check_only = '--check' in sys.argv
s = open(SRC, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in s else '\n'

m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
data = json.loads(m.group(2))

def clean(t):
    return H.unescape(re.sub(r'<[^>]+>', '', t)).strip()

# --- FAQ ---
pairs = re.findall(r'<button class="faq-q">(.*?)<svg.*?<div class="faq-a"><p>(.*?)</p></div>', s, re.S)
qa = [{"@type": "Question", "name": clean(q),
       "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in pairs]

# --- HowTo ---
steps_raw = re.findall(r'<div class="step-n">(\d)</div>\s*<h3>([^<]+)</h3>\s*<p>([^<]+)</p>', s, re.S)
steps = [{"@type": "HowToStep", "position": int(n), "name": name.strip(),
          "text": text.strip(), "url": BASE + "#como-pedir"} for n, name, text in steps_raw]

drift = []
for e in data:
    if e.get('@type') == 'FAQPage':
        if e.get('mainEntity') != qa:
            drift.append(f'FAQPage ({len(e.get("mainEntity", []))} in schema vs {len(qa)} on page)')
        e['mainEntity'] = qa
    if e.get('@type') == 'HowTo':
        if e.get('step') != steps:
            drift.append(f'HowTo ({len(e.get("step", []))} in schema vs {len(steps)} on page)')
        e['step'] = steps

if check_only:
    if drift:
        print('OUT OF SYNC:', '; '.join(drift))
        print('run: python tools/sync_schema.py')
        sys.exit(1)
    print(f'in sync - FAQ {len(qa)} Q&A, HowTo {len(steps)} steps')
    sys.exit(0)

out = s[:m.start(2)] + NL + '    ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + NL + '    ' + s[m.end(2):]
open(SRC, 'w', encoding='utf-8', newline='').write(out)
print('rewrote:', '; '.join(drift) if drift else 'nothing was out of sync')
print(f'FAQ {len(qa)} Q&A, HowTo {len(steps)} steps')

# prove parity against the file we just wrote
h = open(SRC, encoding='utf-8').read()
b = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)[0]
d = json.loads(b); body = h.replace(b, '')
bad = 0
for e in d:
    if e.get('@type') == 'FAQPage':
        bad += sum(1 for q in e['mainEntity']
                   if q['name'] not in body or q['acceptedAnswer']['text'] not in body)
    if e.get('@type') == 'HowTo':
        bad += sum(1 for st in e['step'] if st['name'] not in body or st['text'] not in body)
print('parity mismatches:', bad)
sys.exit(1 if bad else 0)
