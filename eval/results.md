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

> Based on the bill digests, several bills addressing unemployment insurance passed during the 2025-26 biennium (all show a "C ... L ..." chapter/law status, indicating they were enacted):
> 
> 1. **SB 5041** – *Unemployment insurance benefits for striking or lockout workers.* Status: C 352 L 25 (passed in the 2025 session).
> 
> 2. **SB 6134** – *Notice to striking workers applying for unemployment insurance benefits of potential overpayment assessment upon receipt of retroactive wages.* Status: C 161 L 26 (passed in the 2026 session).
> 
> 3. **HB 2264** – *Unemployment insurance benefits for workers separated from employment as a result of employer-initiated layoffs or workforce reductions.* Status: C 150 L 26 (passed in the 2026 session).
> 
> 4. **SB 5874** – *Employers' information reporting for purposes of unemployment compensation.* Status: C 43 L 26 (passed in the 2026 session).
> 
> A closely related bill on layoffs (not strictly "unemployment insurance" but connected to unemployment/benefits for laid-off workers) also passed:
> 
> - **SB 6106** – Modifies the "securing timely notification and benefits for laid-off employees act," updating the definition of employer and adding a public-disclosure exemption for employee data. Status: C 86 L 26.
> - **SB 5525** – Protects workers facing employment loss due to business closings or mass layoffs. Status: C 277 L 25.
> 
> If you'd like, I can pull the specific final-passage vote counts and sponsor information for any of these bills.

### graph — pass

tools: search_bills_semantic

> Based on my search, here are the bills that passed this biennium dealing directly with unemployment insurance (all show a "C ... L 25/26" status, indicating they were signed into law):
> 
> 1. **SB 5041** – "Unemployment insurance benefits for striking or lockout workers" (C 352 L 25)
> 2. **HB 2264** – "Unemployment insurance benefits for workers separated from employment as a result of employer-initiated layoffs or workforce reductions" (C 150 L 26)
> 3. **SB 6134** – "Notice to striking workers applying for unemployment insurance benefits of potential overpayment assessment upon receipt of retroactive wages" (C 161 L 26)
> 4. **SB 5874** – "Employers' information reporting for purposes of unemployment compensation" (C 43 L 26)
> 
> A few related but distinct labor-benefit bills also appeared in the search (e.g., SB 6106 on the laid-off employees notification act, and SB 5525 on business closures/mass layoffs), but these concern layoff notification rather than unemployment insurance benefits specifically — let me know if you'd like details on those as well, or votes/sponsors for any of the four bills above.

## S2 (semantic)

**Q:** What legislation addresses protections or housing stability for residential tenants?

**Expected:** HB 1217 (residential tenants / rent stabilization); SB 5937 (smart access systems/tenants) is a bonus.

### control — pass

tools: search_bills, search_bills, search_bills

> Several bills from the 2025-26 Washington State Legislature address protections and housing stability for residential tenants:
> 
> **Core tenant protection/housing stability legislation:**
> 
> - **HB 1217** – The most comprehensive bill on this topic. It improves housing stability for tenants under the residential landlord-tenant act and manufactured/mobile home landlord-tenant act by: limiting rent and fee increases, requiring notice of rent/fee increases, limiting fees and deposits, establishing a landlord resource center, authorizing tenant lease termination, creating parity between lease types, and providing for attorney general enforcement. (Status: C 209 L 25 — signed into law)
> 
> **Notice and procedural protections:**
> 
> - **HB 2452** – Modifies requirements for service of rent increase notices. (C 118 L 26)
> - **HB 2664** – Modifies requirements for service of unlawful detainer notices and related notices. (C 144 L 26)
> - **HB 1003** – Addresses service of notice by mail in forcible entry and unlawful detainer cases. (C 44 L 25)
> - **SB 5298** – Concerns notice of sale or lease of manufactured/mobile home communities. (C 205 L 25)
> 
> **Access, safety, and habitability:**
> 
> - **SB 5937** – Regulates use of smart access systems in residential rental properties. (C 55 L 26)
> - **SB 6200** – Allows renters and mobile home occupants to install portable cooling devices. (C 184 L 26)
> - **SB 6237** – Requires rental property disclosures of flooding history and flood risk. (C 234 L 26)
> 
> **Court capacity for eviction cases:**
> 
> - **HB 1621** – Authorizes superior courts to appoint housing court commissioners to address court capacity for unlawful detainer (eviction) actions. (C 268 L 25)
> 
> **Related but broader housing bills:**
> 
> - **HB 2266** – Encourages permanent supportive housing, transitional housing, and emergency shelters. (C 232 L 26)
> - **HB 1757** – Modifies regulations for existing buildings used for residential purposes. (C 203 L 25)
> 
> If you'd like, I can pull sponsor information or roll-call vote details (e.g., Yea/Nay counts, party breakdowns) for any of these bills — HB 1217 in particular, since it's the flagship tenant-protection bill.

