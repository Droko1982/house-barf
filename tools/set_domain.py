# -*- coding: utf-8 -*-
"""Point the whole site at a custom domain.

    python tools/set_domain.py www.example.com          # apply
    python tools/set_domain.py www.example.com --dry    # show what would change

On a GitHub Pages *project* site the content lives under /house-barf/. Attaching a
custom domain moves it to the root of that domain, so two things change together:

    https://droko1982.github.io/house-barf/   ->  https://www.example.com/
    /house-barf/en/                           ->  /en/

Both are handled here, along with the CNAME file GitHub needs in the repo root.
Run tools/build_en.py afterwards (this script does it for you).
"""
import os, re, sys, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_ORIGIN = 'https://droko1982.github.io/house-barf/'
OLD_PATH = '/house-barf/'

FILES = ['index.html', 'en/index.html', '404.html', 'privacidad.html',
         'manifest.json', 'en/manifest.json', 'sw.js', 'robots.txt', 'sitemap.xml']

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    if len(args) != 1:
        sys.exit('usage: python tools/set_domain.py <domain> [--dry]\n'
                 '   e.g. python tools/set_domain.py www.housebarf.co')

    domain = args[0].strip().lower().rstrip('/')
    domain = re.sub(r'^https?://', '', domain)
    if not re.fullmatch(r'[a-z0-9.-]+\.[a-z]{2,}', domain):
        sys.exit(f'"{domain}" does not look like a domain name')

    new_origin = f'https://{domain}/'
    print(f'{OLD_ORIGIN}  ->  {new_origin}')
    print(f'{OLD_PATH}{" ":<26}->  /')
    print()

    total = 0
    for rel in FILES:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print(f'  {rel:<20} (missing, skipped)')
            continue
        src = open(path, encoding='utf-8', newline='').read()
        out = src.replace(OLD_ORIGIN, new_origin)
        # absolute paths only - never touch "house-barf" inside a cache name or a word
        out = out.replace('"' + OLD_PATH, '"/').replace("'" + OLD_PATH, "'/")
        out = out.replace('(' + OLD_PATH, '(/')
        n = sum(1 for a, b in zip(src, out) if a != b) if len(src) == len(out) else abs(len(src) - len(out))
        changed = src != out
        total += 1 if changed else 0
        print(f'  {rel:<20} {"updated" if changed else "no change"}')
        if changed and not dry:
            open(path, 'w', encoding='utf-8', newline='').write(out)

    # GitHub needs this file in the repo root to serve the custom domain
    cname = os.path.join(REPO, 'CNAME')
    print(f'  {"CNAME":<20} -> {domain}')
    if not dry:
        open(cname, 'w', encoding='utf-8', newline='').write(domain + '\n')

    # the builder carries the base URL too
    b = os.path.join(REPO, 'tools', 'build_en.py')
    src = open(b, encoding='utf-8').read()
    if OLD_ORIGIN in src:
        print(f'  {"tools/build_en.py":<20} updated (BASE)')
        if not dry:
            open(b, 'w', encoding='utf-8').write(src.replace(OLD_ORIGIN, new_origin))

    if dry:
        print('\nDry run - nothing written.')
        return

    print('\nRebuilding the English page...')
    subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'build_en.py')], check=True)

    leftover = 0
    for rel in FILES:
        p = os.path.join(REPO, rel)
        if os.path.exists(p):
            t = open(p, encoding='utf-8').read()
            leftover += t.count('droko1982.github.io') + t.count(OLD_PATH)
    print(f'\nold references remaining: {leftover}' + ('  <- investigate' if leftover else '  (clean)'))
    print(f'\nNext: commit, push, then set the custom domain to {domain}')
    print('in the repository Settings -> Pages, and tick "Enforce HTTPS" once the')
    print('certificate has been issued (it can take up to an hour).')

if __name__ == '__main__':
    main()
