# 11 Decisions

A short log, so nobody has to argue the same point twice.

- To change a decision, add a new row. Never edit an old one.
- "Proposed" means: the plan says so, and the team has not confirmed it yet.
- "Open" means the team still has to settle it.

| ID | Decision | Why | Status |
|---|---|---|---|
| D-01 | EU first. UK and US only as extras. | An EU regulation applies in all 27 countries at once, so "27 countries" would be a trick. The honest unit is the authority that issues the duties. | proposed |
| D-02 | Acts come from the EU's catalogue (Cellar), never from scraping the EUR-Lex website. | EUR-Lex blocks scripts; Cellar answered in 0.3 s `[MEASURED 2026-11-13]`. | proposed |
| D-03 | We never claim "checked against TARIC". | No free structured feed in three attempts `[MEASURED 2026-11-13]`. | proposed |
| D-04 | Python reads tables and the model cross-checks them. Disagreements go to a person. | A naive reading of a grouped cell gives the wrong company the wrong rate `[MEASURED 2026-11-13]`. | proposed |
| D-05 | No number the user sees comes from free model text. | Trust. A wrong but fluent number is the worst output we could produce. | proposed |
| D-06 | The demo is a replay of stored runs, marked "replay", plus the newest act live. | Only about one act every second day arrives, so a purely live demo would often show nothing. | proposed |
| D-07 | One model provider and model for all reported numbers. | One declared setup makes the numbers comparable. | closed by D-24 |
| D-08 | Evaluation: 24 months of acts, 40 practice acts, a sealed exam of 25 acts split by case and run once. Nobody grades their own homework. | 12 months hold too few acts with company tables. | proposed |
| D-09 | One Postgres database for everything, including the model cache. | One path is simpler than three services. | proposed |
| D-10 | Docker Compose and Render. The daily run is a scheduled GitHub Actions job. | Free hosting has no free background workers `[VERIFY]`. | proposed |
| D-11 | Screens: reuse the prototype's HTML and JS by default. React only if the owner of lane C names what it costs and what is dropped for it. | The prototype is the finished, tested design. | **open**, lane C decides |
| D-12 | Real public acts, synthetic importers. No real customer data, ever. | Privacy, and nothing to leak. | proposed |
| D-13 | The screens are in English. | The cohort and the coaches work in English. | proposed |
| D-14 | The name is "Trade Defence Desk", without "EU". No EU emblem. | It must not look official. | agreed |
| D-15 | Model budget: free tiers, or a small shared budget with a hard cap. The exam runs on one team key. | Cost risk. | closed by D-25 |
| D-16 | PydanticAI, not LangChain or LangGraph. No RAG claim. | We only claim what the project really uses. | proposed |
| D-17 | Every lane owns one model piece that is a Must, with a test set labelled by someone else. | All three want hands-on model work. | agreed |
| D-18 | dbt, Prefect, DVC, Redis, Prometheus, Grafana and Evidently are not on the Must path. | The Must list was about 1.4 times what three people can do. | proposed |
| D-19 | The platform work (repo, Compose, checks, deploy) sits in lane A. The daily job sits in lane B. The exam answers never enter the automatic checks. | Decided on 2026-11-22. | agreed |
| D-20 | We cover anti-dumping and anti-subsidy measures. Safeguards, amendments, corrections, suspensions, undertakings and rates that are not a percentage are shown and sent to a person. No end date is ever computed. | These are the legal states that move money, and the ones we can get right in four weeks. | proposed |
| D-21 | We match the producer named on the invoice, with the invoice declaration, not only the supplier. | The rate follows the producer `[LAW 2026/2393, Art 1(2), 1(3)]`. | proposed |
| D-22 | The story is told through one invented importer, Bergmann Outdoor GmbH, and its head of customs, Thomas. | One company makes every slide and every example concrete. Decided 2026-11-23. | agreed |
| D-23 | The replay runs at a pace we set for the presentation. Not "about a minute". | Decided 2026-11-23. | agreed |
| D-24 | Closes D-07. Every reported number uses `openai/gpt-oss-120b` on Groq, reasoning effort "low", temperature 0, through PydanticAI. The second model for C-16 is `ministral-14b-latest` on Mistral. | On three real acts it got every company row and both grouped cells right, 19 of 20 quotes were found in the act, about 2 seconds per act `[MEASURED 2026-11-24]`. See [07_TECH_STACK.md](07_TECH_STACK.md). | agreed |
| D-25 | Closes D-15. Free tiers during development, each person with their own key. The exam runs once on one team key. A small paid budget only for the whole-act runs of A-13. | The part we send is about 1,000 tokens per act, far below the free limits `[MEASURED 2026-11-24]`. | proposed |

"Proposed" rows were put to the team at the kickoff on Mon 23 Nov. Once the team has
confirmed a row, change its status to "agreed" in a pull request.

## Open questions

### For the coaches

1. The exact dates, length and format of the final presentation.
2. The grading rubric: individual parts, or team only?
3. Are some tools required?
4. The rules on AI coding assistants for the capstone.
5. Is there a model budget or a course key for capstone teams?

### For a real customs person (issue X-07)

1. What matters most: euros on purchase lines, or the days of warning?
2. How do you hear about new acts today, and how late?
3. Would you act on a name match that a person confirmed in a tool, if there is a log?

## Later

Ideas the scope guard parked. Add the date and who asked.

| Date | Idea | Asked by |
|---|---|---|
| | | |
