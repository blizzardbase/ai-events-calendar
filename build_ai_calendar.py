#!/usr/bin/env python3
"""
Builds an interactive AI-events calendar dashboard.
Outputs:
  - ai-events-data.json   (the curated dataset)
  - ai-calendar.html      (self-contained clickable dashboard; localStorage persistence + .ics export)
Run:  python3 build_ai_calendar.py
Window: Jul 2026 - Jun 2027. Scope: APPLIED AI (engineering, agents, products, consumer, B2B/B2C, dev tools,
flagship tech w/ heavy AI, marketing/creative, hackathons). Excludes pure ML-research/training/big-data.
Reputation 0-100 from: prior editions + attendance + real social/press footprint (researched by an agent swarm).
"""
import json, os, html

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# fields: id, name, ds(start ISO), de(end ISO), dd(display), city, country, region,
#   cat(category), fop(Free/Paid/Mixed), cost, url, org, att(last attendance), rep(0-100),
#   rel(Must/Worth/Optional), conf(date confirmed), note
E = [
 # ---------- JULY 2026 ----------
 ["aiewf26","AI Engineer World's Fair 2026","2026-06-29","2026-07-02","Jun 29 – Jul 2, 2026","San Francisco","USA","North America","AI Engineering","Paid","~$800–1,600","https://www.ai.engineer/worldsfair/2026","AI.Engineer","~6,000 (2026)",92,"Must",True,"The anchor event for the AI engineering community. 300+ speakers, 12 tracks."],
 ["elevenlabs-paris26","ElevenLabs Summit Paris 2026","2026-07-08","2026-07-09","Jul 8–9, 2026","Paris","France","Europe","AI Marketing & Creative","Paid","Enterprise (not public)","https://summit.elevenlabs.io/paris","ElevenLabs","~2,000",65,"Worth",True,"Voice-AI city-tour summit; relevant for consumer/agent/creative audio."],
 ["raise26","RAISE Summit 2026","2026-07-08","2026-07-09","Jul 8–9, 2026","Paris","France","Europe","Enterprise & B2B AI","Paid","€800–2,500+","https://www.raisesummit.com/","RAISE","~9,000 (2026)",72,"Worth",True,"Largest applied-AI summit in Europe by attendance; C-suite/BD heavy."],
 ["waic26","World AI Conference (WAIC) 2026","2026-07-17","2026-07-20","Jul 17–20, 2026","Shanghai","China","Asia","AI Products & Consumer","Mixed","Free expo / ¥500–5,000","https://www.worldaic.com.cn/en/","Shanghai Gov / MIIT","400,000+ (2025)",82,"Worth",True,"China's dominant annual AI event. Visa required."],
 ["genai-sf26","GenAI Summit San Francisco 2026","2026-07-18","2026-07-19","Jul 18–19, 2026","San Francisco","USA","North America","AI Products & Consumer","Paid","~$500–1,000","https://agisummit.ai/","Bay AI Circle","15,000 claimed",66,"Optional",True,"Broad applied GenAI; verify the 15k claim (may be cumulative)."],
 ["hacknation26","Hack-Nation Global AI Hackathon","2026-07-18","2026-07-19","Jul 18–19, 2026","13 global hubs + Online","Global","North America","Hackathon","Free","Free","https://hack-nation.ai/","Hack-Nation (MIT-backed)","1,000+",70,"Worth",True,"24-hr sprint across 13 hubs (SF/MIT/NYC/London/Paris/Delhi…). Sponsors: OpenAI, Vercel, Databricks."],
 ["supabase-lw","Supabase Launch Week (recurring)","2026-07-14","2026-07-18","~Quarterly (next Jul 2026)","Online","Global","North America","Vendor Dev Day","Free","Free","https://supabase.com/launch-week","Supabase","50,000+ viewers",65,"Worth",False,"Virtual product-drop week; track pgvector/Edge Functions for AI apps."],
 ["ethglobal-lisbon","ETHGlobal Lisbon 2026","2026-07-24","2026-07-26","Jul 24–26, 2026","Lisbon","Portugal","Europe","Hackathon","Free","Free to hack","https://ethglobal.com/","ETHGlobal","1,000–2,000",85,"Worth",True,"AI x Crypto track; strong if building onchain agents."],
 ["agihouse","AGI House Hackathons (recurring)","2026-07-05","2026-07-06","Near-weekly (SF)","San Francisco","USA","North America","Hackathon","Free","Free (apply)","https://luma.com/agihouse","AGI House","50–150 / event",90,"Must",False,"The center of SF AI builder culture. Apply; dates posted on Luma."],
 ["cv-hacks","Cerebral Valley AI Hackathons (recurring)","2026-09-12","2026-09-13","~Monthly (SF)","San Francisco","USA","North America","Hackathon","Free","Free (apply)","https://cerebralvalley.ai/hackathons","Cerebral Valley","200–500 / event",92,"Must",False,"Co-runs lab-sponsored hackathons (Anthropic/OpenAI/Google). 20k+ apply for Claude editions."],
 ["aitinkerers","AI Tinkerers Meetups (recurring, global)","2026-07-07","2026-07-07","Monthly (243 cities)","SF / NYC / London / Dubai / Bengaluru …","Global","North America","Hackathon","Free","Free","https://aitinkerers.org/all_cities","AI Tinkerers","50–300 / chapter",78,"Worth",False,"World's largest hands-on builder community. Subscribe to your city chapter."],
 ["lablab","lablab.ai Hackathons (recurring)","2026-07-13","2026-07-20","Every 4–8 wks (online + finals)","Online + SF/Dubai","Global","North America","Hackathon","Free","Free","https://lablab.ai/ai-hackathons","lablab.ai","1,000–5,000 reg",75,"Worth",False,"High-volume online sprints; flagship finals land in Dubai & SF."],
 ["mlh-ghw","MLH Global Hack Week — AI","2026-08-01","2026-08-07","Monthly (AI edition ~Aug)","Online","Global","North America","Hackathon","Free","Free","https://www.mlh.com/","Major League Hacking","5,000–20,000",80,"Worth",False,"Gold-standard student league; recurring GenAI tracks."],
 ["openai-hacks","OpenAI Community Hackathons (recurring)","2026-07-15","2026-07-16","Multiple/month, global","SF / NYC / London / 50+ cities","Global","North America","Hackathon","Free","Free","https://developers.openai.com/community/hackathons","OpenAI (community)","50–500 / event",82,"Must",False,"OpenAI-sponsored community hackathons w/ API credits + Codex access."],
 ["buildspace","buildspace Nights & Weekends (recurring)","2027-01-05","2027-02-16","6-wk cohorts (~quarterly)","Online + SF finale","Global","North America","Hackathon","Free","Free","https://buildspace.so/","buildspace","5,000–15,000 / cohort",75,"Worth",False,"6-week ship-an-AI-product cohort; strong founder community."],
 # ---------- AUGUST 2026 ----------
 ["ai4-26","Ai4 2026","2026-08-04","2026-08-06","Aug 4–6, 2026","Las Vegas","USA","North America","Enterprise & B2B AI","Paid","$1,595–2,395","https://ai4.io/","CloserStill / Ai4","12,000+ (2026)",78,"Worth",True,"Massive multi-industry applied-AI expo; practitioner-heavy, some salesy."],
 ["raysummit26","Ray Summit 2026","2026-08-24","2026-08-26","Aug 24–26, 2026","San Francisco","USA","North America","AI Engineering","Paid","~$600–1,200","https://www.anyscale.com/ray-summit/2026","Anyscale","~2,500",76,"Worth",True,"For engineers serving models/agents at scale on Ray. Niche if not in stack."],
 ["gleango26","Glean:GO 2026","2026-08-26","2026-08-27","Aug 26–27, 2026","San Francisco","USA","North America","Enterprise & B2B AI","Paid","~$500","https://www.glean.com/events/glean-go-2026","Glean","~1,500",62,"Optional",True,"Enterprise AI search/agents; good if selling to IT/knowledge-worker buyers."],
 ["leap26","LEAP 2026","2026-08-31","2026-09-03","Aug 31 – Sep 3, 2026","Riyadh","Saudi Arabia","Middle East","Flagship Tech","Paid","~$400–1,350","https://onegiantleap.com/","MiSK / Saudi MCIT","172,000 (2025)",91,"Worth",True,"Largest MENA tech event; ~2hr flight from Dubai. (2026 moved to Aug/Sep.)"],
 # ---------- SEPTEMBER 2026 ----------
 ["m2020-me26","Money20/20 Middle East 2026","2026-09-14","2026-09-16","Sep 14–16, 2026","Riyadh","Saudi Arabia","Middle East","Enterprise & B2B AI","Paid","~$1,500–3,000","https://money2020middleeast.com/","Money20/20","38,500 (2025)",77,"Worth",True,"AI in payments/banking; strong for fintech-AI founders. Riyadh."],
 ["dreamforce26","Salesforce Dreamforce 2026","2026-09-15","2026-09-17","Sep 15–17, 2026","San Francisco","USA","North America","Enterprise & B2B AI","Paid","$1,500–3,500+","https://www.salesforce.com/dreamforce/","Salesforce","~45,000",95,"Must",True,"World's largest enterprise-software event; 2026 theme = Agentic Enterprise."],
 ["unbound26","HubSpot UNBOUND 2026","2026-09-16","2026-09-18","Sep 16–18, 2026","Boston","USA","North America","Enterprise & B2B AI","Paid","$1,000–2,000","https://unbound.hubspot.com/","HubSpot","~12,000",78,"Worth",True,"Rebrand of INBOUND; GTM/AI-marketing audience. Overlaps Dreamforce."],
 ["agntcon-eu26","AGNTCon + MCPCon Europe 2026","2026-09-17","2026-09-18","Sep 17–18, 2026","Amsterdam","Netherlands","Europe","Agents & MCP","Paid","~$600–1,200","https://events.linuxfoundation.org/agntcon-mcpcon-europe/","Agentic AI Foundation / LF","first EU edition",70,"Worth",True,"European anchor for MCP/open-agent ecosystem (Linux Foundation)."],
 ["cogx26","CogX Summit London 2026","2026-09-23","2026-09-23","Sep 23, 2026","London","UK","Europe","AI Products & Consumer","Paid","£500–1,500","https://www.cogxfestival.com/","CogX Group","~4,000",72,"Worth",True,"Long-running London AI/strategy summit at Royal Albert Hall."],
 ["metaconnect26","Meta Connect 2026","2026-09-23","2026-09-24","Sep 23–24, 2026","Menlo Park","USA","North America","Flagship Tech","Mixed","Free livestream","https://www.meta.com/connect/","Meta","~3,000 in-person",83,"Worth",True,"Meta AI + smart glasses/XR platform announcements."],
 ["oktane26","Oktane 2026","2026-09-22","2026-09-24","Sep 22–24, 2026","Las Vegas","USA","North America","Enterprise & B2B AI","Paid","$1,200–2,000","https://www.okta.com/oktane/","Okta","~5,000",68,"Optional",True,"Identity/auth for AI apps; relevant if you need enterprise SSO/governance."],
 ["gitlab-commit26","GitLab Commit 2026","2026-09-26","2026-09-26","Sep 26, 2026","San Francisco","USA","North America","Vendor Dev Day","Paid","~$299","https://about.gitlab.com/events/","GitLab","~2,000",70,"Worth",False,"GitLab Duo / agentic CI/CD. Verify date on official site."],
 ["bdaiw-asia26","Big Data & AI World Asia 2026","2026-09-29","2026-09-30","Sep 29–30, 2026","Singapore","Singapore","Asia","Enterprise & B2B AI","Mixed","Free expo / $450–900","https://www.singaporetechnologyweek.com/big-data-ai-world","CloserStill","7,000+",65,"Worth",True,"Anchor of Singapore Tech Week; APAC enterprise-AI vendor floor."],
 ["mongodb-nyc26","MongoDB.local NYC 2026","2026-09-30","2026-09-30","Sep 30, 2026","New York","USA","North America","Vendor Dev Day","Paid","$200","https://www.mongodb.com/events/mongodb-local/nyc","MongoDB","~2,000",72,"Worth",True,"Atlas Vector Search, RAG, agent app patterns."],
 ["openai-devday26","OpenAI DevDay 2026","2026-09-29","2026-09-29","Sep 29, 2026","San Francisco","USA","North America","Vendor Dev Day","Paid","$650 (keynote free)","https://devday.openai.com/","OpenAI","~2,500",88,"Must",True,"OpenAI's flagship dev event; satellite DevDay Exchanges follow globally."],
 ["wandb-fc26","W&B Fully Connected 2026","2026-09-29","2026-10-01","Sep 29 – Oct 1, 2026","San Francisco","USA","North America","AI Engineering","Mixed","Free–$300","https://wandb.ai/site/resources/events/fully-connected/","Weights & Biases / CoreWeave","~2,000",77,"Worth",True,"Evals, observability, LLMOps, production AI deployment."],
 ["aiconf26","The AI Conference 2026","2026-09-29","2026-10-01","Sep 29 – Oct 1, 2026","San Francisco","USA","North America","AI Engineering","Paid","~$895–2,495","https://aiconference.com/","The AI Conference","~3,500 (2025)",75,"Worth",True,"Vendor-neutral applied-AI tracks. Clashes w/ W&B FC."],
 ["ethglobal-tokyo","ETHGlobal Tokyo 2026","2026-09-25","2026-09-27","Sep 25–27, 2026","Tokyo","Japan","Asia","Hackathon","Free","Free to hack","https://ethglobal.com/","ETHGlobal","800–1,500",83,"Worth",True,"APAC stop; AI x Crypto track."],
 ["mcp-tokyo26","MCP Dev Summit Tokyo 2026","2026-09-10","2026-09-11","Sep 10–11, 2026","Tokyo","Japan","Asia","Agents & MCP","Paid","~$400–800","https://events.linuxfoundation.org/mcp-dev-summit-tokyo/","Agentic AI Foundation / LF","~600",63,"Optional",True,"APAC MCP edition; skip for NA/EU editions if location flexible."],
 ["reuters-momentum26","Reuters Momentum AI — Austin 2026","2026-09-24","2026-09-25","Sep 24–25, 2026","Austin","USA","North America","Enterprise & B2B AI","Paid","~$3,000–4,500","https://events.reutersevents.com/momentum","Reuters Events","300–600 (curated)",67,"Optional",True,"Invite-only enterprise BD; no expo."],
 # ---------- OCTOBER 2026 ----------
 ["supabase-select26","Supabase Select26","2026-10-02","2026-10-02","Oct 2, 2026","San Francisco","USA","North America","Vendor Dev Day","Paid","$256 (application)","https://select.supabase.com/","Supabase","~400",65,"Worth",True,"Intimate Postgres-for-AI product conf; high founder density."],
 ["ethglobal-mumbai","ETHGlobal Mumbai 2026","2026-10-01","2026-10-03","Oct 1–3, 2026","Mumbai","India","Asia","Hackathon","Free","Free to hack","https://ethglobal.com/","ETHGlobal","800–1,500",82,"Worth",False,"India stop; AI + DeFi tracks. Dates TBC."],
 ["ai-everything-ad26","AI Everything Global (Abu Dhabi) 2026","2026-10-05","2026-10-07","Oct 5–7, 2026","Abu Dhabi","UAE","Middle East","AI Engineering","Mixed","Summit ~AED 2,000 / expo free–500","https://www.adnec.ae/en/eventlisting/ai-everything-abu-dhabi","Kaoun / DCT Abu Dhabi","~15,000",78,"Must",True,"Dedicated cross-industry AI expo; 45 min from Dubai."],
 ["adweek-ny26","Advertising Week New York 2026","2026-10-05","2026-10-08","Oct 5–8, 2026","New York","USA","North America","AI Marketing & Creative","Mixed","Free–$1,500+","https://advertisingweek.com/event/awnewyork-2026/","Advertising Week","15,000–20,000",87,"Worth",True,"AI/agentic tech is a headline 2026 theme."],
 ["wsai-amsterdam26","World Summit AI 2026","2026-10-07","2026-10-08","Oct 7–8, 2026","Amsterdam","Netherlands","Europe","Enterprise & B2B AI","Paid","€1,200–2,500","https://worldsummit.ai/","Prestige Events","10,000+",84,"Must",True,"Europe's premier enterprise-AI summit; anchor of World AI Week."],
 ["cypher26","Cypher 2026 (AIM)","2026-10-07","2026-10-09","Oct 7–9, 2026","Bengaluru","India","Asia","AI Engineering","Paid","~$180–540","https://cypher.analyticsindiamag.com/","Analytics India Magazine","5,000+",73,"Worth",True,"India's largest practitioner AI/ML conference. Best India ecosystem access."],
 ["productcon-sf26","ProductCon San Francisco 2026","2026-10-07","2026-10-07","Oct 7, 2026","San Francisco","USA","North America","AI Products & Consumer","Paid","~$299–999 (free stream)","https://productschool.com/productcon/san-francisco-2026","Product School","3,000+",65,"Worth",True,"Senior PM/CPO crowd; strategic not technical."],
 ["atlassian-team-eu26","Atlassian Team '26 Europe","2026-10-06","2026-10-08","Oct 6–8, 2026","Amsterdam","Netherlands","Europe","Enterprise & B2B AI","Paid","€700–1,500","https://events.atlassian.com/teameurope","Atlassian","~3,000",70,"Worth",True,"AI agents (Rovo) for eng/ops/ITSM teams."],
 ["aie-summit-nyc26","AI Engineer Summit NYC 2026","2026-10-12","2026-10-14","Oct 12–14, 2026","New York","USA","North America","AI Engineering","Paid","~$800–1,600","https://www.ai.engineer/nyc/2026","AI.Engineer","~800",82,"Must",False,"East-coast AI-engineering flagship. (Date being verified.)"],
 ["workday-us26","Workday Rising US 2026","2026-10-12","2026-10-15","Oct 12–15, 2026","Las Vegas","USA","North America","Enterprise & B2B AI","Paid","$1,500–2,500","https://rising.workday.com/us.html","Workday","~15,000",72,"Worth",True,"For founders targeting CHRO/CFO buyers."],
 ["tcdisrupt26","TechCrunch Disrupt 2026","2026-10-13","2026-10-15","Oct 13–15, 2026","San Francisco","USA","North America","Flagship Tech","Paid","$559+","https://techcrunch.com/events/techcrunch-disrupt/","TechCrunch","~10,000",87,"Must",True,"Densest VC+founder concentration in October. Work the corridors."],
 ["maicon26","MAICON 2026","2026-10-13","2026-10-15","Oct 13–15, 2026","Cleveland","USA","North America","AI Marketing & Creative","Paid","$1,799–2,999","https://www.marketingaiinstitute.com/events/marketing-artificial-intelligence-conference","Marketing AI Institute","~1,500–2,000",77,"Worth",True,"The flagship US marketing-AI conference."],
 ["vercelship-sf26","Vercel Ship 26 — San Francisco","2026-10-15","2026-10-15","Oct 15, 2026","San Francisco","USA","North America","AI Engineering","Paid","$250–500","https://vercel.com/ship/sf","Vercel","~2,500 (London)",80,"Must",True,"AI SDK / v0 / agent deployment. (You're registered.)"],
 ["cloudflare-connect26","Cloudflare Connect 2026","2026-10-19","2026-10-21","Oct 19–21, 2026","San Francisco","USA","North America","Vendor Dev Day","Paid","$595","https://www.cloudflare.com/connect/","Cloudflare","2,500+",78,"Worth",True,"Workers AI / AI Gateway / edge inference."],
 ["grafana-obscon26","Grafana ObservabilityCON 2026","2026-10-19","2026-10-21","Oct 19–21, 2026","San Francisco","USA","North America","Vendor Dev Day","Free","Free","https://grafana.com/events/observabilitycon/","Grafana Labs","~2,000",72,"Worth",True,"AI observability / LLM tracing. Free."],
 ["aibde-eu26","AI & Big Data Expo Europe 2026","2026-10-19","2026-10-20","Oct 19–20, 2026","Amsterdam","Netherlands","Europe","AI Engineering","Paid","€599–1,499","https://www.ai-expo.net/europe/","TechEx","6,000–8,000",70,"Worth",True,"Applied-AI vendor show; co-located w/ 4 other expos."],
 ["gartner-us26","Gartner IT Symposium/Xpo US 2026","2026-10-19","2026-10-22","Oct 19–22, 2026","Orlando","USA","North America","Enterprise & B2B AI","Paid","$4,000–5,500","https://www.gartner.com/en/conferences/na/symposium-us","Gartner","~10,000",82,"Worth",True,"Unmatched CIO density; pricey. For enterprise lighthouse customers."],
 ["agntcon-na26","AGNTCon + MCPCon North America 2026","2026-10-22","2026-10-23","Oct 22–23, 2026","San Jose","USA","North America","Agents & MCP","Paid","~$600–1,200","https://aaif.io/","Agentic AI Foundation / LF","~1,200",75,"Must",True,"Where the MCP/agent protocol direction is set. ~45 min from SF."],
 ["encode-london26","Encode London Hackathon & Conf 2026","2026-10-23","2026-10-25","Oct 23–25, 2026","London","UK","Europe","Hackathon","Free","Free (apply)","https://luma.com/encode-london-2026","Encode Club","300–500",72,"Worth",True,"AI Agents / Creative AI / Onchain AI tracks."],
 ["hashiconf26","HashiConf 2026 (@ IBM TechXchange)","2026-10-26","2026-10-29","Oct 26–29, 2026","Atlanta","USA","North America","Vendor Dev Day","Paid","$1,119–1,599","https://www.hashicorp.com/en/conferences/hashiconf","HashiCorp (IBM)","~5,000",76,"Worth",True,"Terraform for AI GPU infra, Vault for LLM secrets."],
 ["dubai-aifest26","Dubai AI Festival 2026","2026-10-26","2026-10-27","Oct 26–27, 2026","Dubai","UAE","Middle East","AI Products & Consumer","Mixed","Free–AED 1,500","https://dubaiaifestival.com/","DIFC","~10,000",72,"Must",True,"Dubai home-turf; AI startups, GenAI products, fintech AI."],
 ["odsc-west26","ODSC AI West 2026","2026-10-27","2026-10-29","Oct 27–29, 2026","Burlingame","USA","North America","AI Engineering","Paid","~$399+ (free virtual)","https://odsc.ai/west/","ODSC Media","~2,500",70,"Optional",True,"ML-practitioner heavy; free virtual covers keynotes."],
 ["scale-product26","@Scale: Product 2026","2026-10-28","2026-10-28","Oct 28, 2026","Menlo Park","USA","North America","Enterprise & B2B AI","Free","Free","https://atscaleconference.com/events/product-2026/","Meta Engineering","—",74,"Worth",True,"Free AI-native product-eng content from Meta infra teams."],
 ["github-universe26","GitHub Universe 2026","2026-10-28","2026-10-29","Oct 28–29, 2026","San Francisco","USA","North America","AI Engineering","Paid","$799+ (virtual free)","https://githubuniverse.com/","GitHub (Microsoft)","~3,500",84,"Must",True,"GitHub's AI dev-tooling roadmap (Copilot agents)."],
 # ---------- NOVEMBER 2026 ----------
 ["adipec26","ADIPEC 2026","2026-11-02","2026-11-05","Nov 2–5, 2026","Abu Dhabi","UAE","Middle East","Enterprise & B2B AI","Mixed","Free expo / $500–2,000","https://www.adipec.com/","ADNEC","239,000 (2025)",85,"Worth",True,"Energy giant; AI & Digital is now its #1 track. 45 min from Dubai."],
 ["dubai-fintech26","Dubai FinTech Summit 2026","2026-11-02","2026-11-03","Nov 2–3, 2026","Dubai","UAE","Middle East","Enterprise & B2B AI","Paid","~$800–2,500","https://dubaifintechsummit.com/","DIFC","~6,000",73,"Worth",True,"Dubai home; AI-in-finance, regulators, C-suite."],
 ["boxworks26","BoxWorks 2026","2026-11-05","2026-11-06","Nov 5–6, 2026","San Francisco","USA","North America","Enterprise & B2B AI","Paid","$549–749","https://boxworks.box.com/","Box","~10,000",65,"Worth",True,"AI for unstructured content / document workflows."],
 ["websummit26","Web Summit 2026","2026-11-09","2026-11-12","Nov 9–12, 2026","Lisbon","Portugal","Europe","Flagship Tech","Paid","€895–2,200","https://websummit.com/","Web Summit","70,000+",88,"Must",True,"Best single AI-founder networking event in Europe."],
 ["adobemax26","Adobe MAX 2026","2026-11-10","2026-11-12","Nov 10–12, 2026","Miami Beach","USA","North America","AI Marketing & Creative","Mixed","$1,595+ (free online)","https://max.adobe.com/","Adobe","10,000+ in-person",91,"Worth",True,"Firefly / generative video / AI creative tools. Free online option."],
 ["gartner-eu26","Gartner IT Symposium/Xpo Europe 2026","2026-11-09","2026-11-12","Nov 9–12, 2026","Barcelona","Spain","Europe","Enterprise & B2B AI","Paid","€3,500–5,000","https://www.gartner.com/en/conferences/emea/symposium-spain","Gartner","~7,000",80,"Worth",True,"Best European CIO-level access; EU AI Act focus."],
 ["vapicon26","VapiCon 2026","2026-11-11","2026-11-12","Nov 11–12, 2026","San Francisco","USA","North America","Agents & MCP","Paid","TBD (waitlist)","https://vapi.ai/vapicon","Vapi","700+ (2025)",62,"Optional",True,"Voice-AI infra; only if voice is on your roadmap. Fort Mason."],
 ["nvidia-japan26","NVIDIA AI Summit Japan 2026","2026-11-12","2026-11-13","~Nov 2026","Tokyo","Japan","Asia","Vendor Dev Day","Mixed","Free (reg) / paid enterprise","https://blogs.nvidia.com/blog/ai-summit-japan/","NVIDIA","3,000–5,000",77,"Worth",False,"Physical AI, robotics, enterprise LLM. Date est."],
 ["cv-summit26","Cerebral Valley AI Summit SF 2026","2026-11-12","2026-11-12","Nov 12, 2026","San Francisco","USA","North America","AI Products & Consumer","Mixed","~$99 founder / $599 (invite)","https://www.cerebralvalley.com/","Newcomer / Volley","~400–600",72,"Worth",True,"Invite-only; the room IS your peer set (frontier founders + VCs)."],
 ["slush26","Slush 2026","2026-11-18","2026-11-19","Nov 18–19, 2026","Helsinki","Finland","Europe","Flagship Tech","Paid","~€1,500–2,500","https://slush.org/","Slush","~13,000",80,"Must",True,"Highest investor-to-founder ratio anywhere. Best for fundraising."],
 ["sff26","Singapore FinTech Festival 2026","2026-11-18","2026-11-20","Nov 18–20, 2026","Singapore","Singapore","Asia","Enterprise & B2B AI","Paid","~$600–1,650","https://www.fintechfestival.sg/","MAS","66,000+",83,"Worth",True,"World's largest fintech event; AI-in-finance dominant."],
 ["msignite26","Microsoft Ignite 2026","2026-11-17","2026-11-20","Nov 17–20, 2026","San Francisco","USA","North America","Flagship Tech","Paid","~$2,400 (digital free)","https://ignite.microsoft.com/","Microsoft","20,000+",92,"Must",True,"Azure AI Foundry, Copilot Studio. Enterprise IT heavy; digital free."],
 ["qconsf26","QCon San Francisco 2026","2026-11-16","2026-11-18","Nov 16–18, 2026","San Francisco","USA","North America","AI Engineering","Paid","$2,595+","https://qconsf.com/","C4Media / InfoQ","~1,000",80,"Worth",True,"Senior-engineer depth; ~1/3 tracks AI."],
 ["aie-code26","AI Engineer CODE Summit NYC 2026","2026-11-19","2026-11-22","Nov 19–22, 2026","New York","USA","North America","AI Engineering","Paid","~$800–1,600","https://www.ai.engineer/code/2026","AI.Engineer","~500",78,"Must",False,"Only conf solely on AI coding agents. (Being verified.)"],
 ["brandweek26","Brandweek 2026","2026-11-09","2026-11-11","Nov 9–11, 2026","Atlanta","USA","North America","AI Marketing & Creative","Paid","~$2,000–3,500","https://event.adweek.com/brandweek_2026","Adweek","~2,500",75,"Optional",True,"Senior CMO audience; dedicated AI track."],
 # ---------- DECEMBER 2026 ----------
 ["saastr-london26","SaaStr AI London 2026","2026-12-01","2026-12-02","~Dec 1–2, 2026","London","UK","Europe","Enterprise & B2B AI","Paid","$500–1,500","https://saastrlondon.com/","SaaStr","~2,500",72,"Worth",False,"Europe's B2B-SaaS founder+VC event. Dates est."],
 ["apidays-paris26","apidays GenerationAI Paris 2026","2026-12-01","2026-12-03","Dec 1–3, 2026","Paris","France","Europe","AI Engineering","Paid","€400–1,200","https://www.generationaiconf.com/events/paris","apidays","2,500–3,000",65,"Worth",True,"Developer-centric: AI APIs, agents, enterprise LLM integration."],
 ["reinvent26","AWS re:Invent 2026","2026-11-30","2026-12-04","Nov 30 – Dec 4, 2026","Las Vegas","USA","North America","Flagship Tech","Paid","~$1,799","https://aws.amazon.com/events/reinvent/","AWS","60,000+",97,"Must",True,"World's largest cloud+AI conference. re:Inforce merged in for 2026."],
 ["gitex26","GITEX Global 2026","2026-12-07","2026-12-11","Dec 7–11, 2026","Dubai","UAE","Middle East","Flagship Tech","Paid","~$950–2,050","https://www.gitex.com/gitex-global-2026","Kaoun / DWTC","200,000+",96,"Must",True,"World's largest tech expo. 2026 moved to Dec at Expo City. AI hackathon embedded. Dubai home."],
 ["northstar26","Expand North Star 2026","2026-12-08","2026-12-10","Dec 8–10, 2026","Dubai","UAE","Middle East","AI Products & Consumer","Paid","~$400–800 (or GITEX bundle)","https://expandnorthstar.com/","Kaoun / Dubai Chamber","~100,000",82,"Must",True,"World's largest startup-investor event; nested in GITEX week."],
 ["adfw26","Abu Dhabi Finance Week 2026","2026-12-07","2026-12-10","Dec 7–10, 2026","Abu Dhabi","UAE","Middle East","Enterprise & B2B AI","Mixed","Free–$2,000","https://www.adfw.com/","ADGM","35,000 (2025)",76,"Worth",True,"AI in finance + sovereign investment. Overlaps GITEX week."],
 ["aisummit-ny26","The AI Summit New York 2026","2026-12-09","2026-12-10","Dec 9–10, 2026","New York","USA","North America","Enterprise & B2B AI","Paid","$1,500–3,000","https://newyork.theaisummit.com/","Informa Tech","4,000+",73,"Worth",True,"East-coast commercial-AI; 10th edition. (Hackathon embedded.)"],
 # ---------- JANUARY 2027 ----------
 ["ces27","CES 2027","2027-01-06","2027-01-09","Jan 6–9, 2027","Las Vegas","USA","North America","Flagship Tech","Paid","~$1,500–2,000+","https://www.ces.tech/","CTA","148,000 (2025)",95,"Worth",True,"AI is the defining theme; unmatched for hardware/product discovery + press."],
 ["1bn27","1 Billion Followers Summit 2027","2027-01-08","2027-01-10","Jan 8–10, 2027","Dubai","UAE","Middle East","AI Marketing & Creative","Paid","~AED 500–3,000","https://www.1billionsummit.com/","Dubai Gov Media Office","~30,000",68,"Worth",True,"Creator economy; AI content tools. Dubai home."],
 # ---------- FEBRUARY 2027 ----------
 ["wsqatar27","Web Summit Qatar 2027","2027-01-31","2027-02-03","Jan 31 – Feb 3, 2027","Doha","Qatar","Middle East","Flagship Tech","Paid","~$500–1,500","https://qatar.websummit.com/","Web Summit","~30,000",75,"Worth",True,"MENA market entry + Gulf SWF exposure. 1hr from Dubai."],
 ["wgs27","World Governments Summit 2027","2027-02-01","2027-02-03","Feb 1–3, 2027","Dubai","UAE","Middle East","Enterprise & B2B AI","Mixed","Invite / public forums free","https://www.worldgovernmentssummit.org/","WGS Org","6,000+; 150 govts",88,"Must",True,"Premier GovTech/AI-governance summit. Dubai home."],
 ["leap27","LEAP 2027","2027-02-03","2027-02-06","Feb 3–6, 2027","Riyadh","Saudi Arabia","Middle East","Flagship Tech","Paid","~$400–1,350","https://onegiantleap.com/","MiSK / Saudi MCIT","172,000+",91,"Must",True,"Biggest MENA tech event; AI/cloud/fintech. ~2hr from Dubai."],
 ["step27","Step Conference Dubai 2027","2027-02-03","2027-02-04","Feb 3–4, 2027","Dubai","UAE","Middle East","AI Products & Consumer","Paid","~$200–800","https://dubai.stepconference.com/","Step Group","~7,000",68,"Worth",True,"Longest-running MENA startup festival. Dubai home (same dates as LEAP)."],
 # ---------- MARCH 2027 ----------
 ["humanx27","HumanX 2027","2027-03-07","2027-03-10","Mar 7–10, 2027","Las Vegas","USA","North America","Enterprise & B2B AI","Paid","$2,500–4,500","https://www.humanx.co/","HumanX","9,500+ (2027)",82,"Worth",True,"Fastest-scaling broad AI conference; VP/C-suite + founders."],
 ["mwc27","Mobile World Congress 2027","2027-03-01","2027-03-04","Mar 1–4, 2027","Barcelona","Spain","Europe","Flagship Tech","Paid","€900–2,000+","https://www.mwcbarcelona.com/","GSMA","109,000",92,"Optional",True,"Telecom/5G core; on-device & edge AI growing. Optional unless AI touches connectivity."],
 ["gtc27","NVIDIA GTC 2027","2027-03-14","2027-03-18","Mar 14–18, 2027","San Jose","USA","North America","AI Engineering","Mixed","Keynote free / $1,299+","https://www.nvidia.com/gtc/","NVIDIA","25,000+",92,"Must",True,"Jensen keynote; inference/CUDA/NIM/agent + AI-platform roadmap."],
 ["sxsw27","SXSW 2027","2027-03-13","2027-03-21","Mar 13–21, 2027","Austin","USA","North America","Flagship Tech","Paid","~$1,395–2,200","https://sxsw.com/","SXSW","350,000+ (all)",93,"Worth",True,"AI Revolution + Creative Renaissance headline tracks. Best for consumer-AI + media."],
 ["rise27","RISE 2027","2027-03-01","2027-03-04","~Mar 2027","Hong Kong","Hong Kong","Asia","Flagship Tech","Paid","~$1,200–2,500","https://riseconf.com/","Web Summit","12,000–16,000",76,"Worth",False,"Web Summit's Asia flagship; APAC investor network. Date est."],
 ["adobesummit27","Adobe Summit 2027","2027-03-22","2027-03-25","Mar 22–25, 2027","Las Vegas","USA","North America","AI Marketing & Creative","Paid","~$1,700–2,200","https://summit.adobe.com/","Adobe","15,000+",83,"Worth",True,"Enterprise marketing AI (GenStudio, content supply chain)."],
 ["bdaiw-london27","Big Data & AI World London 2027","2027-03-10","2027-03-11","Mar 10–11, 2027","London","UK","Europe","Enterprise & B2B AI","Paid","£299–999 (free expo)","https://www.bigdataworld.com/","CloserStill","~12,000 (Tech Show)","",71,"Worth",True].__len__ and None,
 # (placeholder removed below)
 # ---------- APRIL 2027 ----------
 ["gcnext27","Google Cloud Next 2027","2027-04-13","2027-04-15","~Apr 2027","Las Vegas","USA","North America","Flagship Tech","Paid","~$1,799","https://cloud.google.com/next","Google Cloud","30,000+",91,"Must",False,"Gemini / Vertex AI enterprise platform. Dates est."],
 ["nab27","NAB Show 2027","2027-04-04","2027-04-07","Apr 4–7, 2027","Las Vegas","USA","North America","AI Marketing & Creative","Mixed","Free floor / $500–1,200","https://www.nabshow.com/las-vegas/","NAB","90,000+",86,"Worth",True,"AI in media/generative video/post-production. World's largest media-tech show."],
 ["possible27","POSSIBLE Miami 2027","2027-04-05","2027-04-07","Apr 5–7, 2027","Miami Beach","USA","North America","AI Marketing & Creative","Mixed","Free (brand) / $1,500–3,500","https://possibleevent.com/","POSSIBLE","5,400 (2026)",80,"Worth",True,"Fast-growing senior-marketing conf; dedicated AI Verse track."],
 ["gitex-africa27","GITEX Africa 2027","2027-04-26","2027-04-28","Apr 26–28, 2027","Marrakech","Morocco","Africa","Flagship Tech","Paid","~$200–800","https://gitexafrica.com/","Kaoun","~30,000",72,"Optional",True,"African market access; B2G AI. 3.5hr from Dubai."],
 ["m2020-asia27","Money20/20 Asia 2027","2027-04-27","2027-04-29","Apr 27–29, 2027","Bangkok","Thailand","Asia","Enterprise & B2B AI","Paid","~$2,500–4,500","https://asia.money2020.com/","Money20/20","4,500 (2026)",76,"Optional",True,"AI in payments/fintech; senior exec audience."],
 ["gitex-ai-asia27","GITEX AI Asia 2027","2027-04-29","2027-04-30","Apr 29–30, 2027","Singapore","Singapore","Asia","AI Products & Consumer","Paid","~$350–1,000","https://gitexasia.com/","Kaoun / DWTC","50,000+ claimed",70,"Worth",True,"GITEX Asia; AI products + startups. Overlaps Money20/20 Asia."],
 ["aie-europe27","AI Engineer Europe 2027","2027-04-07","2027-04-09","~Apr 2027","London","UK","Europe","AI Engineering","Paid","~£600–1,200","https://www.ai.engineer/europe/","AI.Engineer","~1,000 (2026)",80,"Must",False,"Best European applied-AI-engineering conf. Date est."],
 ["grafanacon27","GrafanaCON 2027","2027-04-19","2027-04-21","~Apr 2027","TBD (Europe)","TBD","Europe","Vendor Dev Day","Mixed","Free virtual / ~€299","https://grafana.com/events/grafanacon/","Grafana Labs","~3,000",70,"Worth",False,"AI observability flagship. Location/date est."],
 # ---------- MAY 2027 ----------
 ["googleio27","Google I/O 2027","2027-05-11","2027-05-13","~May 2027","Mountain View","USA","North America","Flagship Tech","Mixed","Free (lottery) / virtual free","https://io.google/","Google","~7,000 in-person",95,"Must",False,"Gemini / AI Studio / Android. Dates est (typically mid-May)."],
 ["msbuild27","Microsoft Build 2027","2027-05-19","2027-05-21","~May 2027","Seattle","USA","North America","Flagship Tech","Paid","~$1,799","https://build.microsoft.com/","Microsoft","~10,000",90,"Must",False,"Copilot Studio / Azure AI Foundry / MCP. Dates est."],
 ["cwc27","Anthropic Code with Claude 2027","2027-05-05","2027-05-05","~May 2027","San Francisco","USA","North America","Vendor Dev Day","Free","Free (livestreamed)","https://claude.com/code-with-claude","Anthropic","~3,000 (multi-city)",72,"Must",False,"Anthropic's dev conference (SF/London/Tokyo). Dates est."],
 ["interrupt27","LangChain Interrupt 2027","2027-05-12","2027-05-13","~May 2027","San Francisco","USA","North America","Agents & MCP","Paid","~$500–900","https://interrupt.langchain.com/","LangChain","~900 (2026)",82,"Must",False,"Best single conf for agentic-AI practitioners (LangGraph/LangSmith). Dates est."],
 ["stripe-sessions27","Stripe Sessions 2027","2027-05-05","2027-05-06","May 5–6, 2027","San Francisco","USA","North America","Vendor Dev Day","Paid","~$599","https://stripe.com/sessions","Stripe","~6,000",88,"Must",True,"Agent billing / usage-based pricing / AI monetisation."],
 ["twilio-signal27","Twilio SIGNAL 2027","2027-05-05","2027-05-06","~May 2027","San Francisco","USA","North America","Vendor Dev Day","Paid","~$799","https://signal.twilio.com/","Twilio","~5,000",80,"Worth",False,"Conversational AI / agent voice+SMS handoffs. Dates est."],
 ["snow-knowledge27","ServiceNow Knowledge 2027","2027-05-04","2027-05-06","May 4–6, 2027","Las Vegas","USA","North America","Enterprise & B2B AI","Paid","$1,500–2,500","https://www.servicenow.com/events/knowledge.html","ServiceNow","~22,000",80,"Worth",True,"AI agents for IT/ops workflows; 20th edition."],
 ["saastr27","SaaStr Annual 2027","2027-05-11","2027-05-13","~May 2027","San Mateo","USA","North America","Enterprise & B2B AI","Mixed","Free–$1,500","https://saastr.ai/events/annual","SaaStr","~12,000",83,"Must",False,"Highest-density B2B-SaaS founder+VC event. Dates est."],
 ["datainnov27","Data Innovation Summit 2027","2027-05-18","2027-05-20","May 18–20, 2027","Stockholm","Sweden","Europe","AI Engineering","Paid","€799–1,499","https://datainnovationsummit.com/region/nordics/","Corinium","3,500+",73,"Worth",True,"Nordic applied-AI; dedicated Agentic AI & GenAI track."],
 ["current27","Confluent Current 2027","2027-05-18","2027-05-19","~May 2027","TBD (USA)","USA","North America","Vendor Dev Day","Paid","~$699","https://current.confluent.io/","Confluent","~3,000",72,"Worth",False,"Streaming for AI agents / real-time ML. Location/date est."],
 # ---------- JUNE 2027 ----------
 ["aisummit-london27","The AI Summit London 2027","2027-06-09","2027-06-10","Jun 9–10, 2027","London","UK","Europe","Enterprise & B2B AI","Paid","£1,200–2,800","https://london.theaisummit.com/","Informa Tech","~4,500",85,"Must",True,"Flagship of London Tech Week; best EU enterprise-AI deal flow."],
 ["vivatech27","VivaTech 2027","2027-06-16","2027-06-19","Jun 16–19, 2027","Paris","France","Europe","Flagship Tech","Mixed","€50–2,500","https://vivatech.com/","VivaTech","200,000+",88,"Must",True,"Largest tech event in continental Europe; AI central."],
 ["dash27","Datadog DASH 2027","2027-06-15","2027-06-17","Jun 15–17, 2027","New York","USA","North America","AI Engineering","Paid","~$599","https://dash.datadoghq.com/","Datadog","~5,000",84,"Must",True,"LLM Observability / agent monitoring / AI cost management."],
 ["config27","Figma Config 2027","2027-06-22","2027-06-24","~Jun 2027","San Francisco","USA","North America","Vendor Dev Day","Mixed","Free virtual / ~$299","https://config.figma.com/","Figma","~40,000 (in-person+virtual)",87,"Worth",False,"AI design generation / designer-engineer handoff. Dates est."],
 ["cannes27","Cannes Lions 2027","2027-06-21","2027-06-25","~Jun 21–25, 2027","Cannes","France","Europe","AI Marketing & Creative","Paid","€5,000–8,000+","https://www.canneslions.com/","LIONS","15,000+",96,"Worth",False,"Most prestigious creativity festival; AI dominant. Pricey. Dates est."],
 ["superai27","SuperAI Singapore 2027","2027-06-18","2027-06-19","~Jun 2027","Singapore","Singapore","Asia","AI Products & Consumer","Paid","~$300–1,200","https://superai.com/","SuperAI","6,000+ (2025)",78,"Worth",False,"APAC's flagship applied-AI festival. Dates est."],
 ["gtc-taipei27","GTC Taipei 2027","2027-06-01","2027-06-04","~Jun 2027","Taipei","Taiwan","Asia","AI Engineering","Mixed","Free dev pass / paid sessions","https://www.nvidia.com/en-tw/gtc/taipei/","NVIDIA","5,000+",84,"Worth",False,"NVIDIA APAC roadmap (timed w/ Computex). Dates est."],
 ["aiewf27","AI Engineer World's Fair 2027","2027-06-28","2027-07-01","~Late Jun 2027","San Francisco","USA","North America","AI Engineering","Paid","~$900–1,700","https://www.ai.engineer/","AI.Engineer","~6,000+",92,"Must",False,"The global must-attend for AI engineers. Dates est (may graze window end)."],
]

