---
name: kg-deep-research
description: Heavyweight research mode for a topic that deserves a proper dive — more sources, adversarial fact-checking, and explicit treatment of where the evidence disagrees with itself — rather than the quick pass kg-research does by default. Trigger on "go deep on X", "properly research X", "I need to actually understand X", "deep dive", any major decision, or when a quick pass has left the owner wanting more. Files output straight into the vault rather than producing a standalone report.
---

## When this rather than kg-research

Use this when being wrong has a cost: a career move, a significant purchase, a health or legal question, a technical choice that will be expensive to reverse, a belief they are about to act on. The quick pass is for building general knowledge; this is for decisions.

The difference is not just more sources. It is that you actively try to falsify what you are finding.

## Protocol

1. **Frame the actual question.** Not the topic — the decision underneath it. "Research X" and "should I do X" need different research. Establish which in one exchange, along with their constraints and what would change their mind. Read `_self/` if populated: values, constraints, risk appetite and prior commitments all bear on what counts as a good answer for them specifically.

2. **Map the positions before gathering evidence.** Who holds which view on this, and what does each side's strongest version look like? Going in with the map prevents assembling ten sources that all say the same thing and mistaking that for consensus.

3. **Gather widely — ten to twenty sources.** Deliberately include: primary sources and original research over summaries of it; the strongest available case *against* whatever the early consensus seems to be; practitioners as well as commentators; and anything that dates the claims, since a 2019 answer to a 2026 question is often simply wrong.

4. **Fact-check adversarially.** For each load-bearing claim: who is making it, what is it based on, who funds or benefits from it, has anyone credible contested it, and does the original source actually say what the secondary source claims it says? Following a claim back to its origin routinely dissolves it. When it does, that is a finding — write it down.

5. **Treat disagreement as content, not noise.** Where sources conflict, do not average them into a bland middle. Say who disagrees, on what, why, and what evidence would settle it. Separate genuine empirical uncertainty from disagreement about values, which no amount of further research will resolve.

6. **File into the vault**, per the standard pipeline — source notes in `01_Sources/`, synthesis in `03_Permanent_Notes/`, hub updated. Add one permanent note the quick pass never produces: **`what-would-change-my-mind-about-<topic>.md`**, stating the specific evidence that would overturn the conclusion. It is what stops today's research calcifying into next year's unexamined assumption.

7. **Deliver a decision brief in chat**: what the evidence supports, how confident you are and why, where it is genuinely contested, what remains unknown, and what it implies given their stated constraints. Name the weakest link in your own reasoning. End with the concrete next step.

## Rules

- **Never fabricate a source, a quote, a figure or a URL.** In this mode especially — they are going to act on it.
- **Calibrate confidence explicitly and honestly.** "Three good studies agree" and "one blog post everyone cites" are different, and collapsing them is the most damaging thing you can do here.
- **Do not manufacture a verdict.** If the evidence does not support a clear answer, say so and set out how to decide under uncertainty. A confident wrong answer is worse than an honest unresolved one.
- **Say what you could not check.** Paywalled sources, claims you could not trace, fields where you lack the expertise to judge quality — name them.
- **Their decision, not yours.** Lay out the reasoning so they can disagree with it, rather than handing down a conclusion.
