# Source registry

Immutable provenance for every raw source. One row per source. The `id` is cited inline
across the wiki. Raw captures (PDFs, screenshots, saved articles, pulled quotes) live
alongside this file in `sources/`. **Never edit a row's claims after capture — append a new
source instead.**

| id | source | title / finding | date | type | url | status |
|---|---|---|---|---|---|---|
| src-gartner-2025-automation | Gartner | Agentic AI will autonomously resolve ~80% of common customer-service issues without human intervention by 2029; ~30% reduction in operational costs | 2025-03 | analyst | https://www.gartner.com/en/newsroom/press-releases/2025-03-05-gartner-predicts-agentic-ai-will-autonomously-resolve-80-percent-of-common-customer-service-issues-without-human-intervention-by-20290 | verified |
| src-gartner-2026-cost | Gartner | GenAI cost per resolution will exceed $3 by 2030, higher than many B2C offshore human agents ("Predicts 2026: Generative AI Will Cost a Lot More Than You Think") | 2026-01 | analyst | https://www.gartner.com/en/newsroom/press-releases/2026-01-26-gartner-predicts-genai-cost-per-resolution-for-customer-service-will-exceed-offshore-human-agent-costs-by-2030 | verified |
| src-gartner-2022-labor | Gartner | Conversational AI will reduce contact-center agent labor costs by $80B in 2026; labor is up to 95% of contact-center cost; only ~1 in 10 interactions automated by 2026 | 2022-08 | analyst | https://www.gartner.com/en/newsroom/press-releases/2022-08-31-gartner-predicts-conversational-ai-will-reduce-contac | verified |
| src-gartner-2024-selfservice | Gartner | Only ~14% of customer-service issues fully resolve in self-service (survey of 5,728 customers, Dec 2023); even "very simple" issues only 36% | 2024-08 | analyst | https://www.gartner.com/en/newsroom/press-releases/2024-08-19-gartner-survey-finds-only-14-percent-of-customer-service-issues-are-fully-resolved-in-self-service | verified |
| src-gartner-2024-costbenchmarks | Gartner | Median cost per contact: $1.84 self-service vs $13.50 assisted (phone/chat/email similar) — "Benchmarks to Assess Your Customer Service Costs" | 2024-02 | analyst | https://www.gartner.com/en/documents/5164231 | verified |
| src-gartner-2025-cancellations | Gartner | Over 40% of agentic-AI projects will be cancelled by end of 2027 (escalating costs, unclear value, inadequate risk controls) | 2025-06 | analyst | _pending_ | seeded |
| src-mck-2023-genai | McKinsey | Gen AI can cut human-serviced contacts up to 50%; customer-care productivity uplift 30–45% (where ~50% of activity is automatable) | 2023-06 | consulting | https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier | verified |
| src-mck-2025-transactional | McKinsey | Across 30+ organizations, 50–60% of customer interactions remain transactional despite efforts to eliminate them | 2025-03 | consulting | https://www.mckinsey.com/capabilities/operations/our-insights/the-contact-center-crossroads-finding-the-right-mix-of-humans-and-ai | verified |
| src-mck-2024-qa | McKinsey | Gen AI in QA: >50% QA cost savings, 25–30% agent-efficiency gain, 5–10% CSAT improvement | 2024-07 | consulting | https://www.mckinsey.com/capabilities/operations/our-insights/operations-blog/ai-mastery-in-customer-care-raising-the-bar-for-quality-assurance | verified |
| src-mck-callcost | McKinsey (disputed) | "~$7.16 average cost per inbound call" — commonly attributed to McKinsey but appears to originate with ContactBabel; superseded as the benchmark anchor by src-gartner-2024-costbenchmarks | unknown | consulting | _pending_ | superseded |
| src-contactbabel-callcost | ContactBabel | $7.16 average cost per inbound call (2025 US Contact Center Decision-Makers' Guide) — the likely true source of the "$7.16" figure; not a sanctioned benchmark firm, not used | 2025 | industry | _pending_ | seeded |
| src-forrester-tei | Forrester | TEI composites for conversational-AI customer service: ROI ~210–391%, NPV up to ~$19.9M, payback ~6–12 months (e.g. boost.ai 293%/$19.9M; PolyAI 391%/$11.3M; Sprinklr 210%) | 2024 | analyst | https://boost.ai/guides/forrester-report-the-total-economic-impact-of-boost-ai/ | verified |

**Status legend:** `seeded` = imported, source URL not yet verified. `verified` = primary
source located and figure confirmed. `contested` = the claim or its attribution could not be
confirmed (see the page body). `superseded` = a newer source replaced it (kept for history).

> **Verification pass 2026-06-25:** primary sources located for the four Gartner claims and
> three of the four McKinsey claims; Forrester composites tied to published vendor TEI
> studies. Two items need attention: (1) the **$7.16 per-call** figure is widely cited as
> McKinsey but traces to **ContactBabel**, which is *not* a sanctioned benchmark firm
> (Gartner/McKinsey/Forrester) — flagged `contested`; (2) the **40%-cancellation** Gartner
> caveat was newly discovered and entered `seeded` pending its press-release URL.
>
> **Follow-up 2026-06-25:** found a sanctioned replacement for the cost-per-contact anchor —
> Gartner's Feb-2024 cost benchmarks (`src-gartner-2024-costbenchmarks`): **$13.50 median per
> assisted contact**, **$1.84 self-service**. The `$7.16/McKinsey` row is now `superseded`.
> The value model's conservative per-channel defaults ($6 voice / $4 chat) sit *below*
> Gartner's $13.50 assisted median, so they remain defensible.
