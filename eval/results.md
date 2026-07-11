# Eval results — flat-vector control vs HelixDB graph+vector

Auto-scored by required-substring check; see per-question transcripts below.

| id | bucket | question | control | graph |
|----|--------|----------|:-------:|:-----:|
| S1 | semantic | Which bills passed this biennium deal with unemployment insurance? | ✅ | ✅ |
| S2 | semantic | What legislation addresses protections or housing stability for residential tena… | ✅ | ✅ |
| S3 | semantic | Which bills concern artificial intelligence? | ✅ | ✅ |
| S4 | semantic | Is there legislation about student cell phone or mobile device use in schools? | ✅ | ✅ |
| R1 | relational | Which Democratic senators voted Nay on the Senate 3rd Reading & Final Passage of… | ❌ | ✅ |
| R2 | relational | Which cosponsors of SB 5041 voted against it on final passage? | ❌ | ✅ |
| R3 | relational | Which Democrats voted Nay on the House final passage of HB 2049, the K-12 educat… | ❌ | ✅ |
| R4 | relational | Did any sponsor of HB 1620 (parenting plan limitations) vote against it on final… | ❌ | ✅ |
| H1 | hybrid | Find the major bill about residential rent stabilization and report how close it… | ❌ | ✅ |
| H2 | hybrid | Among bills about the capital gains tax, did any Republican cosponsor one and th… | ❌ | ✅ |
| H3 | hybrid | Which bills about artificial intelligence had contested (non-unanimous) final pa… | ❌ | ✅ |
| H4 | hybrid | Find the bill about allowing alcohol service in public places and list the Democ… | ❌ | ✅ |

---

## S1 (semantic)

**Q:** Which bills passed this biennium deal with unemployment insurance?

**Expected:** HB 2264 (unemployment insurance/layoffs), SB 5041 (unemployment insurance for strikes & lockouts), SB 5874 (unemployment info reporting), SB 6134 (striking workers/UI overpayments). Any three of the four is a pass.

### control — pass

tools: search_bills

> Based on the tool results, several bills that passed this biennium (each shows a "C ___ L 25/26" chapter-law status, indicating enactment) deal directly with unemployment insurance:
> 
> - **SB 5041** – Unemployment insurance benefits for striking or lockout workers (status: C 352 L 25)
> - **SB 6134** – Notice to striking workers applying for unemployment insurance benefits about potential overpayment assessment upon receipt of retroactive wages (status: C 161 L 26)
> - **HB 2264** – Unemployment insurance benefits for workers separated due to employer-initiated layoffs or workforce reductions (status: C 150 L 26)
> - **SB 5874** – Employers' information reporting requirements for unemployment compensation purposes (status: C 43 L 26)
> 
> Two related but more tangential bills also appeared in the search — **SB 6106** (laid-off employees notification act) and **SB 5525** (business closures/mass layoffs protections) — these concern worker layoff notifications rather than unemployment insurance benefits directly, so I'd flag them as adjacent topics rather than core UI bills.
> 
> If you'd like, I can pull the specific final-passage vote counts and sponsors for any of these bills.

### graph — pass

tools: search_bills_semantic

> Based on the semantic search of bill digests, the following bills that passed this biennium directly concern unemployment insurance (all have "C ... L 25/26" status, indicating they were enacted into law):
> 
> 1. **SB 5041** — "Concerning unemployment insurance benefits for striking or lockout workers." (Chapter 352, Laws of 2025)
> 2. **SB 6134** — "Concerning notice to striking workers applying for unemployment insurance benefits of potential overpayment assessment upon receipt of retroactive wages." (Chapter 161, Laws of 2026)
> 3. **HB 2264** — "Concerning unemployment insurance benefits for workers separated from employment as a result of employer-initiated layoffs or workforce reductions." (Chapter 150, Laws of 2026)
> 4. **SB 5874** — "Concerning employers' information reporting for purposes of unemployment compensation." (Chapter 43, Laws of 2026)
> 
> A few related but adjacent bills also passed, touching on layoffs/notification rather than UI benefits specifically — I'd flag these as related but not core "unemployment insurance" bills:
> - **SB 6106** — modifies the "laid-off employees act" (WARN-type notification law), Chapter 86, Laws of 2026
> - **SB 5525** — "protecting workers facing employment loss due to businesses closing or mass layoffs," Chapter 277, Laws of 2025
> 
> If you'd like, I can pull sponsors and final-passage vote tallies for any of these bills.