### graph — pass

tools: search_bills_semantic

> The bill most directly on point is **HB 1217** — "AN ACT Relating to improving housing stability for tenants subject to the residential landlord-tenant act and the manufactured/mobile home landlord-tenant act." It:
> 
> - Limits rent and fee increases
> - Requires notice of rent and fee increases
> - Limits fees and deposits
> - Establishes a landlord resource center and associated services
> - Authorizes tenant lease termination
> - Creates parity between lease types
> - Provides for attorney general enforcement
> 
> Its status is **C 209 L 25** (signed into law, Chapter 209, Laws of 2025).
> 
> A related, narrower bill is **SB 5937** — "AN ACT Relating to the use of a smart access system in a residential property subject to the residential landlord-tenant act," which regulates keyless/smart-lock entry systems landlords use in tenant units (status: C 55 L 26).
> 
> Would you like details on HB 1217's sponsors or the roll-call votes (e.g., Final Passage tally) to see how it passed?

## S3 (semantic)

**Q:** Which bills concern artificial intelligence?

**Expected:** HB 1170 (AI content notices) and HB 2225 (AI companion chatbots).

### control — pass

tools: search_bills

> Based on my search, two bills clearly and directly concern artificial intelligence:
> 
> 1. **HB 1170** – "AN ACT Relating to informing users when content is developed or modified by artificial intelligence." This bill would require disclosure to users when content has been created or altered by AI. Status: C 167 L 26 (enacted as Chapter 167, Laws of 2026).
> 
> 2. **HB 2225** – "AN ACT Relating to regulation of artificial intelligence companion chatbots." This bill regulates AI companion chatbots. Status: C 168 L 26 (enacted as Chapter 168, Laws of 2026).
> 
> The rest of the search results (e.g., SCR 8401, HJM 4001, HB 2113, SB 5937, SB 6025, HCR 4407, SJM 8002, SB 6002) do not substantively relate to artificial intelligence — they came up due to loose semantic matches but concern unrelated topics like joint rules, memorials, radiologic technologist supervision, landlord-tenant smart locks, fetal death definitions, and license plate readers.
> 
> If you'd like, I can pull sponsor and roll-call vote details for HB 1170 or HB 2225.

### graph — pass

tools: search_bills_semantic, search_bills_semantic, search_bills_semantic

> Based on my search of bill digests, two bills directly and explicitly concern artificial intelligence:
> 
> 1. **HB 1170** – "Informing users when content is developed or modified by artificial intelligence." This bill requires disclosure to users when content has been created or altered by AI. Status: enacted (C 167 L 26).
> 
> 2. **HB 2225** – "Regulating artificial intelligence companion chatbots." This bill sets rules around AI companion chatbot products/services. Status: enacted (C 168 L 26).
> 
> I ran additional searches (e.g., "automated decision making algorithm," "generative AI in education") but found no other bills substantively about AI — other near matches (like SB 6002 on automated license plate readers, or various education bills) are not really AI-focused, just tangentially related by keyword similarity. If you'd like, I can pull sponsors and vote details for HB 1170 and HB 2225.

## S4 (semantic)

**Q:** Is there legislation about student cell phone or mobile device use in schools?

**Expected:** Yes — SB 5346 (student mobile device use).

### control — pass

tools: search_bills

