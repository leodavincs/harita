# Harita

[Türkçe](README.md) | **English**

> Stop asking AI for reports. Ask it for a map.

AI answers in walls of text; your brain thinks in branches. **Harita** ("map" in Turkish) is an agent skill that turns any content into a clickable mind map. You see the whole picture at a glance and open details only when you want them.

Just say "map this", "draw this as a mind map" or "map what we talked about last week".

- Produces one self-contained HTML file; no internet or install needed.
- Six layouts: mind map, logic chart, tree, timeline, fishbone, matrix.
- Collapse branches, focus on one branch, present branch by branch, list view on phones.
- Works in the Claude app, Codex and Claude Code.
- The page interface is in Turkish for now; map content follows your language.

## Install

### Claude app (claude.ai, desktop)

The app doesn't install from GitHub; skills are uploaded as a zip.

1. Download [`dist/zihin-haritasi.zip`](dist/zihin-haritasi.zip) (keep it zipped).
2. In Settings → Capabilities, turn on **Code execution and file creation**.
3. Customize → Skills → **+** → **Upload a skill** → pick the zip.
4. In a new chat: "Draw this as a mind map."

### Claude Code

Inside Claude Code:

```
/plugin marketplace add leodavincs/harita
/plugin install harita@harita
```

### Codex (app, CLI, IDE)

Tell Codex:

```
$skill-installer https://github.com/leodavincs/harita/tree/main/skills/zihin-haritasi
```

Manual: copy `skills/zihin-haritasi` into `~/.agents/skills/`.

## How it works

The agent writes the content as a tree (JSON), `scripts/kur.py` validates it and builds a single HTML page, and changes rebuild the same file. Format: [`references/bicim.md`](skills/zihin-haritasi/references/bicim.md). Full example: [`examples/ornek.json`](examples/ornek.json).

```sh
python3 skills/zihin-haritasi/scripts/kur.py examples/ornek.json --ac
```

## License

MIT.
