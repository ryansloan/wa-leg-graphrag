# Case study: multi-hop — who can reach the opposition (post 1's "pushed further" example)

- **Run date:** 2026-07-11
- **Agent:** graph agent (claude-sonnet-5 via PydanticAI), with the exact-aggregation
  and verification tools
- **Provenance:** verbatim CLI session (`uv run leg`); the `[tools: ...]` block is the
  agent's actual tool-call trace
- **Audit:** all member-vote claims (verified in-run via `verify_claims`) and all seven
  sponsorship-connection claims check against `data/dataset.json`. Known residual
  errors, both in unverified claim classes: the bloc is **58** members, not 57 (one name
  dropped in transcription), and HB 2077's House tally is **55–42**, not 52–45.
- Note: this run constructed its own five-bill test set, so its bloc differs from the
  four-bill, 22-member bloc in `case-study-themes.md` — same method, different slice.

---

## Prompt

> I represent a coalition of small business owners concerned about regulatory and compliance burden. There's presumably a bloc of legislators who consistently opposed this session's major cost-increasing bills, but we can't get meetings with them directly. Who in the legislature is best positioned to reach that bloc for us, ie: members connected to them through shared bill sponsorships, ideally ones sympathetic to business concerns?

## Tool-call trace

```
[tools: survey_bills({"query": "small business regulatory compliance costs mandates fees", "k": 40}); survey_bills({"query": "minimum wage paid leave employer mandate business", "k": 40}); survey_bills({"query": "business tax increase B&O surcharge revenue", "k": 30}); survey_bills({"query": "unemployment insurance benefits striking workers cost employers", "k": 15}); survey_bills({"query": "sales tax on services expansion new tax base", "k": 15}); bill_info({"bill_id": "HB 2081"}); bill_info({"bill_id": "SB 5813"}); bill_info({"bill_id": "SB 5041"}); bill_info({"bill_id": "HB 2077"}); bill_vote_summary({"bill_id": "HB 2081"}); bill_vote_summary({"bill_id": "SB 5813"}); bill_vote_summary({"bill_id": "SB 5041"}); bill_vote_summary({"bill_id": "HB 2077"}); bill_vote_summary({"bill_id": "HB 2020"}); bill_vote_summary({"bill_id": "SB 5786"}); voting_bloc({"bill_ids": ["HB 2081","SB 5813","SB 5041","HB 2077","SB 5786"], "vote": "Nay", "motion_contains": "Final Passage"}); member_sponsorships({"member_name": "Adison Richards"}); member_sponsorships({"member_name": "Dave Paul"}); member_sponsorships({"member_name": "Clyde Shavers"}); member_sponsorships({"member_name": "Alicia Rule"}); member_sponsorships({"member_name": "Joe Timmons"}); member_sponsorships({"member_name": "Deborah Krishnadasan"}); bill_sponsors({"bill_id": "HB 1353"}); bill_sponsors({"bill_id": "HB 2420"}); bill_sponsors({"bill_id": "HB 1524"}); bill_sponsors({"bill_id": "SB 6136"}); bill_sponsors({"bill_id": "HB 2047"}); bill_sponsors({"bill_id": "HB 1553"}); bill_sponsors({"bill_id": "HB 1788"}); bill_sponsors({"bill_id": "HB 1902"}); bill_sponsors({"bill_id": "HB 2199"}); bill_sponsors({"bill_id": "HB 2445"}); bill_sponsors({"bill_id": "HB 2604"}); bill_sponsors({"bill_id": "HB 1273"}); bill_sponsors({"bill_id": "HB 2325"}); bill_sponsors({"bill_id": "HB 1102"}); bill_sponsors({"bill_id": "HB 2534"}); bill_sponsors({"bill_id": "HB 1287"}); bill_sponsors({"bill_id": "SB 6162"}); member_votes({"member_name": "Dave Paul", "motion_contains": "Final Passage"}); member_votes({"member_name": "Clyde Shavers", "motion_contains": "Final Passage"}); member_votes({"member_name": "Deborah Krishnadasan", "motion_contains": "Final Passage"}); verify_claims({"claims": [{"member_name":"Adison Richards","bill_id":"HB 2081","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Adison Richards","bill_id":"SB 5813","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Adison Richards","bill_id":"SB 5041","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Adison Richards","bill_id":"HB 2077","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Adison Richards","bill_id":"SB 5786","vote":"Nay","motion_contains":"Final Passage"}]})]
```

