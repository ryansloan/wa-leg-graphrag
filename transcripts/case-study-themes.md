# Case study: themes across bills (post 1's worked example)

- **Run date:** 2026-07-10
- **Agent:** graph agent (claude-sonnet-5 via PydanticAI), with the exact-aggregation
  and verification tools (`survey_bills`, `voting_bloc`, `party_crossovers`, `verify_claims`)
- **Provenance:** verbatim CLI session (`uv run leg`); the `[tools: ...]` block is the
  agent's actual tool-call trace
- **Audit:** every member-vote, bloc, crossover, and sponsor claim in this response was
  independently verified against `data/dataset.json`. Known residual errors, all outside
  the verified claim classes: three near-unanimous relief-bill tallies are slightly off
  (SB 5611 was 96–0/48–0, HB 2418 93–0, HB 2309 97–0/48–0), and the 22-member bloc list
  omits one member (Phil Fortunato) that the tool returned.

---

## Prompt

> I represent a coalition of small business owners concerned about growing regulatory and compliance burden. Which WA legislators should we prioritize for outreach? Focus on themes across bills rather than any single bill.

## Tool-call trace

```
[tools: survey_bills({"query": "small business regulatory compliance burden", "k": 40}); survey_bills({"query": "reducing regulations and permitting requirements for businesses", "k": 40}); survey_bills({"query": "new mandates on employers paid leave minimum wage overtime", "k": 30}); survey_bills({"query": "business tax increase B&O tax surcharge fees", "k": 30}); survey_bills({"query": "small business exemption from regulation relief", "k": 30}); bill_info({"bill_id": "HB 2081"}); bill_sponsors({"bill_id": "HB 2081"}); bill_info({"bill_id": "SB 5786"}); bill_sponsors({"bill_id": "SB 5786"}); bill_sponsors({"bill_id": "HB 2575"}); bill_sponsors({"bill_id": "SB 5611"}); bill_sponsors({"bill_id": "HB 2418"}); bill_sponsors({"bill_id": "HB 2309"}); bill_sponsors({"bill_id": "HB 1524"}); bill_sponsors({"bill_id": "SB 5525"}); bill_vote_summary({"bill_id": "HB 2081"}); bill_vote_summary({"bill_id": "SB 5786"}); bill_vote_summary({"bill_id": "HB 1524"}); bill_vote_summary({"bill_id": "SB 5525"}); bill_vote_summary({"bill_id": "HB 2575"}); bill_vote_summary({"bill_id": "SB 5611"}); bill_vote_summary({"bill_id": "HB 2418"}); bill_vote_summary({"bill_id": "HB 2309"}); party_crossovers({"bill_ids": ["HB 2081","SB 5786","SB 5525","HB 1524"], "motion_contains": "Final Passage"}); voting_bloc({"bill_ids": ["HB 2081","SB 5786","SB 5525","HB 1524"], "motion_contains": "Final Passage", "vote": "Nay"}); verify_claims({"claims": [{"member_name":"Edwin Obras","bill_id":"HB 2081","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Adison Richards","bill_id":"SB 5786","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Mari Leavitt","bill_id":"SB 5786","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Vandana Slatter","bill_id":"HB 2081","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Chris Corry","bill_id":"HB 2081","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Claudia Kauffman","bill_id":"SB 5786","vote":"Nay","motion_contains":"Final Passage"},{"member_name":"Curtis King","bill_id":"HB 1524","vote":"Yea","motion_contains":"Final Passage"}]})]
```

## Agent output (verbatim from here)

## Where the regulatory-burden fight actually shows up

Scanning the 2025-26 bill landscape, "regulatory/compliance burden" splits into two distinct clusters your coalition should treat differently:

**A. Cost/mandate-increasing bills** — these had real, contested floor votes (party-line or near party-line):
- **HB 2081** – B&O tax surcharge on large companies + rate/surcharge changes (House 50-48, Senate 26-22 final passage)
- **SB 5786** – Across-the-board license/permit/endorsement fee increases (Senate 25-23/24, House 51-47)
- **SB 5525** – New mass-layoff/business-closure benefit requirements (House 59-38, Senate 30-19)
- **HB 1524** – New workplace-standards duties for employers of "isolated employees" (House 86-10, Senate 37-12)

