# Realty Stack — Platform Extensions Roadmap

**Status:** Future vision (not v0.x). Captured 2026-05-17 for project memory.
**Author:** Holden Richardson
**Targeted ship:** v1.x+ once core skill bundle is established and demand justifies the integration work

---

## Vision

Realty Stack becomes the AI layer on top of a **complete realtor business operating system**. A realtor installs the bundle, connects their data sources (MLS via Repliers, CRM via FUB or other, own database via Supabase), and runs their entire business out of Cowork — drafting, comping, prospecting, building websites, managing pipeline, all in one workspace, all in their voice and brand.

The free Realty Stack bundle is the wedge. The paid Realty Brain SaaS becomes the always-on autonomous layer that watches everything continuously. Both consume the same connected data sources.

---

## Integration surfaces

### 1. Repliers (MLS data layer)

[Repliers](https://repliers.com) — Canadian-founded MLS-data-as-a-service. REST API for listing data across multiple US + Canadian MLSs, real-time updates via webhook, saved-searches with notification capability, IDX-compliant feeds, polygon / neighborhood search, agent / office data, market analytics. Founded ~2020, developer-friendly, used by a growing chunk of proptech that doesn't want to negotiate MLS-by-MLS data contracts.

**Connector model:** realtor brings their Repliers API key (BYO), skill stores it locally encrypted (or in Cowork project secrets), every skill that needs live listing data calls through a shared `repliers-client` MCP server bundled with Realty Stack.

**What this unlocks immediately:**
- `/cma` auto-pulls comparables from Repliers given a subject address (eliminates the manual "paste 5 comps" step entirely)
- `/saved-search-watcher` — realtor defines criteria, skill watches Repliers, surfaces matches with contact-fit reasoning (which lead would care about this)
- `/listing-research` — pull full listing detail for any address, including history, price changes, days-on-market
- `/comp-checker` — quick gut-check on price vs current active listings + recent sales in the area
- `/neighborhood-pulse` — current inventory, average DOM, average list-to-sale ratio for any zip / polygon
- Live data inside Tier 2 FUB skills (cross-reference contact's IDX activity with current listings that match)

### 2. CRM connectors (FUB first, others on demand)

Already in the kickoff doc as Tier 2. Repliers makes Tier 2 dramatically more valuable because contact data + listing data combine.

**FUB MCP server** (already designed in the kickoff doc) provides ~25 tools for contacts, action plans, custom fields, automations, smart lists, tags, etc.

**With Repliers + FUB together:**
- `/lead-recon` — cross-references contact's stated criteria + IDX activity + current MLS inventory + their last-touch history → produces "what to send this lead today" recommendation
- `/revival-campaign-launcher` — picks stale leads + finds matching new listings + drafts outreach in voice (voice-draft already there)
- `/listing-alert` — when a new listing matches a saved search, drafts the alert in the realtor's voice using the agent profile already captured
- `/showing-prep` — for an upcoming showing, pulls listing detail + contact history + recent comps in one briefing document

**Other CRMs:** same connector pattern. Add KW Command, BoomTown, kvCORE, Sierra Interactive, etc. as standalone MCP servers when demand surfaces. All consume the same internal skill interfaces.

### 3. Supabase (realtor's own database)

Realtor gets their own Supabase project (free tier covers most agents). Skill bundle includes a schema template + setup wizard. Supabase stores:
- Contact data (synced from CRM as source-of-truth backup)
- Lead history with full message + activity log
- Saved searches with notification preferences
- Showing history, feedback notes
- Website lead capture
- Agent's own analytics (conversion rates, cycle times, source ROI)

**Why Supabase specifically:**
- Free tier is generous (500MB DB, 1GB file storage, 2GB egress / month — enough for most solo agents)
- Realtor owns and controls their data (portable, exportable, never locked in)
- Real-time subscriptions enable pushed notifications (saved-search hits)
- Built-in auth handles realtor-website login if they want client portals
- BYO key model — same security pattern as Repliers and FUB

**What this unlocks:**
- Cross-skill state: voice-draft's profile, brand-kit's assets, every CMA produced, every follow-up sent — all queryable in one place by other skills
- Persistent saved-search history for the realtor's own pipeline tracking
- Foundation for Realty Brain's continuous-monitoring capabilities (Brain reads from the same Supabase the bundle writes to)
- Multi-device sync (the per-device limitation of v0.0.x voice profile + brand kit can be addressed by syncing through their own Supabase — way better than the SaaS-only sync we deferred to Realty Brain)

### 4. Realtor website builder

`/website-build` — templates a full IDX-enabled realtor website, brand-kit-styled, deployed to Cloudflare Workers or Pages. Mirrors what Holden already does for [holdengr.com](https://holdengr.com).

**Components:**
- Brand-kit applied to the entire site (colors, typography, wordmark, headshot)
- IDX feed via Repliers (search, listings, detail pages)
- Lead capture forms wired to the realtor's Supabase + Resend (or other transactional email)
- AEO + SEO infrastructure baked in (per the 6333 Blackmar marketing-pillar pattern)
- Optional: per-property landing pages (auto-generated for each active listing)
- Optional: market-pulse tool (per Holden's existing holdengr.com/market-pulse)

**Deploy targets:** Cloudflare Workers / Pages as default (cheap, fast, edge-deployed). Vercel as alternative. Skill produces the codebase + deployment instructions; realtor owns the domain.

### 5. IDX iframe embed generator

For realtors who already have a website (Squarespace, WordPress, Wix, etc.) but want IDX functionality without rebuilding, `/idx-embed-build` produces:
- An iframe-embeddable IDX widget powered by Repliers
- Customizable to the brand kit
- Drop-in code the realtor pastes into any host site
- Optional: lead capture wired to their Supabase

This is the lighter-touch alternative to `/website-build` — keep your existing site, add IDX.

---

## Dependency ordering

Build in this order when we get to v1.x:

1. **Repliers connector first** — unlocks `/cma` auto-comp-pull immediately (highest-frequency leverage), foundation for everything else
2. **Supabase setup wizard + schema template** — establishes the shared state layer
3. **FUB MCP server** — already designed in the kickoff doc; activate with Tier 2 skills
4. **Tier 2 skills** — `/lead-recon`, `/revival-campaign-launcher`, `/listing-alert`, `/showing-prep`, etc.
5. **Realtor website builder** — `/website-build` (big project — possibly its own dependent skill cycle)
6. **IDX embed builder** — `/idx-embed-build` (lighter complement to #5)
7. **Other CRM connectors** — based on demand (KW Command, BoomTown, etc.)

---

## Architectural principles for the extensions

- **BYO credentials.** All third-party integrations use realtor's own API keys / accounts. We never see their data, never store credentials server-side. Same pattern as Tier 2 FUB design in the kickoff doc.
- **MCP servers for stateful connectors.** Repliers, FUB, Supabase each get their own bundled MCP server (or community-maintained one we reference). Skills call the MCPs; the MCPs hold credentials and abstract the API.
- **Per-device storage for free tier; Supabase for power-tier sync.** v0.0.x voice profile + brand kit ship per-device because we don't have central infrastructure. Once a realtor adds Supabase, those profiles can move there for cross-device sync — without requiring Realty Brain subscription. (Realty Brain becomes auto-everything + continuous monitoring; Supabase-backed bundle is sync + on-demand workflows.)
- **No silent service dependencies.** Every external service the bundle uses is opt-in, documented, and the realtor controls the connection. Skills work degraded (or refuse with a clear message) when a service isn't connected.

---

## Honest scope note

**This roadmap is not v0.x.** v0.0.x ships the foundational skill bundle (voice profile, brand kit, voice-draft, follow-up-draft, meeting-distill, listing-description, CMA). v0.1.x extends with more Tier 1 skills and the first Tier 2 FUB integration. Platform extensions in this document land in v1.x+ when:

1. The free bundle has real usage and demand signal for these integrations
2. Realty Brain has shipped (the paid SaaS path is established)
3. Holden has bandwidth to commit to MCP server maintenance for Repliers / FUB / Supabase

The vision is real and load-bearing for the long-game thesis. Capturing it now so the project remembers and so design decisions in v0.x respect the trajectory.

---

## When to revisit

- Every quarter while v0.x is shipping — check if any v1.x integration becomes a credibility-pull (i.e., the bundle gets adopted by enough agents that not having Repliers-comp-auto-pull becomes a blocker)
- When Realty Brain ships — these extensions are key differentiators between the free bundle's value ceiling and Brain's continuous-monitoring superpower
- When a third party reaches out wanting to integrate (Repliers themselves, a CRM vendor, etc.) — partnership signal worth chasing
