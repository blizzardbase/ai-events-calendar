# CLAUDE.md — AI Events Calendar

Context for Claude Code working in this repo.

## What this is
A self-contained, reputation-scored AI-events calendar dashboard. Single source of truth is `build_ai_calendar.py`, which holds the curated event data **and** generates `index.html` (the dashboard) + `ai-events-data.json`.

## Golden rule
**Never hand-edit `index.html` or `ai-events-data.json`** — they are generated. Edit the data/template in `build_ai_calendar.py`, then run:

```bash
python3 build_ai_calendar.py
```

Both outputs regenerate. No dependencies (Python stdlib only).

## Data model
The `E` list in `build_ai_calendar.py` is one row per event, in this order (see `KEYS`):
`id, name, ds(start YYYY-MM-DD), de(end), dd(display), city, country, region, cat, fop, cost, url, org, att, rep, rel, conf, note`

- `region` ∈ {North America, Europe, Middle East, Asia, Africa, Other}
- `cat` ∈ {AI Engineering, Agents & MCP, AI Products & Consumer, Enterprise & B2B AI, Vendor Dev Day, Flagship Tech, AI Marketing & Creative, Hackathon}
- `fop` ∈ {Free, Paid, Mixed}
- `rel` ∈ {Must, Worth, Optional}
- `rep` = integer 0–100 (see scoring rubric below)
- `conf` = bool; `False` renders an `est` flag for projected/unconfirmed dates

Post-build adjustments (drops / field overrides / additions from review passes) live in the block right after `EVENTS = [...]`. Prefer fixing data at the source row; use the override block only for review-driven corrections.

## Scope (IMPORTANT — keep it tight)
INCLUDE applied AI: engineering, agents/MCP, dev tools, AI products, consumer AI, enterprise/B2B AI, vendor dev days, flagship tech w/ heavy AI, AI marketing/creative, hackathons.

EXCLUDE: pure ML/DL research & academic conferences (NeurIPS, ICML, ICLR, CVPR, ACL, COLM, KDD), model-training/distillation events, and big-data/data-engineering infra shows. The audience is people **shipping AI products**, not training models.

## Reputation rubric (0–100)
Score from: prior editions (did it run before?) + verified attendance + real social/press footprint (recaps, talk videos, attendee posts — not organizer marketing).
90–100 global flagship · 75–89 established/reputable · 60–74 solid/growing · 40–59 newer/niche · <40 thin/caution. Default floor for inclusion ≈ 60; keep credible recurring builder communities (AGI House, AI Tinkerers, Cerebral Valley) even if smaller.

## Dashboard behavior (in the generated JS)
- Marks (Going/Maybe/Skip) persist in `localStorage` key `aical_status_v1`. No backend.
- Filters: search, category, region, relevance chips, min-reputation slider; views All/My plan/Maybe/Unmarked.
- `.ics` export builds all-day VEVENTs from `Going` events. Commas/semicolons are stripped (not backslash-escaped) to avoid JS string-escaping bugs — keep it that way.

## Deploy
- Hosted on **Vercel** (static; `index.html` at root). Production domain: `calendar.blizzardcollective.xyz` (CNAME → `cname.vercel-dns.com`, DNS on Cloudflare, proxy OFF).
- Redeploy: `vercel --prod` from repo root (or push to `main` if Git integration is connected).

## Git workflow
- Source of truth is GitHub: `blizzardbase/ai-events-calendar` (public).
- Code changes go on a feature branch (`claude/<desc>`) → PR → CodeRabbit review → merge. Docs-only (`*.md`) may go straight to `main`.
- Never commit secrets. There are none in this project — keep it that way (no `.env`, no tokens).

## Good first features to build next
Per-event prep checklists, "trips" grouping (cluster nearby events into one travel block), price/ROI sorting, a public submissions form → PR, auto-refresh of `est` dates, calendar-grid view, shareable filtered URLs.