## S2 (semantic)

**Q:** What legislation addresses protections or housing stability for residential tenants?

**Expected:** HB 1217 (residential tenants / rent stabilization); SB 5937 (smart access systems/tenants) is a bonus.

### control — pass

tools: search_bills, search_bills

> Several bills in the 2025-26 Washington biennium address tenant protections and housing stability:
> 
> **Core tenant protection / housing stability legislation:**
> 
> - **HB 1217** – "Improving housing stability for tenants subject to the residential landlord-tenant act and the manufactured/mobile home landlord-tenant act." This is the most directly on-point bill: it limits rent and fee increases, requires notice of rent/fee increases, limits fees and deposits, establishes a landlord resource center, authorizes tenant lease termination, creates parity between lease types, and provides for attorney general enforcement. Status: enacted (C 209 L 25).
> 
> **Related/adjacent bills:**
> 
> - **HB 2452** – Modifies requirements for service of rent increase notices. Status: C 118 L 26.
> - **SB 5298** – Concerns notice of sale or lease of manufactured/mobile home communities (protects residents of mobile home parks when the community changes hands). Status: C 205 L 25.
> - **SB 5937** – Concerns use of a "smart access system" (e.g., keyless/smart locks) in residential property subject to the residential landlord-tenant act. Status: C 55 L 26.
> - **HB 1003** – Addresses service of notice by mail in forcible entry/detainer (eviction) cases, a procedural protection in eviction proceedings. Status: C 44 L 25.
> - **HB 1621** – Authorizes superior courts to appoint housing court commissioners to address court capacity for unlawful detainer (eviction) actions — relevant to how quickly/fairly eviction cases move through courts. Status: C 268 L 25.
> 
> **Not primarily tenant-protection but touching housing supply/affordability** (surfaced by search but more tangential): HB 1494 (property tax exemption for multi-unit housing), HB 1757 (regulations for existing residential buildings), HB 2266 (permanent supportive/transitional/emergency housing), HB 1096 (lot splitting for housing options), HB 1403/HB 2304 (condominium construction/warranty statutes).
> 
> If you want, I can pull the specific "Final Passage" roll-call votes and sponsor information for HB 1217 (the flagship tenant-stability bill) or any of the others — just let me know which bill(s) to drill into.

### graph — pass

tools: search_bills_semantic, search_bills_semantic, search_bills_semantic

> Based on my search of the bill database, several pieces of 2025-26 Washington legislation address tenant protections and housing stability:
> 
> **Most directly on-point:**
> 
> - **HB 1217** – *"Improving housing stability for tenants subject to the residential landlord-tenant act and the manufactured/mobile home landlord-tenant act."* This is the centerpiece bill: it limits rent and fee increases, requires notice of rent/fee increases, limits fees and deposits, establishes a landlord resource center, authorizes tenant lease termination in certain circumstances, creates parity between lease types, and provides for attorney general enforcement. Status: Chapter 209, Laws of 2025 (enacted).
> 
> **Related, narrower tenant/landlord-tenant-act bills:**
> 
> - **SB 5937** – Concerning use of "smart access systems" (e.g., keyless/electronic entry) in residential rental properties. Status: Chapter 55, Laws of 2026.
> - **HB 2452** – Modifies requirements for service of rent increase notices. Status: Chapter 118, Laws of 2026.
> - **SB 5298** – Concerns notice requirements for sale or lease of manufactured/mobile home communities (protects manufactured-home tenants facing park sales). Status: Chapter 205, Laws of 2025.
> - **HB 1003** – Addresses service of notice by mail in forcible entry/unlawful detainer (eviction) cases. Status: Chapter 44, Laws of 2025.
> - **SB 6237** – Requires rental property disclosures of flooding history and flood risk. Status: Chapter 234, Laws of 2026.
> 
> **Adjacent housing-stability measures (not landlord-tenant law per se, but related to housing stability):**
> 
> - **HB 2266** – Encourages permanent supportive housing, transitional housing, and emergency shelters. Status: Chapter 232, Laws of 2026.
> - **HB 1494** – Property tax exemption for new/rehabilitated multi-unit dwellings in urban centers. Status: Chapter 164, Laws of 2025.
> - **SB 5938** – Concerns a "foreclosure prevention fee" (homeownership stability, not rental tenancy). Status: Chapter 156, Laws of 2026.
> 
> If you'd like, I can pull sponsor lists and floor (Final Passage) vote breakdowns for any of these — HB 1217 in particular, since it's the primary tenant-protection bill — to show which legislators supported or opposed it.

