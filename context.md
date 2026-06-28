# context.md — AI Events Calendar (universal handoff)

_Last updated: 2026-06-28_

## What it is
A reputation-scored, filterable AI-events calendar (single self-contained `index.html`) covering applied AI for a rolling ~12 months. Born from a research-agent swarm; productized into a public open-source repo + Vercel deployment.

## Current state — DONE
- ✅ 121 curated events (Jul 2026 → Jun 2027), each with a 0–100 reputation score, category, region, cost, relevance, source URL, and note.
- ✅ Interactive dashboard: filters (search/category/region/relevance/min-reputation), Going/Maybe/Skip marks persisted in `localStorage`, My-plan view, `.ics` export.
- ✅ Single-source generator `build_ai_calendar.py` (stdlib only) → emits `index.html` + `ai-events-data.json`.
- ✅ Git repo initialized; pushed to GitHub `blizzardbase/ai-events-calendar` (public, MIT).
- ✅ Deployed to Vercel (production): https://ai-events-calendar-ruddy.vercel.app
- ✅ Custom domain `calendar.blizzardcollective.xyz` live: `A calendar → 76.76.21.21` (DNS-only) created on Cloudflare; Vercel auto-issues SSL.

## Deploy / infra
- **Host:** Vercel project `ai-events-calendar` (scope `minitech782-5101` / `hvs-projects-470139d8`). Static — `index.html` at root.
- **Domain:** `calendar.blizzardcollective.xyz` — live. Record on Cloudflare (zone `blizzardcollective.xyz`, id `6cd0a0f64ee19f73f43e1a77927b27c3`): `A calendar → 76.76.21.21`, proxy OFF (DNS-only).
- **DNS automation (DONE — permanent):** a Cloudflare API token (Zone:DNS:Edit + Zone:Read, all 11 zones) is set as **`CLOUDFLARE_DNS_API_TOKEN`** in **`~/.zshenv`** — verified active and edit-capable. Any agent/tool shell can manage DNS for every domain hands-off. NOTE: it's deliberately NOT named `CLOUDFLARE_API_TOKEN`, because that name would shadow wrangler's own OAuth login and break Workers/KV/Pages deploys. Keep DNS on `CLOUDFLARE_DNS_API_TOKEN`; let wrangler use its OAuth (`~/.config/.wrangler`, scopes: workers/workers_kv/workers_routes write).
- **Gotcha for future sessions:** tool shells run as **non-interactive `zsh -c`**, which source ONLY `~/.zshenv` (NOT `~/.zshrc`/`~/.zprofile`). Env vars meant for agents MUST live in `~/.zshenv`. (wrangler's OAuth token is `workers:write` only — no DNS. Per-zone fallback tokens also exist in `~/.cloudflared/cert.<zone>.pem.*` from `cloudflared tunnel login`.)
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