> Yes — **SB 5346**, "AN ACT Relating to student use of mobile devices in public schools," directly addresses this topic. It concerns student use of mobile devices in public schools and has a status of "C 225 L 26" (chaptered as Chapter 225, Laws of 2026), indicating it passed into law.
> 
> None of the other bills returned are substantively about student phone/device use in schools — they cover unrelated topics like behavioral health supports (HB 1634), mobile market programs (SB 5214), school transportation (SB 6065, SB 5009), school safety penalties (SB 5272), and other education administration matters.
> 
> If you'd like, I can look up the sponsors and roll-call vote details for SB 5346.

### graph — pass

tools: search_bills_semantic, bill_info, bill_sponsors, bill_vote_summary

> ## SB 5346 — Student Use of Mobile Devices in Public Schools
> 
> **Summary:** This bill addresses student use of mobile devices in public schools. It is now law, enacted as **Chapter 225, Laws of 2026** (current version: SSB 5346).
> 
> **Sponsorship:** A broad bipartisan effort led by primary sponsor **Sen. Marko Liias (D)**, with cosponsors from both parties including Sen. Paul Harris (R), Sen. Sharon Shewmake (D), Sen. Perry Dozier (R), Sen. Jessica Bateman (D), Sen. Leonard Christian (R), Sen. Noel Frame (D), Sen. Bob Hasegawa (D), Sen. Curtis King (R), Sen. Deborah Krishnadasan (D), Sen. John Lovick (D), Sen. T'wina Nobles (D), and Sen. Jesse Salomon (D).
> 
> **Legislative path & votes:**
> - **Senate, 3rd Reading & Final Passage (2026-02-11):** Passed 37 Yea – 12 Nay
> - **House, Final Passage as Amended by House (2026-03-04):** Passed 63 Yea – 34 Nay – 1 Excused
> - **Senate, Final Passage as Amended by House (2026-03-09):** Concurred 43 Yea – 4 Nay – 2 Excused
> 
> The bill passed with strong support in both chambers, gaining even wider margins after the House amendment came back to the Senate for concurrence — suggesting the amended version was broadly acceptable across party lines.
> 
> If you'd like, I can pull the full digest text/amendment details or look at which specific members voted against it.

## R1 (relational)

**Q:** Which Democratic senators voted Nay on the Senate 3rd Reading & Final Passage of SB 5041?

**Expected:** Lisa Wellman and Mike Chapman.

### control — FAIL

tools: search_bills

> I found SB 5041 (unemployment insurance benefits for striking or lockout workers), but my only tool is a semantic search over bill digests/titles/status — it does not contain roll-call vote data (individual member votes, party breakdowns, or Yea/Nay counts).
> 
> I cannot retrieve which specific senators voted Nay on the Final Passage vote for SB 5041, including any Democratic senators, because that data isn't available through the tool I have access to. I don't want to guess names or counts, so I can't answer this question reliably. If a vote-data tool becomes available, I'd be able to look up the exact roll call for you.

### graph — pass

tools: bill_votes

> On the Senate 3rd Reading & Final Passage vote for SB 5041, two Democratic senators voted Nay:
> 
> - **Mike Chapman** (D-Senate)
> - **Lisa Wellman** (D-Senate)
> 
> All other Nay votes on this motion came from Republican senators.

## R2 (relational)

**Q:** Which cosponsors of SB 5041 voted against it on final passage?

**Expected:** Lisa Wellman (cosponsored the bill, voted Nay on Senate final passage).

### control — FAIL

tools: search_bills

> I don't have access to sponsor lists or roll-call vote data for individual members through my tools — the search_bills tool only returns bill id, title, digest, and status (as shown above for SB 5041). It does not provide cosponsor names or vote records.
> 
> Because of this limitation, I can't determine which cosponsors of SB 5041 (if any) voted against it on final passage. I don't want to guess member names or vote outcomes without supporting data. If you have access to a roll-call vote source or sponsor list, I'd be happy to help analyze it once that information is available.

### graph — pass

tools: bill_sponsors, bill_votes