## Agent output (verbatim from here)

## Bottom line

Based on the roll-call and sponsorship data, the "bloc" you're describing is essentially **the entire Republican caucus in both chambers** (55+ members), and the best-documented connectors into that bloc are a handful of **Democrats who both vote with it on cost issues and co-sponsor legislation with several of its members** — most notably **Rep. Adison Richards (D-House)**.

## How I identified the bloc

I treated five bills this session as representative "major cost-increasing" measures for business, based on their subject matter and contentious final votes:

- **HB 2081** – B&O tax surcharge increases/new surcharge on large companies (House 50-48, Senate 26-22)
- **SB 5813** – More progressive capital gains/estate tax rates (House 53-45, Senate 27-21)
- **SB 5041** – Unemployment insurance for striking/lockout workers (a direct new cost on employers) (House 51-45, Senate 27-21)
- **HB 2077** – New tax on business activity tied to the ZEV program (House 52-45, Senate 28-19)
- **SB 5786** – Increases to license, permit, and endorsement fees (House 51-47, Senate 25-23)

Running `voting_bloc` across these five Final Passage votes, **57 legislators voted Nay on all five** — nearly the full GOP caucus in both chambers (e.g., John Braun, Chris Corry, Drew Stokesbary, Jim Walsh, Mark Schoesler, Judy Warnick, and others), plus **one Democrat: Adison Richards (D-House)**. A further six Democrats — **Dave Paul, Clyde Shavers, Alicia Rule, Deborah Krishnadasan (D-Senate), Joe Timmons, and Chris Gildon (R-Senate, near-miss)** — opposed 4 of the 5.

## Who can best reach that bloc

Using `bill_sponsors`/`member_sponsorships` to find shared-sponsorship ties into the bloc:

**1. Adison Richards (D-House)** — strongest candidate. He's the only Democrat who matched the bloc on all five votes (confirmed via roll call), and he has *direct, repeated bipartisan co-sponsorships* with bloc Republicans:
- **HB 1553** (primary) — cosponsored with **Tom Dent (R)**
- **HB 1902** (primary) — cosponsored with **Tom Dent (R), David Stuebe (R), and Andrew Barkis (R)**
- **HB 2604** (primary) — cosponsored with **Andrew Barkis (R)**

*Inference: as a sitting Democrat who already works across the aisle with Dent, Stuebe, and Barkis and votes with the bloc on cost questions, he's plausibly better positioned than an outside advocate to get a hearing with those members and, through them, the wider caucus.*

**2. Dave Paul (D-House)** — matched the bloc on 4 of 5 votes; co-sponsors with bloc Republicans **Carolyn Eslick** (HB 1273) and **Mike Steele / Andrew Barkis** (HB 2325).

**3. Clyde Shavers (D-House)** — matched the bloc on 4 of 5; co-sponsors with bloc Republicans **Joel McEntire** and **Stephanie Barnard** (HB 2534).

**4. Deborah Krishnadasan (D-Senate)** — matched the bloc on 4 of 5, and is notable because she's a **Senate** Democrat (the others above are House), giving reach into the Senate GOP side; she co-sponsors **SB 6162** with **Leonard Christian (R-Senate)**, a bloc member.

**On the Republican side**, note that **Andrew Barkis (R-House)** shows up repeatedly as the GOP cosponsor on bipartisan bills with both Richards and Paul — *inference: he may function as a relatively cross-aisle-accessible node within the bloc itself*, worth treating as a first point of contact if you want to start from the Republican side rather than through a Democratic intermediary.

## Caveats

- This is built from **sponsorship and roll-call data only**. Whether any of these members are personally "sympathetic to business concerns" beyond these five votes, and things like committee assignments, leadership positions, or personal relationships, are **background knowledge my tools can't confirm — verify independently** before approaching them.
- "Connected through shared sponsorship" here means they co-sponsored specific bills together (HB 1553, HB 1902, HB 2604, HB 1273, HB 2325, HB 2534, SB 6162) — I haven't reviewed those bills' content/intent, only that the sponsor lists overlap.
- The 4-of-5 members' one dissenting vote wasn't isolated in my query; if you want a precise picture of which bill each broke on, I can pull that separately.