# Fix the one malformed row (Big Data & AI World London) cleanly:
E = [row for row in E if row and row[0] != "bdaiw-london27"]
E.append(["bdaiw-london27","Big Data & AI World London 2027","2027-03-10","2027-03-11","Mar 10–11, 2027","London","UK","Europe","Enterprise & B2B AI","Paid","£299–999 (free expo)","https://www.bigdataworld.com/","CloserStill","~12,000 (Tech Show)",71,"Worth",True,"UK enterprise data+AI; co-located w/ Tech Show London."])

KEYS = ["id","name","ds","de","dd","city","country","region","cat","fop","cost","url","org","att","rep","rel","conf","note"]
EVENTS = [dict(zip(KEYS, r)) for r in E]

# ---- Senior-review adjustments ----
DROP = {"leap26","hashiconf26","atlassian-team-eu26","workday-us26","datainnov27","current27"}
EVENTS = [e for e in EVENTS if e["id"] not in DROP]

OVERRIDES = {
 "aie-summit-nyc26": {"conf": True, "note": "East-coast AI-engineering flagship. Sheraton NY Times Square."},
 "aie-code26": {"conf": True, "note": "Only conference solely on AI coding agents."},
 "gcnext27": {"conf": True, "ds": "2027-04-13", "de": "2027-04-15", "dd": "Apr 13–15, 2027", "city": "Las Vegas", "note": "Gemini / Vertex AI enterprise platform. Mandalay Bay, Las Vegas."},
 "vapicon26": {"conf": False, "ds": "2026-10-02", "de": "2026-10-02", "dd": "~Oct 2026 (TBC)", "note": "Voice-AI infra; 2026 date TBC (inaugural was Oct 2, 2025)."},
 "aie-europe27": {"note": "Best European applied-AI-engineering conf. City & dates TBC."},
}
for e in EVENTS:
    if e["id"] in OVERRIDES:
        e.update(OVERRIDES[e["id"]])