## S3 (semantic)

**Q:** Which bills concern artificial intelligence?

**Expected:** HB 1170 (AI content notices) and HB 2225 (AI companion chatbots).

### control — pass

tools: search_bills, search_bills, search_bills

> Based on my searches, two bills in the dataset directly and substantively concern artificial intelligence:
> 
> 1. **HB 1170** — "Relating to informing users when content is developed or modified by artificial intelligence." Requires disclosure when content is AI-generated or AI-modified. Status: C 167 L 26 (signed into law).
> 
> 2. **HB 2225** — "Relating to regulation of artificial intelligence companion chatbots." Regulates AI companion chatbots. Status: C 168 L 26 (signed into law).
> 
> Other results returned by my searches (e.g., SB 6002 on automated license plate readers, SB 5937 on smart access systems, SCR 8401 on joint rules) mention automation or technology but are not substantively about artificial intelligence — I'm excluding them as not on-topic.
> 
> If you'd like, I can pull the sponsor lists and roll-call vote details (including any Final Passage votes) for HB 1170 and HB 2225.

### graph — pass

tools: search_bills_semantic, search_bills_semantic, search_bills_semantic

> Based on my search of the bill database, two bills clearly and specifically concern artificial intelligence:
> 
> 1. **HB 1170** — "Informing users when content is developed or modified by artificial intelligence." Status: Chaptered (C 167 L 26).
> 2. **HB 2225** — "Regulating artificial intelligence companion chatbots." Status: Chaptered (C 168 L 26).
> 
> I ran additional searches on related themes (automated decision systems, generative AI in schools) but did not find other bills that are substantively about AI — the other results returned were unrelated (e.g., driver privacy/license plate readers, radiologic technologist supervision, education efficiency bills) or only tangentially matched on keywords. If there are other AI-related bills in the dataset that didn't surface with these queries, I don't have a way to guarantee completeness beyond semantic search, so I'd recommend a follow-up search with different terms (e.g., "deepfake," "machine learning," "facial recognition") if you want broader coverage.

## S4 (semantic)

**Q:** Is there legislation about student cell phone or mobile device use in schools?

**Expected:** Yes — SB 5346 (student mobile device use).

### control — pass

tools: search_bills

> Yes — **SB 5346**, "AN ACT Relating to student use of mobile devices in public schools," directly addresses this topic. According to the digest, it concerns student use of mobile devices in public schools. Its status shows it was enacted as **Chapter 225, Laws of 2026 (C 225 L 26)**.
> 
> I don't have further details from my tools (e.g., sponsor names, specific provisions, or roll-call vote counts) on this bill. If you'd like, I can search for its floor vote/roll-call results specifically.

### graph — pass

tools: search_bills_semantic, bill_sponsors, bill_vote_summary

> ## SB 5346 — Student Use of Mobile Devices in Public Schools
> 
> **Summary:** "Addressing student use of mobile devices in public schools." (Full bill text/policy details beyond this digest aren't available in my tools — for specifics on what the law actually requires, e.g. bans, exceptions, or district policy mandates, you'd want to check the enrolled bill text directly.)
> 
> **Status:** Chaptered as **Chapter 225, Laws of 2026** — the bill passed and was signed into law.
> 
> **Primary sponsor:** Sen. Marko Liias (D)
> **Cosponsors:** Paul Harris (R), Sharon Shewmake (D), Perry Dozier (R), Jessica Bateman (D), Leonard Christian (R), Noel Frame (D), Bob Hasegawa (D), Curtis King (R), Deborah Krishnadasan (D), John Lovick (D), T'wina Nobles (D), Jesse Salomon (D) — a bipartisan cosponsor list.
> 
> **Decisive votes (Final Passage):**
> - **Senate**, original 3rd Reading & Final Passage (2026-02-11): Yea 37 – Nay 12
> - **House**, Final Passage as Amended by the House (2026-03-04): Yea 63 – Nay 34, Excused 1
> - **Senate**, Final Passage as Amended by the House (concurrence, 2026-03-09): Yea 43 – Nay 4, Excused 2
> 
> The bill passed the Senate first, was amended in the House, passed there, then went back to the Senate for concurrence on the House amendment, which passed by a wide margin (43-4). This pattern — strong Senate support both times, more contested in the House — is consistent with the bill picking up broader bipartisan support after the House amendment, though I can't say from vote data alone what that amendment changed (inference, not confirmed by amendment text).
> 
> Let me know if you'd like the individual roll-call breakdown by member/party for any of these votes.

