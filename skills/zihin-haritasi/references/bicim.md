# Data format

One JSON object. Keys are Turkish; write them exactly as below. Text values are in the user's language.

```json
{
  "baslik": "Page title",
  "tarih": "31 October 2026",
  "alt": "One-line subtitle (empty = a usage hint is shown)",
  "duzen": "harita",
  "acikDerinlik": 2,
  "kok": {
    "id": "kok",
    "ad": "Central idea",
    "not": "The one-sentence answer.",
    "alt": [
      {
        "id": "a", "ad": "Main branch", "renk": 1,
        "not": ["bullet one", "bullet two"],
        "alt": [
          { "id": "a1", "ad": "Child", "isaret": ["kanit"], "not": "Detail shown on click." },
          { "ad": "Child with a link", "baglanti": "https://example.com" }
        ]
      },
      { "id": "b", "ad": "Second branch", "kapali": true, "alt": [ { "ad": "Starts collapsed" } ] }
    ]
  },
  "iliskiler": [ { "kaynak": "a1", "hedef": "b", "etiket": "why they are linked" } ],
  "cerceveler": [ { "ust": "a", "aralik": [0, 1], "etiket": "group name" } ],
  "ozetler":    [ { "ust": "a", "aralik": [0, 1], "ad": "conclusion", "not": "..." } ]
}
```

| Key | Meaning |
| --- | --- |
| `baslik`, `tarih`, `alt` | title, date, subtitle at the top of the page |
| `duzen` | layout: `harita` (default), `mantik`, `agac`, `zaman`, `kilcik`, `matris` |
| `acikDerinlik` | levels open on load; deeper levels start collapsed (2 is a good default) |
| `kolonlar` | only for `matris`: column names, e.g. `["Price", "Speed"]` |
| `kok` | the root node |
| `ad` | node name (required on every node, keep it short) |
| `not` | detail shown on click: a string or a list of strings |
| `alt` | list of child nodes (any depth) |
| `id` | needed only on nodes used by `iliskiler`, `cerceveler`, `ozetler`; must be unique |
| `renk` | main branches only: 1-8 (palette) or a hex colour; children inherit |
| `kapali` | `true` = this node starts collapsed |
| `baglanti` | a URL shown in the detail card |
| `isaret` | markers: `karar` (decision for the user), `kanit` (evidence), `fikir` (idea), `uyari` (warning), `soru` (question), `tamam` (done), `oncelik-1`…`oncelik-9` (priority), `ilerleme-40` (progress %), `yolda` (in progress: faded, dashed). Any other text shows as a grey tag |
| `iliskiler` | arrows between any two nodes: `kaynak` (from id), `hedef` (to id), `etiket` (label) |
| `cerceveler` | a box around some children of `ust`; `aralik` = [first, last] child index, 0-based, both included; omit for all |
| `ozetler` | a brace joining some children of `ust` into one conclusion (`ad`, optional `not`) |

The page itself lets the viewer switch layout and theme, collapse branches, focus on one branch, present branch by branch, and read it as a list (automatic on phones). Themes, set with `"tema"` or `?tema=` in the URL: `beyaz` (default, clean white), `pastel`, `kagit` (warm paper), `koyu` (dark), and three terminal styles `gece`, `fosfor`, `amber`. The page also has a theme picker; the viewer's last choice is remembered on their device and wins over `"tema"` (the URL wins over both).

`scripts/kur.py` stops on unknown ids, bad ranges and unknown layouts and prints what is wrong.
