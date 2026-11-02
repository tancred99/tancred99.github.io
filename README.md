# Russian grammar drills

Mobile-friendly static site for Russian grammar and vocabulary practice, with a Lessons tab. Lesson 1 is ready; the rest of the course is on the roadmap. It is published at the root of <https://tancred99.github.io>.

`index.html` is the app. Served over HTTP, it loads `lessons.json`, `exercises.json`, and `vocab.json` from the same directory. Opened as a local file, it uses the copy of that data built into the page.

## Rebuild `index.html`

After editing the JSON, rebuild the page from the repo root:

```bash
python3 build.py
```

Grammar items live in `exercises.json`. `build.py` regenerates `vocab.json` from `src/vocab_source.txt` and `lessons.json` from `src/lessons_src.py`, then inlines `exercises.json`, `vocab.json`, `lessons.json`, `src/engine.js`, and `src/app.js` into `template.html` and writes `index.html`. Put lasting starter-vocabulary edits in `src/vocab_source.txt` and lasting lesson edits in `src/lessons_src.py` so the rebuild keeps them.