## R1 (relational)

**Q:** Which Democratic senators voted Nay on the Senate 3rd Reading & Final Passage of SB 5041?

**Expected:** Lisa Wellman and Mike Chapman.

### control — FAIL

tools: search_bills

> My tool only provides bill digests, titles, and status — it does not return roll-call vote data (individual member votes, party breakdowns, or motion-level detail like "3rd Reading & Final Passage" tallies). I cannot retrieve which senators voted Yea or Nay on SB 5041, so I can't answer this question with the tools available.
> 
> If you have access to a roll-call vote lookup tool or dataset, that would be needed to answer this specific question accurately.

### graph — pass

tools: bill_votes

> On the Senate 3rd Reading & Final Passage vote for SB 5041, two Democratic senators voted Nay:
> 
> - **Mike Chapman (D-Senate)**
> - **Lisa Wellman (D-Senate)**
> 
> All other Nay votes on that motion came from Republican senators.

## R2 (relational)

**Q:** Which cosponsors of SB 5041 voted against it on final passage?

**Expected:** Lisa Wellman (cosponsored the bill, voted Nay on Senate final passage).

### control — FAIL

tools: search_bills

> I don't have tool access to cosponsor lists or roll-call vote data — my only tool searches bill digests (title, summary, status), which don't include sponsor names or individual member votes. I can confirm SB 5041 exists ("AN ACT Relating to unemployment insurance benefits for striking or lockout workers," enacted as C 352 L 25), but I cannot retrieve who cosponsored it or how any specific member voted on final passage.
> 
> To answer this accurately, you'd need a source with the bill's sponsor list and the roll-call record for its final passage vote — neither of which my current tools expose. I'd rather flag that gap than guess at member names or vote outcomes.

### graph — pass

tools: bill_sponsors, bill_votes

