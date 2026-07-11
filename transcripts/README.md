# Transcripts

Agent sessions cited in the blog posts, preserved for auditability. Each file carries
its own provenance header: run date, tooling era, whether anything is abridged, and the
results of an independent audit of the response against `data/dataset.json`, including
the errors we found. The claims these runs make are checkable; several were checked and
a few were wrong, and the headers say exactly which.

| File | What it is |
|------|------------|
| `case-study-themes.md` | The "themes across bills" run behind post 1's worked example |
| `case-study-connectors.md` | Multi-hop: who can reach the opposition through co-sponsorship ties |
| `case-study-champions.md` | What the crossover Democrats themselves sponsor |
| `failure-misattribution.md` | ⚠️ The documented failure behind the follow-up post: real votes bound to the wrong bill. **Preserved with its errors intact — see its header for the corrections before citing anything from it.** |

Two things to know when reading:

1. **Tooling era matters.** `failure-misattribution.md` predates the exact-aggregation
   tools (`voting_bloc`, `party_crossovers`), self-describing tool rows, and the
   `verify_claims` audit step; the other three runs use them. That before/after is the
   point of the follow-up post.
2. **Answers vary across runs.** The same question re-run will pick different
   representative bills and produce a differently shaped answer (e.g., the connectors
   run built a five-bill opposition bloc of 58 members, where the themes run's four-bill
   bloc has 22). Verified facts stay stable; framing and scope wobble.