> Cross-referencing the cosponsor list with the "Nay" votes on final passage of SB 5041, one cosponsor voted against the bill despite having cosponsored it:
> 
> - **Lisa Wellman (D-Senate)** — voted Nay on both "3rd Reading & Final Passage" and "Final Passage as Recommended by Conference Committee."
> 
> None of the other listed cosponsors (Riccelli, Conway, Hasegawa, Saldaña, Salomon, Stanford, Dhingra, Nobles, Trudeau, Valdez, Bateman, Lovelett, Cleveland, Frame, Orwall, Pedersen, Slatter, Wilson) appear among the Nay votes.

## R3 (relational)

**Q:** Which Democrats voted Nay on the House final passage of HB 2049, the K-12 education funding bill?

**Expected:** Adam Bernbaum, Adison Richards, Alicia Rule, Clyde Shavers, Dave Paul, Joe Timmons, Mari Leavitt, Melanie Morgan, Shelley Kloba (9 members, House 3rd Reading & Final Passage).

### control — FAIL

tools: search_bills

> My tool only provides bill digests, titles, and status (semantic search over bill text) — it does not return roll-call vote data, sponsor lists, or individual member votes. I can confirm that HB 2049 exists ("Investing in the state's paramount duty to fund K-12 education and build strong and safe communities," status: C 404 L 25), but I have no way to retrieve who voted Yea/Nay on its final passage, let alone break that down by party.
> 
> I can't answer which Democrats voted Nay on HB 2049's House final passage — that data isn't accessible with my current tools. If a roll-call vote lookup tool becomes available, I'd be able to answer this precisely.

### graph — pass

tools: bill_info, bill_votes

> On the House Final Passage vote for HB 2049 ("Investing in the state's paramount duty to fund K-12 education..."), the following Democrats voted **Nay**:
> 
> - Adison Richards (D)
> - Shelley Kloba (D)
> - Dave Paul (D)
> - Mari Leavitt (D)
> - Melanie Morgan (D)
> - Alicia Rule (D)
> - Joe Timmons (D)
> - Clyde Shavers (D)
> - Adam Bernbaum (D)
> 
> All other Nay votes on this motion came from Republican members.

## R4 (relational)

**Q:** Did any sponsor of HB 1620 (parenting plan limitations) vote against it on final passage? Who?

**Expected:** Yes — cosponsors Roger Goodman and Natasha Hill voted Nay on House final passage.

### control — FAIL

tools: search_bills

> I don't have access to sponsor lists or roll-call vote details for individual bills through my available tools—my search only returns bill title, digest, and status (HB 1620, "Concerning limitations in parenting plans," status: C 166 L 25). I cannot retrieve the list of sponsors or the individual Yea/Nay votes on final passage, so I cannot determine whether any sponsor voted against it.
> 
> If you have access to the legislature's roll-call vote records or sponsor list, I'd be happy to help analyze that data if you provide it.

### graph — pass

tools: bill_sponsors, bill_votes

> Yes. Two of HB 1620's own sponsors voted "Nay" on final passage:
> 
> - **Roger Goodman (D-House)** — cosponsor, voted Nay on "3rd Reading & Final Passage"
> - **Natasha Hill (D-House)** — cosponsor, voted Nay on "3rd Reading & Final Passage"
> 
> The primary sponsor, Jamila Taylor (D), and cosponsor Julia Reed (D) are not listed among the Nay votes, so it appears they voted Yea (or were not recorded as Nay).

## H1 (hybrid)

**Q:** Find the major bill about residential rent stabilization and report how close its Senate final passage vote was.

**Expected:** HB 1217; Senate final passage was 29 Yea to 20 Nay.

### control — FAIL

tools: search_bills, search_bills

> The search tool only returns bill digests (title, summary, status) — it does not provide roll-call vote data, vote counts, or member-level voting records. This means I cannot retrieve the actual Senate final passage vote tally for **HB 1217** ("AN ACT Relating to improving housing stability for tenants... limiting rent and fee increases..." — the residential rent stabilization bill, enacted as **C 209 L 25**).
> 
> I can confirm HB 1217 is the major rent stabilization bill you're asking about, but I do not have access to a tool that returns roll-call vote breakdowns (Yea/Nay counts by chamber), so I can't tell you how close the Senate final passage vote was. If you have a tool or source for roll-call data, I'd be happy to analyze it.

