# Verification protocol

This document is the rulebook. If a record violates it, it is a `candidate` no matter how true the story is.

---

## 1. The unit of record

**One incident per row.** Not one shooter, not one article, not one intervener. If two people fired at the same attacker in the same event, that is one incident with two interveners recorded in the `intervener_detail` field.

If one attacker attacked two locations in sequence, that is **one incident** (matching ALERRT and FBI practice). Record both locations in `notes`.

---

## 2. What qualifies

All five must hold:

1. **Place and time.** United States, on or after 1 January 1996.
2. **Attack in progress or imminent.** The attacker was killing or attempting to kill people in a public or semi-public place. A person who merely displayed a gun without attacking is **not** an active attack — that is `mechanism=fled_after_confrontation` only if shots had already been fired.
3. **The intervener is a private citizen.** Not on-duty police, not off-duty police acting in that capacity, not professional security, not a school resource officer. Volunteer security counts as civilian **when the person is unpaid and holds an ordinary carry permit** — the New Life Church case is the test case, logged as `included_reclassified`.
4. **Lawful possession of the firearm.** Permit holder, constitutional carry, or lawful owner. If the intervener was a prohibited person, the record is kept but flagged — it is a counter-example, not a supporting case.
5. **The intervention caused the attack to stop** — by any mechanism: shot, held at gunpoint, physically disarmed, attacker fled, attacker surrendered, attacker shot himself after being confronted.

## 2a. What does not qualify

- Robbery, burglary, home invasion, carjacking, drug dispute, or domestic violence **inside a private residence**, with no element of attacking multiple people in a public place.
- A person who drew a gun and the attacker never knew they were there, and the attack continued unchanged.
- A person who fired and missed while the attacker kept going — unless the attack stopped as a result (then it is `mechanism=fled_after_confrontation`).

**Borderline cases are kept and labelled, not silently dropped.** The `notes` field must state the doubt. A reviewer reading the row six months later should be able to see exactly what was uncertain.

---

## 3. Source tiers

| Tier | Definition | Publishable |
|---|---|---|
| **A** | Primary record: court filing, plea or sentencing document, prosecutor statement, police report, coroner finding, NIBRS extract | yes |
| **B** | Official dataset: FBI active-shooter report, ALERRT Active Attack Data | yes |
| **C** | Two or more independent contemporaneous news sources (different outlets, within 7 days of the event) | yes |
| **D** | A single news source, or retrospective coverage only | no |
| **E** | Secondary compilation (CPRC, NRA, Cato, Wikipedia, blog lists) | **never** — leads only |

**Three rules that matter more than the table:**

- **An aggregator is not a source.** "CPRC says it happened" is a lead. It becomes a record only when the underlying article or record is found and archived.
- **Independence is not plurality.** Three articles that all rewrite the same AP wire story are one source. Check the byline.
- **A record may be downgraded.** If a second source contradicts the first, the tier drops to D and the status goes to `disputed` until resolved.

---

## 4. Every source gets a link or a capture

See [`source-archiving.md`](source-archiving.md). No URL **and** no filed capture = validation error. Paywalled, blocked, print, and broadcast sources require a local capture without exception.

---

## 5. Promotion: candidate → verified

1. The submitter fills the intake form. Status is `candidate`.
2. A **second person** — never the submitter — checks the record against the sources. They set `reviewer_2`.
3. The record is promoted to `verified` only if the confidence rule is met (A, B or C) **and** every source has a URL or capture.
4. Anything that fails goes to `data/adjudication_log.csv` with a reason code, not to the bin.

**Two people, one of whom did not do the research.** Self-certification is the single most common failure mode in volunteer datasets, and it is fatal to credibility.

---

## 6. Disputes

Anyone may challenge any record. The process:

1. Open an issue with the record ID and a source.
2. The record's status becomes `disputed`. It stays in the dataset and stays visible.
3. The original reviewer responds within 30 days.
4. Adjudication is logged publicly with the reasoning.
5. If the record is wrong, it becomes `excluded` — **and remains in the file**, with the reason attached.

Records are never deleted. A dataset that deletes its mistakes cannot be audited, and anyone who wants to discredit it only needs to find one.

---

## 7. Counter-cases are mandatory

For every incident where an armed civilian intervened and:

- was shot or killed,
- shot a bystander,
- had the weapon taken away,
- or failed to stop the attack,

the record is entered with `mechanism=no_effect` (or the relevant outcome) and kept in the live dataset.

**Why this is non-negotiable:** without the denominator of failures, the project cannot report a risk rate, and the risk rate is the most valuable contribution it could make. CPRC's own deep-dive — 180 cases, one bystander hit (0.56%), two interveners killed (1.1%) — is only credible *because* it counts the failures. Ours must do the same, and it must publish the number even if the number is unflattering.

---

## 8. Coding discipline

- **Don't code what you infer.** If the source doesn't say the intervener had a permit, write `unknown`, not `permit_holder`.
- **`prevented_further_deaths=yes` requires evidence of capacity and intent** — the attacker had ammunition, was moving toward more people, said so. Otherwise `unknown`. This field is where advocacy datasets inflate their claims, and it is the first thing a critic will test.
- **`attacker_had_stopped_firing`** must be coded honestly even when it weakens the case. Pearl High School 1997 is the canonical example: the attacker had finished shooting and was driving away. The record is kept, the field is set, and the analysis reports both readings.
- **Note the doubt.** Every row has a `notes` field. Use it for what you are unsure about, not what you are proud of.
