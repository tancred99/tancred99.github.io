# Russian grammar drills

Mobile-friendly static site for Russian grammar and vocabulary practice. It is published at the root of <https://tancred99.github.io>.

`index.html` is the app. Served over HTTP, it loads `exercises.json` and `vocab.json` from the same directory. Opened as a local file, it uses the copy of that data built into the page.

## Rebuild `index.html`

After editing the JSON, rebuild the page from the repo root:

```bash
python3 build.py
```

Grammar items live in `exercises.json`. `build.py` first regenerates `vocab.json` from `src/vocab_source.txt`, then inlines `exercises.json`, `vocab.json`, `src/engine.js`, and `src/app.js` into `template.html` and writes `index.html`. Put lasting starter-vocabulary edits in `src/vocab_source.txt` so the rebuild keeps them.