### graph — pass

tools: search_bills_semantic, bill_vote_summary

> The major bill on residential rent stabilization is **HB 1217** ("Improving housing stability for tenants... by limiting rent and fee increases..."), which became law as Chapter 209, Laws of 2025.
> 
> **Senate final passage vote** (Final Passage as Recommended by Conference Committee, April 27, 2025):
> - **Yea: 27**
> - **Nay: 20**
> - **Excused: 1**
> 
> This was a fairly narrow margin — the bill passed the Senate by just 7 votes. (Note: an earlier Senate vote on its own amended version, "3rd Reading & Final Passage as Amended by the Senate" on April 10, 2025, was 29 Yea–20 Nay, but the decisive vote sending the bill to the Governor was the conference-committee version, 27–20.)

## H2 (hybrid)

**Q:** Among bills about the capital gains tax, did any Republican cosponsor one and then vote against it on final passage?

**Expected:** Yes — Paul Harris (R) cosponsored SB 5314 and voted Nay on its final passage.

### control — FAIL

tools: search_bills

> I found the bills most directly related to the capital gains tax (HB 1376, SB 5314, SB 5813), but my only tool is `search_bills`, which returns just the bill ID, title, digest, and status — it does not return sponsor lists, cosponsor information, or roll-call vote data.
> 
> I cannot retrieve information on who cosponsored these bills or how individual legislators voted on final passage, because no tool available to me exposes sponsor rosters or member-level vote records. As a result, I'm unable to determine whether any Republican cosponsored a capital gains tax bill and then voted against it on final passage — I don't have the data access needed to verify that claim, and I don't want to guess names or vote outcomes.
> 
> If a tool for retrieving bill sponsors and roll-call votes becomes available, I could answer this precisely.

### graph — pass

tools: search_bills_semantic, bill_sponsors, bill_sponsors, bill_sponsors, bill_votes, bill_votes

> Yes. On **SB 5314** ("Modifying the capital gains tax"), Senator **Paul Harris (R)** was a listed cosponsor, but he voted **Nay** on both final-passage motions ("3rd Reading & Final Passage" and "Final Passage as Amended by the House").
> 
> For comparison, the other capital-gains-related bill with Republican involvement, **HB 1376** ("prepayment of capital gains taxes six months prior to the due date"), was actually a Republican-sponsored bill (primary sponsor Ed Orcutt, R, with cosponsors Mark Klicker, Cyndy Jacobsen, John Ley, and Andrew Barkis, all R) — all of those cosponsors voted **Yea** on final passage, so no defection there.
> 
> **SB 5813** (progressive capital gains/estate tax rate structure) had no Republican cosponsors.
> 
> So the only case of a Republican cosponsoring a capital-gains-tax bill and then voting against it on final passage is Paul Harris on SB 5314.

## H3 (hybrid)

**Q:** Which bills about artificial intelligence had contested (non-unanimous) final passage votes, and what were the House tallies?

**Expected:** HB 1170 (AI content notices), House 56-37; HB 2225 (AI companion chatbots), House 74-21. Both contested.

### control — FAIL

tools: search_bills

> I found two bills clearly about artificial intelligence:
> 
> - **HB 1170** – "Informing users when content is developed or modified by artificial intelligence" (status: C 167 L 26 — enacted)
> - **HB 2225** – "Regulating artificial intelligence companion chatbots" (status: C 168 L 26 — enacted)
> 
> However, I'm unable to report on which of these had **contested (non-unanimous) final passage votes** or give **House tallies**, because my only available tool (`search_bills`) returns just bill ID, title, digest, and status — it does not provide roll-call vote data, vote counts, or motion-level detail (e.g., "Final Passage" tallies). I don't have a tool to look up individual member votes or chamber tallies, so I can't verify or guess at the numbers.
> 
> If you have access to a vote-lookup tool or can share vote data, I can help analyze it. Otherwise, based on current tools, I can only confirm these two bills as AI-related and enacted, not the contested nature of their final passage votes or the specific House tallies.

### graph — pass

tools: search_bills_semantic, search_bills_semantic, search_bills_semantic, bill_votes, bill_votes, bill_vote_summary, bill_vote_summary