ADD = [
 ["aie-paris26","AI Engineer Paris 2026","2026-09-23","2026-09-24","Sep 23–24, 2026","Paris","France","Europe","AI Engineering","Paid","~€500–1,000","https://www.ai.engineer/paris/2026","AI.Engineer","~700",80,"Worth",False,"ai.engineer's Paris edition (Station F); verify dates."],
 ["databricks27","Databricks Data + AI Summit 2027","2027-06-15","2027-06-18","~Jun 2027","San Francisco","USA","North America","Enterprise & B2B AI","Paid","~$1,699","https://www.databricks.com/dataaisummit","Databricks","30,000+",85,"Worth",False,"Agents/LLMOps/GenAI in production (data-platform heavy). Dates est."],
 ["wwdc27","Apple WWDC 2027","2027-06-07","2027-06-11","~Jun 2027","Cupertino","USA","North America","AI Products & Consumer","Free","Free (online)","https://developer.apple.com/wwdc/","Apple","online free",88,"Worth",False,"Apple Intelligence / on-device LLMs / Core ML. Online free. Dates est."],
 ["globalaishow-ad26","Global AI Show Abu Dhabi 2026","2026-11-12","2026-11-13","Nov 12–13, 2026","Abu Dhabi","UAE","Middle East","Enterprise & B2B AI","Paid","~$300–900","https://www.globalaishow.com/abu-dhabi/","Global AI Show","10,000+",72,"Worth",True,"MENA enterprise-AI; ~45 min from Dubai."],
 ["aws-london27","AWS Summit London 2027","2027-04-22","2027-04-22","~Apr 2027","London","UK","Europe","Vendor Dev Day","Free","Free","https://aws.amazon.com/events/summits/london/","AWS","15,000+",80,"Worth",False,"Free; Bedrock / AI builder track. Pairs w/ AI Engineer Europe. Date est."],
 ["token2049-sg26","TOKEN2049 Singapore 2026","2026-10-07","2026-10-08","Oct 7–8, 2026","Singapore","Singapore","Asia","AI Products & Consumer","Paid","~$1,000–2,000","https://www.token2049.com/singapore","TOKEN2049","25,000+",75,"Optional",True,"AI x crypto / on-chain agents — relevant given your crypto background."],
 ["aidevworld27","AI DevWorld 2027","2027-02-09","2027-02-11","Feb 9–11, 2027","Santa Clara","USA","North America","AI Engineering","Paid","~$499–999","https://aidevworld.com/","DeveloperWeek","3,000+",70,"Optional",True,"Co-located w/ DeveloperWeek; open-source LLMs, agents, enterprise AI."],
]
EVENTS += [dict(zip(KEYS, r)) for r in ADD]

