# context.md — AI Events Calendar (universal handoff)

_Last updated: 2026-06-28_

## What it is
A reputation-scored, filterable AI-events calendar (single self-contained `index.html`) covering applied AI for a rolling ~12 months. Born from a research-agent swarm; productized into a public open-source repo + Vercel deployment.

## Current state — DONE
- ✅ 121 curated events (Jul 2026 → Jun 2027), each with a 0–100 reputation score, category, region, cost, relevance, source URL, and note.
- ✅ Interactive dashboard: filters (search/category/region/relevance/min-reputation), Going/Maybe/Skip marks persisted in `localStorage`, My-plan view, `.ics` export.
- ✅ Single-source generator `build_ai_calendar.py` (stdlib only) → emits `index.html` + `ai-events-data.json`.
- ✅ Git repo initialized; pushed to GitHub `blizzardbase/ai-events-calendar` (public, MIT).
- ✅ Deployed to Vercel.

## Deploy / infra
- **Host:** Vercel project `ai-events-calendar` (scope `minitech782-5101` / `hvs-projects-470139d8`). Static — `index.html` at root.
- **Domain:** `calendar.blizzardcollective.xyz`. DNS zone is on **Cloudflare** (proxied apex). Subdomain needs: `CNAME calendar → cname.vercel-dns.com`, **proxy OFF (grey cloud)**.
- The local wrangler/Cloudflare token only has `workers:write` — it CANNOT edit DNS. The CNAME was added manually in the Cloudflare dashboard (or via a DNS-scoped API token if one is later provided).
- Redeploy with `vercel --prod` from repo root.

## Data provenance
- Built by ~11 parallel research agents (by category/region) + 1 senior reviewer that dropped phantom/out-of-scope events (e.g. a bogus August LEAP, infra-only confs) and corrected scores/dates. Snapshot as of late June 2026; some 2027 dates are projected (`conf=False` → `est` badge).

## How to update the data
Edit the `E` list in `build_ai_calendar.py` → `python3 build_ai_calendar.py` → commit. Never hand-edit `index.html`.

## Open ideas / backlog
- Per-event prep checklists + personal notes (persist alongside status).
- "Trips" — auto-cluster nearby-in-time-and-place events into a travel block (e.g. GITEX week in Dubai, SF October run).
- ROI/price sorting; shareable filtered URLs; calendar-grid view.
- Public event-submission flow that opens a PR.
- Scheduled refresh of `est` dates as organizers publish 2027 dates.

## Owner notes
- Owner: Harish (non-developer). Keep explanations simple; show preview steps.
- Repo is public so others can fork/clone. Keep scope to *applied* AI; no secrets in the repo.
