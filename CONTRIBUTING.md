# Contributing

Two ways to help, in order of value: **submit a case you have sourced yourself**, or **review someone else's**.

Read [`docs/verification-protocol.md`](docs/verification-protocol.md) before your first submission. It is short and it is enforced in CI.

---

## Before you start

- **One incident per submission.** Two incidents in one issue will be closed and asked for again.
- **Every source needs a URL or a filed capture.** A source with neither fails validation and will not be merged. See [`docs/source-archiving.md`](docs/source-archiving.md).
- **No aggregators as sources.** "CPRC says it happened" is a lead, not a source. Find the article or the record.
- **Counter-cases are welcome and required.** If the armed civilian was shot, hit a bystander, had the gun taken, or failed to stop the attack, that is a record we want.

## Submitting

1. Open a [case submission issue](.github/ISSUE_TEMPLATE/case-submission.yml) **or** build the record with `intake/index.html` and open a PR adding the row.
2. Include at least one source you have opened and read.
3. A maintainer or another contributor reviews it. Someone other than you confirms it before it is marked `verified`.
4. If it is rejected, it still gets logged in `data/adjudication_log.csv` with a reason. Nothing is deleted.

## Reviewing

Reviews are what make the dataset worth having. To review:

- Open the record's sources yourself. Do not take the submitter's summary as correct.
- Check the three things that are most often wrong: **was the intervener actually a civilian**, **does the source actually say what the record claims**, **is the mechanism coded honestly** (shot vs fled vs surrendered).
- If you cannot open a source, that is a finding — say so in the review.

## Style rules for records

| Field | Rule |
|---|---|
| `date` | ISO `YYYY-MM-DD`. Normalise odd formats at ingest; keep the original wording in `notes` |
| `state` | Two-letter code |
| `intervener_type` | If the source does not establish it, `unknown`. Never assume |
| `firearm_legal_status` | If the source does not say "permit", the answer is `unknown`, not `permit_holder` |
| `prevented_further_deaths` | `yes` requires evidence of capacity and intent to keep killing |
| `attacker_had_stopped_firing` | Code honestly even where it weakens the case |
| `notes` | Put the uncertainty here, not the advocacy |

## What gets a contribution rejected

- A fabricated or unopenable source.
- A record promoted to `verified` by the person who researched it.
- Deleting an exclusion rather than logging it.
- An off-duty police officer or professional guard entered as a civilian.

## Prose, licensing, attribution

By contributing you agree that your contribution is licensed under CC BY 4.0 (data) and MIT (code). Do not paste blocks of text from a source into the `notes` field — record the facts and cite the source. Facts are not copyrightable; someone else's sentences are.

## Questions

Open a discussion or an issue. There are no stupid questions here, only unsourced records.