> Based on the roll call for SB 5041's final passage motions (3rd Reading & Final Passage, and Final Passage as Recommended by Conference Committee), one cosponsor voted against the bill:
> 
> - **Lisa Wellman (D-Senate)** — voted Nay on both final passage motions, despite being listed as a cosponsor.
> 
> All other cosponsors (Steve Conway, Bob Hasegawa, Rebecca Saldaña, Jesse Salomon, Derek Stanford, Manka Dhingra, T'wina Nobles, Yasmin Trudeau, Javier Valdez, Jessica Bateman, Liz Lovelett, Annette Cleveland, Noel Frame, Tina Orwall, Jamie Pedersen, Vandana Slatter, and Claire Wilson) voted Yea on final passage.
> 
> Note: This dataset lists no House cosponsors for SB 5041 (all cosponsors are Senate members), so the House final-passage votes on this bill aren't relevant to the cosponsor question.

## R3 (relational)

**Q:** Which Democrats voted Nay on the House final passage of HB 2049, the K-12 education funding bill?

**Expected:** Adam Bernbaum, Adison Richards, Alicia Rule, Clyde Shavers, Dave Paul, Joe Timmons, Mari Leavitt, Melanie Morgan, Shelley Kloba (9 members, House 3rd Reading & Final Passage).

### control — FAIL

tools: search_bills

> I found the bill itself, but my only tool is `search_bills`, which returns bill metadata (id, title, digest, status) — it does not provide roll-call vote data, sponsor lists, or individual member votes.
> 
> I cannot retrieve who voted Yea/Nay on HB 2049's House final passage, or identify any Democrats who voted Nay, because that data isn't accessible through the tools available to me. I don't have a way to pull roll-call records, so I won't guess at member names or vote counts.
> 
> If you have access to a roll-call/vote-data tool or dataset, that would be needed to answer this specific question accurately.

### graph — pass

tools: bill_info, bill_votes

> On the House final passage vote (3rd Reading & Final Passage) for HB 2049, the Democrats who voted Nay were:
> 
> - Adison Richards (D-House)
> - Shelley Kloba (D-House)
> - Dave Paul (D-House)
> - Mari Leavitt (D-House)
> - Melanie Morgan (D-House)
> - Alicia Rule (D-House)
> - Joe Timmons (D-House)
> - Clyde Shavers (D-House)
> - Adam Bernbaum (D-House)
> 
> All other Nay votes on this motion came from Republican members.

## R4 (relational)

**Q:** Did any sponsor of HB 1620 (parenting plan limitations) vote against it on final passage? Who?

**Expected:** Yes — cosponsors Roger Goodman and Natasha Hill voted Nay on House final passage.

### control — FAIL

tools: search_bills

> My tool only returns bill digest/status/title/score — it does not provide sponsor lists or roll-call vote data for HB 1620. I cannot retrieve sponsor names or the final passage vote breakdown from this dataset, so I can't confirm whether any sponsor voted against it on final passage.
> 
> If you have access to a roll-call or sponsor lookup source, that would be needed to answer this accurately. I don't want to guess member names or vote outcomes without tool support.

### graph — pass

tools: bill_info, bill_sponsors, bill_votes

> Looking at the roll calls for **HB 1620**, the sponsors are:
> 
> - Jamila Taylor (D) [primary]
> - Roger Goodman (D) [cosponsor]
> - Julia Reed (D) [cosponsor]
> - Natasha Hill (D) [cosponsor]
> 
> Two "Final Passage"-labeled House votes appear in the data: the initial House **"3rd Reading & Final Passage"** and, after Senate amendments, the House vote on **"Final Passage as Amended by the Senate"** (the vote that actually sent the bill to the Governor).
> 
> - **Jamila Taylor**: Yea on both.
> - **Julia Reed**: Yea on both.
> - **Roger Goodman**: **Nay** on the original House "3rd Reading & Final Passage," then **Yea** on "Final Passage as Amended by the Senate."
> - **Natasha Hill**: **Nay** on the original House "3rd Reading & Final Passage," then **Yea** on "Final Passage as Amended by the Senate."
> 
> So yes — two sponsors, **Roger Goodman** and **Natasha Hill**, voted against HB 1620 on its first House final-passage vote, but both switched to Yea on the later House vote concurring in the Senate's amended version, which was the vote that ultimately sent the bill to become law (C 166 L 25).
> 
> Inference: the flip from Nay to Yea between the two House votes suggests the Senate amendments addressed whatever concern led Goodman and Hill to vote no initially — but I can't confirm the amendment's content or their motive from this data; that would require reading the amendment text (background knowledge not available through these tools).

## H1 (hybrid)

**Q:** Find the major bill about residential rent stabilization and report how close its Senate final passage vote was.

**Expected:** HB 1217; Senate final passage was 29 Yea to 20 Nay.

### control — FAIL

tools: search_bills, search_bills

> The search tool only retrieves bill digests/titles/status, not roll-call vote data. I was able to identify the bill but cannot retrieve the actual Senate final passage vote tally through my available tools.
> 
> **What I can confirm:**
> 
> **HB 1217** is the major bill on residential rent stabilization — "AN ACT Relating to improving housing stability for tenants subject to the residential landlord-tenant act and the manufactured/mobile home landlord-tenant act by limiting rent and fee increases, requiring notice of rent and fee increases, limiting fees and deposits, establishing a landlord resource center and associated services, authorizing tenant lease termination, creating parity between lease types, and providing for attorney general enforcement." It was enacted (status: C 209 L 25).
> 
> **What I cannot confirm:**
> My search tool only returns bill digests, titles, and status — it does not expose roll-call vote data (yea/nay counts, member votes, or motion labels like "Final Passage"). I do not have a way to query vote tallies directly, so I cannot report how close the Senate final passage vote on HB 1217 was, or which senators voted which way.
> 
> If you have access to a separate roll-call/vote lookup tool or dataset, I'd need that to answer the "how close was the vote" question accurately. I don't want to guess a vote count or margin without grounding it in actual data.

### graph — pass

tools: search_bills_semantic, bill_vote_summary

> **HB 1217** — "AN ACT Relating to improving housing stability for tenants... by limiting rent and fee increases..." (the rent stabilization bill; became law as Ch. 209, L. 25) is the bill you're asking about.
> 
> **Senate final passage vote:**
> The bill passed the Senate twice on "Final Passage" motions, since it went through a conference committee:
> 
> 1. **3rd Reading & Final Passage as Amended by the Senate** (2025-04-10): **Yea 29 – Nay 20** — a 9-vote margin.
> 2. **Final Passage as Recommended by Conference Committee** (2025-04-27) — the decisive, final Senate vote that sent the bill to the Governor: **Yea 27 – Nay 20 – Excused 1** — a **7-vote margin** in a 48-member chamber.
> 
> So the bill's decisive Senate vote was fairly close for a chamber of 48: 27–20, with just a 7-vote cushion (well short of a supermajority, but enough for simple-majority passage). The margin actually narrowed slightly between the initial Senate passage (29-20) and the final conference-report vote (27-20), suggesting (inference, based on the vote-count shift) a couple of senators who'd backed the original Senate version did not support the conference committee's final version — though the specific individuals and reasons aren't available from vote summaries alone.

## H2 (hybrid)

**Q:** Among bills about the capital gains tax, did any Republican cosponsor one and then vote against it on final passage?

**Expected:** Yes — Paul Harris (R) cosponsored SB 5314 and voted Nay on its final passage.

### control — FAIL

tools: search_bills

> My tool only returns bill titles, digests, status, and a relevance score — it does not provide sponsor lists, cosponsor information, or roll-call vote data. I cannot retrieve which members cosponsored a bill or how they voted on final passage through this search interface.
> 
> Based on the search, the capital gains tax bills most relevant to your question appear to be:
> - **HB 1376** – prepayment of capital gains taxes
> - **SB 5314** – modifying the capital gains tax (loopholes, credits, technical corrections)
> - **SB 5813** – creating a more progressive rate structure for the capital gains tax and estate tax
> 
> However, I have no way to pull cosponsor lists or roll-call vote records for these bills with the tools available to me, so I cannot confirm or deny whether any Republican cosponsored one of these and then voted against it on final passage. I don't want to guess member names or vote outcomes, as that would risk stating unsupported claims.
> 
> If you have access to a tool or dataset that lists bill sponsors and individual roll-call votes, that would be needed to answer this specific question accurately.

### graph — pass

tools: search_bills_semantic, bill_sponsors, bill_sponsors, bill_sponsors, bill_votes, bill_votes

> Yes. **SB 5314** ("Modifying the capital gains tax") had **Paul Harris (R)** as a cosponsor, but he voted **Nay** on both final-passage motions in the Senate — "3rd Reading & Final Passage" and "Final Passage as Amended by the House."
> 
> For context on the other capital-gains-related bills I checked:
> - **HB 1376** (prepayment of capital gains taxes) was sponsored entirely by Republicans (Ed Orcutt, Mark Klicker, Cyndy Jacobsen, John Ley, Andrew Barkis), and all of them voted Yea on final passage — no flip there.
> - **SB 5813** (progressive rate structure for capital gains/estate tax) had only Democratic sponsors, so it doesn't fit the question.
> 
> So among the capital-gains bills searched, SB 5314 is the one where a Republican cosponsor (Paul Harris) voted against the bill on final passage.

## H3 (hybrid)

**Q:** Which bills about artificial intelligence had contested (non-unanimous) final passage votes, and what were the House tallies?

**Expected:** HB 1170 (AI content notices), House 56-37; HB 2225 (AI companion chatbots), House 74-21. Both contested.

### control — FAIL

tools: search_bills, search_bills, search_bills

> I identified two bills clearly about artificial intelligence that appear to have passed into law this biennium:
> 
> - **HB 1170** – "Informing users when content is developed or modified by artificial intelligence" (status: C 167 L 26 — chaptered into law)
> - **HB 2225** – "Regulating artificial intelligence companion chatbots" (status: C 168 L 26 — chaptered into law)
> 
> However, I cannot report which final-passage votes were contested or give you the House tallies. My only tool (`search_bills`) returns bill id, title, digest, status, and a relevance score — it does not expose roll-call vote data (motions, yea/nay counts, or individual member votes) for any bill, including these two. I have no other tool to query vote records.
> 
> So, plainly: I can confirm HB 1170 and HB 2225 are the AI-related bills that reached enactment, but I cannot tell you whether their final passage votes were unanimous or contested, nor provide House tallies, because that data isn't retrievable with the tools available to me. If you have access to the Washington Legislature's roll-call records (or a tool that surfaces them), that would be the place to confirm vote counts for these two bills.

### graph — pass

tools: search_bills_semantic, search_bills_semantic, search_bills_semantic, bill_vote_summary, bill_vote_summary

> Based on my search, two bills clearly about artificial intelligence reached floor votes: **HB 1170** and **HB 2225**. Both had contested (non-unanimous) Final Passage votes in the House.
> 
> **HB 1170** — "Informing users when content is developed or modified by artificial intelligence" (now C 167 L 26)
> - House, 3rd Reading & Final Passage (2026-02-13): **56 Yea – 37 Nay – 5 Excused**
> - House, Final Passage as Amended by the Senate (2026-03-11): **55 Yea – 38 Nay – 5 Excused**
> - (For context, the Senate final passage was 46 Yea – 3 Nay, much less contested.)
> 
> **HB 2225** — "Regulating artificial intelligence companion chatbots" (now C 168 L 26)
> - House, 3rd Reading & Final Passage (2026-02-17): **69 Yea – 28 Nay – 1 Excused**
> - House, Final Passage as Amended by the Senate (2026-03-11): **74 Yea – 21 Nay – 3 Excused**
> - (Senate final passage was 43 Yea – 5 Nay – 1 Excused.)
> 
> Both bills passed the House twice — once on initial passage and again to concur in Senate amendments — and both votes were contested each time, though HB 1170 was notably closer (roughly 3:2 margin) than HB 2225 (roughly 3:1 or better).
> 
> If you'd like, I can pull the individual roll-call breakdown (who voted Yea/Nay, by party) for either bill.

## H4 (hybrid)

**Q:** Find the bill about allowing alcohol service in public places and list the Democrats who voted Nay on its House final passage.

**Expected:** HB 1515; D Nay votes: Cindy Ryu, Gerry Pollet, Janice Zahn, Lauren Davis, Lisa Callan, Mari Leavitt, Roger Goodman, Sharon Tomiko Santos, Steve Bergquist (9 members).

### control — FAIL

tools: search_bills

> HB 1515 ("AN ACT Relating to modernizing the regulation of alcohol service in public spaces") is the bill you're referring to.
> 
> However, my search tool only returns bill metadata (title, digest, status) — it does not give me access to roll-call vote data, so I cannot retrieve the actual House final passage vote or identify which members, including Democrats, voted Nay on it. I don't have a tool that returns individual legislator votes, so I can't answer that part of your question reliably.
> 
> If you have access to a roll-call/vote lookup tool or can point me to one, I can cross-reference it with HB 1515's House final passage motion to identify the Nay votes by party.

### graph — pass

tools: search_bills_semantic, bill_votes

> HB 1515 ("modernizing the regulation of alcohol service in public spaces") had **two** House votes labeled with "Final Passage" — an initial passage vote ("3rd Reading & Final Passage") and a later concurrence vote after Senate amendments ("Final Passage as Amended by the Senate"). Here are the Democrats who voted Nay in each:
> 
> **3rd Reading & Final Passage (original House passage) — Democrats voting Nay:**
> - Timm Ormsby
> - Steve Bergquist
> - Lisa Callan
> - Mari Leavitt
> - Lauren Davis
> 
> **Final Passage as Amended by the Senate (House concurrence vote) — Democrats voting Nay:**
> - Sharon Tomiko Santos
> - Roger Goodman
> - Cindy Ryu
> - Gerry Pollet
> - Steve Bergquist
> - Lisa Callan
> - Mari Leavitt
> - Lauren Davis
> - Janice Zahn
> 
> Note that several Republicans also voted Nay in both motions (e.g., Tom Dent, Mary Dye, Mike Volz, Jim Walsh, Chris Corry, Joel McEntire, Peter Abbarno, Cyndy Jacobsen, Stephanie Barnard, Kevin Waters), but you asked specifically for the Democrats, listed above.
