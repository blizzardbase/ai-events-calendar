# AI Events Calendar

An opinionated, **reputation-scored** calendar of the AI events worth your time — a rolling 12-month view (currently **Jul 2026 → Jun 2027**) covering applied AI: engineering, agents, products, consumer & B2B/B2C, dev tools, flagship tech, marketing/creative, and hackathons — across North America, Europe, the Middle East and Asia.

It's a single self-contained HTML page. No server, no build step to view it, no tracking. Open it, filter, and click **Going / Maybe / Skip** on events — your picks are saved in your browser and exportable to your real calendar as an `.ics` file.

**Live:** https://calendar.blizzardcollective.xyz

![events](https://img.shields.io/badge/events-121-blue) ![window](https://img.shields.io/badge/window-Jul%202026%E2%80%93Jun%202027-green) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Why this exists

Most "AI event" lists are SEO spam padded with phantom conferences and pay-to-speak summits. This one is curated and **scored for credibility**, so you can tell a flagship from a cash-grab at a glance, and filter out everything that isn't relevant to you.

It deliberately **excludes** pure ML/DL research & academic conferences (NeurIPS, ICML, ICLR, CVPR, COLM…), model-training/distillation events, and big-data infrastructure shows. The focus is on people **building and shipping AI products**.

## The reputation score (0–100)

Every event gets a single reputation number derived from three signals:

1. **Track record** — did it actually run before? How many editions?
2. **Attendance** — verified headcount from the most recent edition.
3. **Real footprint** — genuine social/press proof (recap posts, talk recordings, attendee write-ups on X / LinkedIn / YouTube / Reddit), not just the organizer's own marketing.

| Score | Meaning |
|------:|---------|
| 90–100 | Global flagship — multi-year, many thousands attend, heavy press |
| 75–89  | Established & reputable, well-attended |
| 60–74  | Solid / growing, real track record |
| 40–59  | Newer or niche; legitimate but unproven |
| < 40   | Thin footprint — caution / likely phantom |

Each event also carries a **relevance** verdict for an AI engineer/founder — **Must / Worth / Optional** — and a **category** and **region** for filtering. Dates marked `est` are projected (official 2027 dates not yet published — verify before booking).

## Using the dashboard

- **Filter** by search term, category, region, relevance, or a minimum-reputation slider.
- **Mark** events **Going / Maybe / Skip**. Marks persist in `localStorage` (this browser only — no account, no backend).
- **Views:** All · My plan · Maybe · Unmarked.
- **Export my plan (.ics)** downloads your *Going* events as a calendar file you can import into Google / Apple / Outlook calendars.

## Run / fork / customize

The page is generated from one Python script — no dependencies beyond the standard library.

```bash
git clone https://github.com/blizzardbase/ai-events-calendar.git
cd ai-events-calendar
python3 build_ai_calendar.py     # regenerates index.html + ai-events-data.json
open index.html                  # or just double-click it
```

**To add or edit an event:** open `build_ai_calendar.py` and edit the `E` list (one row per event). Fields, in order:

```
id, name, date_start, date_end, date_display, city, country, region,
category, free_or_paid, cost, url, organizer, last_attendance,
reputation(0-100), relevance(Must/Worth/Optional), date_confirmed(bool), note
```

Re-run the script and the dashboard rebuilds. The curated dataset is also emitted as `ai-events-data.json` if you want to consume it elsewhere.

## How the dataset was built

The initial 121 events were compiled by a swarm of research agents (one per category/region), each verifying dates, cost, prior editions, attendance and social proof, then audited by a senior reviewer that removed phantom/out-of-scope events and corrected scores. It's a snapshot — PRs with corrections and additions are welcome.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The dashboard (generated; self-contained) |
| `ai-events-data.json` | The curated dataset (generated) |
| `build_ai_calendar.py` | Source of truth — data + generator |

## Contributing

Found a wrong date, a missing flagship, or a phantom that slipped through? Open a PR editing the `E` list in `build_ai_calendar.py` (don't hand-edit `index.html` — it's generated). Keep the scope to applied AI and include a source for any reputation/attendance claim.

## License

MIT — see [LICENSE](LICENSE). Fork it, host your own, change the scope to your niche.
