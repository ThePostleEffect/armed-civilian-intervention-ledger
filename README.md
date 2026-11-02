# Open intervention ledger

**A public, case-level dataset of incidents in which an armed civilian stopped a shooting in the United States, 1996–2026.**

The published figure is that armed civilians stop about 4% of active shooters. That figure is produced by a dataset built for a different purpose: it records one terminal outcome per attack, has no code for an attacker who broke off because someone pointed a gun at him, files volunteer church members under "security," covers only a narrow universe of incidents, and begins in the year 2000. Corrections for those things do not produce a number that flatters anyone, but they do produce one roughly an order of magnitude larger.

This project exists to build that corrected dataset in public, from checkable records, and to publish the method alongside the number so that anyone can replicate or refute it.

---

## What this project claims — and what it does not

**It claims:** the intervention rate reported in public debate is materially understated, and the understatement comes from identifiable coding decisions rather than from a dispute about facts. Every one of those decisions is documented in [`docs/verification-protocol.md`](docs/verification-protocol.md) and testable against the data in `data/`.

**It does not claim:** that the Second Amendment is proven beneficial, that more carry causes fewer deaths, or that armed civilians are the primary civilian response. Those are separate questions. On the last one the data points the other way — unarmed civilians subdue attackers about four times as often as armed ones do — and that finding is in this dataset too, because a dataset that only contains the cases you like is not evidence.

The distinction matters practically. A dataset assembled to prove a conclusion is dismissed on sight, and its findings with it. A dataset that publishes its exclusions, its counter-cases and its error rate is hard to argue with.

---

## Current state (v0.1, seed)

| Tier | Records | Meaning |
|---|---|---|
| Confidence B — verified | **15** | Official dataset coding (FBI/ALERRT), civilian shot the attacker, 2000–2025 |
| Confidence D — candidate | **9** | Single verified news source each; 1996–2013 sweep; second source required to promote |
| Confidence E — candidate | **242** | Secondary compilation only (CPRC list). Unverified, not publishable, awaiting upgrade |
| Excluded | **1** | Duplicate caught by the validator |
| Source rows | **267** | Every incident has at least one; 4 captured and archived so far |

**First job of the project: upgrade the 242.** Each needs a primary or contemporaneous source before it can be counted. Expect a meaningful share to fail — that is the point of the exercise, and the failure rate is itself a finding.

---

## Repository layout

```
schema/case.schema.json        field definitions, enums, protocol rules encoded
data/cases.csv                 the ledger — one row per incident
data/sources.csv               one row per source; every incident has at least one
data/adjudication_log.csv      every exclusion, with reason and reviewer
captures/                      filed PDFs and screenshots of archived sources
docs/verification-protocol.md  source tiers, promotion rules, dispute process
docs/source-archiving.md       the link-or-capture rule and how to comply
docs/state-lead-playbook.md    how to run one state, including a records request
intake/index.html              offline-capable submission form (no server needed)
scripts/validate.py            schema + protocol validator, stdlib only
scripts/capture_source.py      renders a source to PDF + Wayback snapshot
```

Run the validator before every commit:

```bash
python scripts/validate.py data/cases.csv
```

It fails on enum violations, malformed IDs, unparseable dates, incidents with no source rows, **sources with neither a URL nor a filed capture**, gated sources with no capture, and verified records with insufficient sourcing. It warns on duplicates and on web sources that have no archive snapshot.

```bash
python scripts/capture_source.py S0037        # PDF + Wayback snapshot, fields written back
```

---

## The status ladder

No record is ever deleted, and no record is ever self-certifying.

1. **candidate** — submitted, sourced, unverified.
2. **verified** — satisfies the confidence rule (A, B or C) and has been reviewed by two people who are not the submitter.
3. **disputed** — a challenge has been filed; the record stays in the dataset with the challenge attached until adjudicated.
4. **excluded** — fails inclusion criteria or duplicates an existing record. **Excluded records stay in the file.** Deleting them is how datasets become untrustworthy.

Only `verified` records are used in published counts. Every published figure must state how many records sat at each tier.

---

## Confidence tiers

| Tier | Source | Publishable |
|---|---|---|
| **A** | Primary record: court filing, prosecutor statement, police report, coroner finding, NIBRS extract | yes |
| **B** | Official dataset: FBI active-shooter report, ALERRT Active Attack Data | yes |
| **C** | Two or more independent contemporaneous news sources | yes |
| **D** | One news source only | no — needs a second |
| **E** | Secondary compilation (CPRC, NRA, Cato, Wikipedia lists) | no — leads only, never evidence |

### Every source is archived

A record is only as good as the ability of a stranger to check it later. Each source therefore carries **a URL or a filed capture, and usually both**: the live link for convenience, a Wayback snapshot for permanence, and a local PDF or screenshot in `captures/` for the cases where the link is paywalled, blocked, print-only or broadcast. A source with neither is a validation error and the record cannot be published.

The rule is in [`docs/source-archiving.md`](docs/source-archiving.md), including what to do when the source is microfilm and no link will ever exist.

---

## Inclusion criteria

An incident qualifies when **all** of the following hold:

1. It occurred in the United States, 1 January 1996 onward.
2. An attacker was killing or attempting to kill people in a public or semi-public place, or had begun an attack that had not yet concluded.
3. A person who was **not** on-duty law enforcement, not off-duty law enforcement acting in that capacity, and not professional security took direct action with a firearm.
4. That action caused the attack to stop — by any mechanism: attacker shot, held at gunpoint, disarmed, fled, surrendered, or killed himself after being confronted.

**Counter-cases are required, not optional.** Any incident where an armed civilian intervened and (a) was shot, (b) hit a bystander, (c) was disarmed, or (d) failed to stop the attack is coded `mechanism=no_effect` and **kept**. A dataset without these cannot report a risk rate, and the risk rate is the most useful thing it could contribute.

---

## Contributing

Read [`docs/state-lead-playbook.md`](docs/state-lead-playbook.md). In short:

- Claim a state and a year window. One lead per state, publicly listed.
- Pull from primary sources first. NIBRS extracts, prosecutor press releases, coroner findings, court dockets.
- Submit through `intake/index.html`. One incident per submission.
- A second reviewer must confirm before promotion. The submitter is never the confirmer.
- Log every exclusion in `data/adjudication_log.csv` with a reason.

Corrections and challenges are welcome and are the point. If a record is wrong, open an issue with the source; it will be re-adjudicated in public.

---

## Governance and licensing

- **Data:** CC BY 4.0. Use it, including to argue against it. Attribution required.
- **Code:** MIT.
- **Neutrality rule:** no funder, donor or campaign may veto a finding. If the numbers turn out to be unhelpful to the project's originating hypothesis, they get published anyway — that commitment is the only thing that separates this from an advocacy mailer.

---

## Roadmap

1. **v0.2** — upgrade all 242 confidence-E records against primary sources; publish the pass/fail rate.
2. **v0.3** — complete the 1996–2013 sweep across all 50 states; target window for the missing cases.
3. **v1.0** — code every record for time-to-intervention and gun-free-zone status, which no existing dataset carries, and publish the first defensible risk rate (bystanders hit, interveners injured per 100 interventions).
4. **Ongoing** — annual republication alongside each FBI report, so the comparison is automatic and dated.

---

*Independent research project. Not affiliated with the FBI, ALERRT, the Crime Prevention Research Center, or any advocacy organisation. Seed data assembled 2026-11-01; source URLs are retained per record.*