**B. Deregulatory/streamlining bills** — these passed near-unanimously (HB 2575 reducing environmental/energy reporting obligations 95-0/47-0; SB 5611 streamlining local permitting 96-2/48-1; HB 2418 permit review process 93-5/49-0; HB 2309 cutting unnecessary state-employment degree requirements 97-1/48-1). There's essentially no organized opposition to *relief* bills — the fight is entirely on the cost/mandate side.

## Legislators to prioritize

**1. Champions already sponsoring regulatory-relief bills (worth recruiting as allies/messengers):**
- Rep. Zach Hall (D) – primary sponsor, HB 2575 (reducing reporting obligations)
- Sen. Jesse Salomon (D) – primary sponsor, SB 5611 (streamlining permitting)
- Rep. Davina Duerr (D) – primary sponsor, HB 2418 (permit review streamlining)
- Rep. Mari Leavitt (D) with Reps. Skyler Rude (R) and Cyndy Jacobsen (R) – HB 2309, a genuinely bipartisan deregulation effort

**2. The reliable core opposition bloc** — members who voted Nay on *all four* cost/mandate bills tested (HB 2081, SB 5786, SB 5525, HB 1524), confirmed via cross-bill analysis:
House: Chris Corry, Ed Orcutt, Jeremie Dufault, Jim Walsh, Joe Schmick, Joshua Penner, Mark Klicker, Mary Dye, Matt Marshall, Tom Dent.
Senate: Drew MacEwen, Jeff Wilson, Jim McCune, Judy Warnick, Keith Wagoner, Leonard Christian, Mark Schoesler, Matt Boehnke, Nikki Torres, Perry Dozier, Shelly Short.
*Inference: this group's voting pattern suggests they are the most consistent legislative allies on cost-of-business issues; a broader "Nay on 3 of 4" list (e.g., Andrew Barkis, Drew Stokesbary, Skyler Rude, John Braun, Chris Gildon) is also worth cultivating.*

**3. Persuadable swing Democrats — probably your highest-value outreach targets**, since they are majority-caucus members who broke ranks on cost-increasing bills (confirmed via party-crossover analysis):
- House, crossed on **both** HB 2081 and SB 5786: Adison Richards, Dave Paul, Amy Walen, Alicia Rule, Joe Timmons, Clyde Shavers
- House, crossed on one: David Hackney, Edwin Obras, Osman Salahuddin (HB 2081); Dan Bronoske, Mari Leavitt (SB 5786)
- Senate: Vandana Slatter, Deborah Krishnadasan, Adrian Cortes (HB 2081); Claudia Kauffman, Mike Chapman, Liz Lovelett (SB 5786)
*Inference: repeated crossover on tax/fee bills suggests these legislators are genuinely persuadable on future cost-of-business legislation, unlike party-line colleagues — this is inferred from voting behavior, not a statement of their motives.*

**4. Active floor participants worth direct engagement** — members who introduced floor amendments to HB 2081 (the B&O surcharge), indicating hands-on involvement with the bill's mechanics: Reps. Dent, Abell, Caldier, Waters, Griffey, Manjarrez, Connors; Sens. Muzzall, Christian, MacEwen, Short, Wagoner, Warnick, Braun. *Note: the roll-call data only shows who authored each amendment and how members voted on it — not the amendment's substance or intent — so I can't characterize what these amendments would have done; if useful I can pull amendment numbers for your policy staff to review the text directly.*

**5. Bills' primary sponsors worth direct education/engagement** (not necessarily adversarial, but they are the authors of the burden-adding measures and control future iterations): Rep. Joe Fitzgibbon (D) – HB 2081; Sen. Derek Stanford (D) – SB 5786; Sen. Annette Cleveland (D) – SB 5525; Rep. Edwin Obras (D) – HB 1524 (notably, Obras also crossed over to vote Nay on HB 2081 himself).

### Caveats
- This is built from bills that reached recorded floor votes in the tool's dataset; it does not capture bills that died in committee, which may be equally relevant to "regulatory burden" themes.
- Committee assignments, leadership titles, and caucus dynamics (e.g., who chairs relevant committees) are background knowledge not available in this dataset — verify independently before assuming influence.
- All "reliable ally" and "persuadable swing vote" characterizations above are inferences from voting patterns across these specific bills, not confirmed statements of intent.