> Both AI-related bills in the WA 2025-26 biennium had contested (non-unanimous) final passage votes in the House:
> 
> **HB 1170** — "Informing users when content is developed or modified by artificial intelligence"
> - House "3rd Reading & Final Passage" (2026-02-13): **56 Yea – 37 Nay – 5 Excused**
> - House "Final Passage as Amended by the Senate" (2026-03-11): **55 Yea – 38 Nay – 5 Excused**
> - (Senate final passage was 46-3, also contested but far more lopsided.)
> 
> **HB 2225** — "Regulating artificial intelligence companion chatbots"
> - House "3rd Reading & Final Passage" (2026-02-17): **69 Yea – 28 Nay – 1 Excused**
> - House "Final Passage as Amended by the Senate" (2026-03-11): **74 Yea – 21 Nay – 3 Excused**
> - (Senate final passage was 43-5.)
> 
> Both votes broke largely along party lines, with most Republicans voting Nay on HB 1170 and a smaller but still substantial bloc opposing HB 2225 (e.g., Jim Walsh, Matt Marshall, Andrew Barkis, Jenny Graham voting Nay on both bills in both House votes).
> 
> I searched using semantic queries for "artificial intelligence," "automated decision system/algorithm regulation," and "AI in government/employment," and these two bills were the only ones clearly centered on AI regulation that reached House floor votes. I don't have a comprehensive keyword/tag index, so if there are other AI-related bills not surfaced by these searches, I can't confirm their absence with certainty — but these two account for the AI bills that appeared repeatedly across all queries.

## H4 (hybrid)

**Q:** Find the bill about allowing alcohol service in public places and list the Democrats who voted Nay on its House final passage.

**Expected:** HB 1515; D Nay votes: Cindy Ryu, Gerry Pollet, Janice Zahn, Lauren Davis, Lisa Callan, Mari Leavitt, Roger Goodman, Sharon Tomiko Santos, Steve Bergquist (9 members).

### control — FAIL

tools: search_bills

> I found the bill: **HB 1515** – "AN ACT Relating to modernizing the regulation of alcohol service in public spaces" (this is the bill about allowing alcohol service in public places; it was enacted as C 361 L 25).
> 
> However, I'm unable to provide the list of Democrats who voted Nay on its House final passage. My only available tool (`search_bills`) returns bill title, digest, and status — it does not provide roll-call vote data or member-level voting records. I don't have a tool that can retrieve individual legislator votes, so I can't ground a list of "Nay" voters in actual data.
> 
> If you have access to a roll-call/vote-lookup tool, I'd be glad to use it — but with what's available to me now, I can only confirm the bill itself, not the vote breakdown.

### graph — pass

tools: search_bills_semantic, bill_votes

> **Bill:** HB 1515 – "Modernizing the regulation of alcohol service in public spaces" (enacted as C 361 L 25).
> 
> HB 1515 had two House final-passage votes: the original **3rd Reading & Final Passage** and, after Senate amendments, a **Final Passage as Amended by the Senate** vote (the decisive vote that sent it to the Governor).
> 
> **Democrats who voted Nay:**
> 
> *3rd Reading & Final Passage (original House vote):*
> - Timm Ormsby (D)
> - Steve Bergquist (D)
> - Lisa Callan (D)
> - Mari Leavitt (D)
> - Lauren Davis (D)
> 
> *Final Passage as Amended by the Senate (final concurrence vote):*
> - Sharon Tomiko Santos (D)
> - Roger Goodman (D)
> - Cindy Ryu (D)
> - Gerry Pollet (D)
> - Steve Bergquist (D)
> - Lisa Callan (D)
> - Mari Leavitt (D)
> - Lauren Davis (D)
> - Janice Zahn (D)
> 
> If you consider the "decisive" House final passage to be the concurrence vote (Final Passage as Amended by the Senate), the Democrats voting Nay were: **Sharon Tomiko Santos, Roger Goodman, Cindy Ryu, Gerry Pollet, Steve Bergquist, Lisa Callan, Mari Leavitt, Lauren Davis, and Janice Zahn.**