EVENTS.sort(key=lambda e: (e["ds"], e["name"]))

os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, "ai-events-data.json"), "w") as f:
    json.dump(EVENTS, f, indent=1, ensure_ascii=False)

DATA_JSON = json.dumps(EVENTS, ensure_ascii=False)

HTML = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Events Calendar · Jul 2026 – Jun 2027</title>
<style>
:root{
 --bg:#0b0e14; --panel:#141925; --panel2:#1b2233; --line:#26304a; --txt:#e6eaf2; --mut:#8a94a8;
 --acc:#6ea8fe; --going:#1f9d55; --maybe:#c98a13; --skip:#9aa3b2;
 --must:#16a34a; --worth:#2563eb; --opt:#a16207;
}
*{box-sizing:border-box} html,body{margin:0}
body{background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none} a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:30;background:rgba(11,14,20,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 18px}
.h-top{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
h1{font-size:18px;margin:0;font-weight:700}
.sub{color:var(--mut);font-size:12px}
.stats{margin-left:auto;display:flex;gap:14px;font-size:12px;color:var(--mut)}
.stats b{color:var(--txt)}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px}
input[type=search]{background:var(--panel);border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:7px 11px;min-width:220px;font-size:13px}
select{background:var(--panel);border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:7px 9px;font-size:12px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{background:var(--panel);color:var(--mut);border:0;padding:7px 12px;font-size:12px;cursor:pointer}
.seg button.on{background:var(--acc);color:#06101f;font-weight:600}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.chip{border:1px solid var(--line);background:var(--panel);color:var(--mut);border-radius:999px;padding:4px 10px;font-size:11.5px;cursor:pointer;user-select:none}
.chip.on{background:var(--panel2);color:var(--txt);border-color:var(--acc)}
.rng{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mut)}
.btn{background:var(--panel2);border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:7px 12px;font-size:12px;cursor:pointer}
.btn:hover{border-color:var(--acc)}
main{max-width:1100px;margin:0 auto;padding:18px}
.month{font-size:13px;font-weight:700;color:var(--acc);letter-spacing:.04em;text-transform:uppercase;margin:22px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.card{display:grid;grid-template-columns:78px 1fr auto;gap:14px;background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:12px 14px;margin:9px 0;align-items:start}
.card.going{border-color:var(--going);box-shadow:inset 3px 0 0 var(--going)}
.card.maybe{border-color:var(--maybe);box-shadow:inset 3px 0 0 var(--maybe)}
.card.skip{opacity:.5}
.date{font-size:12px;color:var(--mut);text-align:center;padding-top:2px}
.date .d{font-size:20px;font-weight:700;color:var(--txt);line-height:1}
.date .m{text-transform:uppercase;font-size:10.5px;letter-spacing:.06em}
.mid h3{margin:0 0 4px;font-size:15px}
.meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:11.5px;color:var(--mut);margin-bottom:5px}
.tag{border-radius:5px;padding:1px 7px;font-size:10.5px;font-weight:600;white-space:nowrap}
.note{color:#c3cbd9;font-size:12.5px}
.loc{color:var(--txt)}
.badge-rel{border-radius:5px;padding:1px 7px;font-size:10.5px;font-weight:700;color:#fff}
.unconf{color:var(--maybe);font-size:10.5px;border:1px dashed var(--maybe);border-radius:5px;padding:0 5px}
.right{display:flex;flex-direction:column;align-items:flex-end;gap:8px;min-width:128px}
.rep{display:flex;align-items:center;gap:7px}
.repbar{width:70px;height:7px;border-radius:4px;background:var(--panel2);overflow:hidden}
.repfill{height:100%}
.repnum{font-weight:700;font-size:13px;width:26px;text-align:right}
.status{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.status button{background:var(--panel2);color:var(--mut);border:0;padding:5px 9px;font-size:11px;cursor:pointer}
.status button.going.on{background:var(--going);color:#fff}
.status button.maybe.on{background:var(--maybe);color:#06101f}
.status button.skip.on{background:var(--skip);color:#06101f}
.empty{color:var(--mut);text-align:center;padding:50px}
footer{color:var(--mut);font-size:11px;text-align:center;padding:26px 18px;border-top:1px solid var(--line);margin-top:30px}
@media(max-width:640px){.card{grid-template-columns:58px 1fr}.right{grid-column:1/-1;flex-direction:row;align-items:center;justify-content:space-between;min-width:0}}
</style></head>
<body>
<header>
 <div class="h-top">
  <h1>AI Events Calendar</h1>
  <span class="sub">Applied AI · Jul 2026 – Jun 2027 · reputation-scored</span>
  <div class="stats"><span><b id="s-shown">0</b> shown</span><span><b id="s-going" style="color:var(--going)">0</b> going</span><span><b id="s-maybe" style="color:var(--maybe)">0</b> maybe</span></div>
 </div>
 <div class="controls">
  <input id="q" type="search" placeholder="Search name, city, organizer…">
  <div class="seg" id="view"><button data-v="all" class="on">All</button><button data-v="going">My plan</button><button data-v="maybe">Maybe</button><button data-v="unmarked">Unmarked</button></div>
  <div class="rng">Min reputation <input id="rep" type="range" min="0" max="97" value="0"><span id="repv">0</span></div>
  <button class="btn" id="ics">⬇ Export my plan (.ics)</button>
  <button class="btn" id="reset">Reset marks</button>
 </div>
 <div class="chips" id="f-cat"></div>
 <div class="chips" id="f-region"></div>
 <div class="chips" id="f-rel"></div>
</div>
</header>
<main id="list"></main>
<footer>Built by an agent swarm: each event reputation-scored (0–100) from prior editions, attendance & real social/press footprint. Dates marked <span class="unconf">est</span> are projected (official dates not yet published). Your going/maybe/skip marks are saved in this browser only. Verify details on the official site before booking.</footer>
<script>
const EVENTS = __DATA__;
const CATS=[...new Set(EVENTS.map(e=>e.cat))].sort();
const REGIONS=[...new Set(EVENTS.map(e=>e.region))].sort();
const RELS=["Must","Worth","Optional"];
const CAT_COLOR={"AI Engineering":"#2563eb","Agents & MCP":"#7c3aed","AI Products & Consumer":"#0891b2","Enterprise & B2B AI":"#0f766e","Vendor Dev Day":"#4f46e5","Flagship Tech":"#b45309","AI Marketing & Creative":"#be185d","Hackathon":"#15803d"};
const REL_COLOR={"Must":"#16a34a","Worth":"#2563eb","Optional":"#a16207"};
const KEY="aical_status_v1";
let STATUS=JSON.parse(localStorage.getItem(KEY)||"{}");
const sel={cat:new Set(),region:new Set(),rel:new Set(),view:"all",rep:0,q:""};

function save(){localStorage.setItem(KEY,JSON.stringify(STATUS))}
function repColor(r){if(r>=88)return"#16a34a";if(r>=78)return"#65a30d";if(r>=68)return"#ca8a04";if(r>=58)return"#d97706";return"#9aa3b2"}
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
function mkChips(box,vals,set){box.innerHTML="";vals.forEach(v=>{const c=document.createElement("span");c.className="chip";c.textContent=v;c.onclick=()=>{set.has(v)?set.delete(v):set.add(v);c.classList.toggle("on");render()};box.appendChild(c)})}
mkChips(document.getElementById("f-cat"),CATS,sel.cat);
mkChips(document.getElementById("f-region"),REGIONS,sel.region);
mkChips(document.getElementById("f-rel"),RELS,sel.rel);

document.getElementById("q").oninput=e=>{sel.q=e.target.value.toLowerCase();render()};
document.getElementById("rep").oninput=e=>{sel.rep=+e.target.value;document.getElementById("repv").textContent=e.target.value;render()};
document.querySelectorAll("#view button").forEach(b=>b.onclick=()=>{sel.view=b.dataset.v;document.querySelectorAll("#view button").forEach(x=>x.classList.remove("on"));b.classList.add("on");render()});
document.getElementById("reset").onclick=()=>{if(confirm("Clear all your going/maybe/skip marks?")){STATUS={};save();render()}};
document.getElementById("ics").onclick=exportICS;

function monthLabel(ds){const[y,m]=ds.split("-");return new Date(y,m-1,1).toLocaleString("en",{month:"long"})+" "+y}
function setStatus(id,st){if(STATUS[id]===st)delete STATUS[id];else STATUS[id]=st;save();render()}

function passes(e){
 if(sel.rep && e.rep<sel.rep)return false;
 if(sel.cat.size && !sel.cat.has(e.cat))return false;
 if(sel.region.size && !sel.region.has(e.region))return false;
 if(sel.rel.size && !sel.rel.has(e.rel))return false;
 if(sel.view!=="all"){const s=STATUS[e.id]||"";if(sel.view==="unmarked"&&s)return false;if(sel.view==="going"&&s!=="going")return false;if(sel.view==="maybe"&&s!=="maybe")return false}
 if(sel.q){const h=(e.name+" "+e.city+" "+e.country+" "+e.org+" "+e.cat).toLowerCase();if(!h.includes(sel.q))return false}
 return true;
}

function render(){
 const list=document.getElementById("list");list.innerHTML="";
 const shown=EVENTS.filter(passes);
 let lastM="";
 shown.forEach(e=>{
  const ml=monthLabel(e.ds);
  if(ml!==lastM){lastM=ml;const h=document.createElement("div");h.className="month";h.textContent=ml;list.appendChild(h)}
  const st=STATUS[e.id]||"";
  const dd=new Date(e.ds.split("-")[0],e.ds.split("-")[1]-1,e.ds.split("-")[2]);
  const card=document.createElement("div");card.className="card"+(st?" "+st:"");
  card.innerHTML=
   '<div class="date"><div class="d">'+dd.getDate()+'</div><div class="m">'+dd.toLocaleString("en",{month:"short"})+'</div></div>'+
   '<div class="mid"><h3>'+esc(e.name)+(e.conf?'':' <span class="unconf">est</span>')+'</h3>'+
   '<div class="meta">'+
     '<span class="badge-rel" style="background:'+REL_COLOR[e.rel]+'">'+e.rel+'</span>'+
     '<span class="tag" style="background:'+(CAT_COLOR[e.cat]||"#334")+'22;color:'+(CAT_COLOR[e.cat]||"#9ab")+';border:1px solid '+(CAT_COLOR[e.cat]||"#334")+'55">'+esc(e.cat)+'</span>'+
     '<span class="loc">📍 '+esc(e.city)+', '+esc(e.country)+'</span>'+
     '<span>'+esc(e.dd)+'</span>'+
     '<span>'+(e.fop==="Free"?'🟢 Free':(e.fop==="Mixed"?'🟡 '+esc(e.cost):'💲 '+esc(e.cost)))+'</span>'+
     '<a href="'+esc(e.url)+'" target="_blank" rel="noopener">site ↗</a>'+
   '</div>'+
   '<div class="note">'+esc(e.note)+'</div></div>'+
   '<div class="right">'+
     '<div class="rep" title="Reputation '+e.rep+'/100"><div class="repbar"><div class="repfill" style="width:'+e.rep+'%;background:'+repColor(e.rep)+'"></div></div><span class="repnum" style="color:'+repColor(e.rep)+'">'+e.rep+'</span></div>'+
     '<div class="status">'+
       '<button class="going'+(st==="going"?" on":"")+'" data-id="'+e.id+'" data-st="going">Going</button>'+
       '<button class="maybe'+(st==="maybe"?" on":"")+'" data-id="'+e.id+'" data-st="maybe">Maybe</button>'+
       '<button class="skip'+(st==="skip"?" on":"")+'" data-id="'+e.id+'" data-st="skip">Skip</button>'+
     '</div>'+
   '</div>';
  list.appendChild(card);
 });
 if(!shown.length)list.innerHTML='<div class="empty">No events match these filters.</div>';
 list.querySelectorAll(".status button").forEach(b=>b.onclick=()=>setStatus(b.dataset.id,b.dataset.st));
 document.getElementById("s-shown").textContent=shown.length;
 document.getElementById("s-going").textContent=Object.values(STATUS).filter(s=>s==="going").length;
 document.getElementById("s-maybe").textContent=Object.values(STATUS).filter(s=>s==="maybe").length;
}

function exportICS(){
 const going=EVENTS.filter(e=>STATUS[e.id]==="going");
 if(!going.length){alert("Mark some events as 'Going' first.");return}
 const pad=n=>String(n).padStart(2,"0");
 const fmt=s=>{const[y,m,d]=s.split("-");return y+pad(m)+pad(d)};
 const plus1=s=>{const[y,m,d]=s.split("-").map(Number);const dt=new Date(y,m-1,d+1);return dt.getFullYear()+pad(dt.getMonth()+1)+pad(dt.getDate())};
 let out=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//AI Events Calendar//EN","CALSCALE:GREGORIAN"];
 going.forEach(e=>{out.push("BEGIN:VEVENT","UID:"+e.id+"@ai-calendar","DTSTART;VALUE=DATE:"+fmt(e.ds),"DTEND;VALUE=DATE:"+plus1(e.de),"SUMMARY:"+e.name.replace(/[,;]/g,""),"LOCATION:"+(e.city+", "+e.country).replace(/[,;]/g," "),"URL:"+e.url,"DESCRIPTION:"+(e.cat+" | rep "+e.rep+"/100 | "+e.note).replace(/[,;]/g," "),"END:VEVENT")});
 out.push("END:VCALENDAR");
 const blob=new Blob([out.join("\\r\\n")],{type:"text/calendar"});
 const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="my-ai-events.ics";a.click();
}
render();
</script>
</body></html>"""

HTML = HTML.replace("__DATA__", DATA_JSON)
with open(os.path.join(OUTDIR, "index.html"), "w") as f:
    f.write(HTML)

print("events:", len(EVENTS))
print("wrote:", os.path.join(OUTDIR, "ai-events-data.json"))
print("wrote:", os.path.join(OUTDIR, "index.html"))
