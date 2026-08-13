# tools/

## The English page is generated, not hand-edited

`en/index.html` is built from `index.html`. **Never edit `en/index.html` by hand** —
the next build overwrites it.

The workflow is always:

1. Edit `index.html` (the Spanish page is the source of truth for structure, CSS and JS).
2. If you added or changed any Spanish text, add the English string to `tools/i18n.py`.
3. Run the build:

   ```sh
   python tools/build_en.py
   ```

4. Commit both `index.html` and `en/index.html`.

## The build fails loudly

`build_en.py` prints anything it could not translate:

```
UNTRANSLATED text nodes : 0
UNTRANSLATED attributes : 0
UNMAPPED whatsapp msgs  : 0
```

Any non-zero count lists the exact strings. Add them to the right map in
`tools/i18n.py` and re-run — do not ship a page with a non-zero count, because
those strings stay in Spanish on the English page.

## What lives where in `i18n.py`

| map | covers |
|-----|--------|
| `T`  | visible text nodes, keyed by the exact Spanish string including punctuation and surrounding quote marks |
| `A`  | `alt`, `aria-label`, `title`, `placeholder` attribute values |
| `J`  | strings embedded in the inline JavaScript (social-proof ticker, breed names) |

Keys must match the source **exactly**. If a string does not translate, copy it
from the builder's report rather than retyping it — accents and the `¿ ¡` marks
are easy to get subtly wrong.

## What the build handles on its own

You do not need to maintain these by hand; they are derived each run:

- `<html lang>`, title, meta description/keywords, Open Graph and Twitter tags
- canonical + reciprocal `hreflang` (es-CO / es / en / x-default)
- the whole JSON-LD block, including an English `FAQPage` regenerated **from the
  translated markup**, so schema and page can never drift apart
- WhatsApp deep links, including the ones assembled in JS at runtime
- rewriting asset paths to `../` and the service-worker registration
- swapping the ES→EN nav switcher for the EN→ES one

## Checks worth running after a build

```sh
# structured data parses and FAQ matches the visible page
python - <<'EOF'
import re, json
for f in ('index.html', 'en/index.html'):
    h = open(f, encoding='utf-8').read()
    b = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)[0]
    d = json.loads(b); body = h.replace(b, '')
    faq = [x for x in d if x.get('@type') == 'FAQPage'][0]
    bad = sum(1 for q in faq['mainEntity']
              if q['name'] not in body or q['acceptedAnswer']['text'] not in body)
    print(f, '| entities:', len(d), '| FAQ:', len(faq['mainEntity']), '| mismatches:', bad)
EOF
```

Bump `CACHE_NAME` in `sw.js` whenever you ship a change, or returning visitors
keep the old page until the service worker happens to revalidate.

## Moving to a custom domain

`en/index.html`, the manifests, the service worker, the sitemap and robots.txt all
carry absolute URLs and `/house-barf/` paths. Attaching a custom domain moves the
site to the root of that domain, so both have to change together. One command does
all of it:

```sh
python tools/set_domain.py www.yourdomain.com --dry   # preview
python tools/set_domain.py www.yourdomain.com         # apply + rebuild /en/
```

It rewrites every absolute URL, converts `/house-barf/…` paths to `/…`, writes the
`CNAME` file GitHub needs, updates `BASE` in `build_en.py`, rebuilds the English
page and reports any old references it could not resolve (should be 0).

Afterwards: commit, push, then set the custom domain in **Settings → Pages** and
tick **Enforce HTTPS** once the certificate is issued.

## After editing any FAQ or the ordering steps

Google requires FAQ and HowTo text in the structured data to appear on the page.
Editing an answer without regenerating the JSON-LD breaks that silently — nothing
in the browser complains.

```sh
python tools/sync_schema.py          # regenerate from the visible markup
python tools/sync_schema.py --check  # exit 1 if out of sync, changes nothing
python tools/build_en.py             # then rebuild /en/
```

`build_en.py` already regenerates both from the *translated* markup, so the English
page cannot drift. Only the Spanish page needs this step.
