# State lead playbook

You own one state and one window. That's it. The project fails if 50 people each try to own everything, and it succeeds if 50 people each do a boring, complete job on a small patch.

**One state, one window, every case — including the ones that don't help the argument.**

---

## 1. What you're accountable for

| Deliverable | Standard |
|---|---|
| Coverage | Every qualifying incident in your state for your window, or a documented reason there are none |
| Sourcing | Every record has a URL **or** a filed capture in `captures/` |
| Archive | Every web source has a Wayback snapshot |
| Exclusions | Logged in `data/adjudication_log.csv` with a reason code |
| Review | Your records confirmed by someone who isn't you |

A state lead who submits five immaculate cases and drops the sixth because it involved an off-duty officer has damaged the project more than one who submits nothing.

---

## 2. Where the cases actually are

In rough order of yield, based on the 1996–2013 sweep:

**1. Prosecutor press releases.** District attorneys announce justified-homicide rulings in plain language: *"no charges will be filed against the citizen who shot..."*. These are A-tier, free, and indexed by Google. Search `site:<da-domain> "justified" shooting bystander` for every county in your state.

**2. Local newspaper archives.** The case you're looking for is in a 40,000-circulation daily, not the wire. Most have a searchable archive behind a paywall — that's what the capture rule is for. Your library card may include free access; check before paying.

**3. NIBRS and the Supplementary Homicide Reports.** Justifiable homicide by a private citizen is coded in the data. Pull your state's extract, filter for justifiable homicide with a firearm, then cross-reference against news for the same date. This is the single highest-yield primary source and it is free through the FBI's Crime Data Explorer.

**4. Court records.** A justified shooting that produced a civil suit produces a docket, and dockets are public. Check your state's court portal for wrongful-death filings against the intervener.

**5. Television archives.** Local TV covered these when papers didn't, and the clips are often still up. Note the chyron text and the date — a screenshot is your capture.

**6. Reddit, Facebook groups, local forums.** **Leads only.** Never a source. Useful for finding the name of the bar or the date; useless as evidence.

**7. Existing compilations** (CPRC, NRA, Cato, Wikipedia, this project's own E-tier rows). Also leads. Your job is to replace them with something checkable.

---

## 3. The weekly cadence

Two hours a week, which is what a volunteer actually sustains:

1. **20 min** — one targeted search, rotating: `"justified" shooting [county] [year] bystander`, `concealed carry stopped shooting [state] [year]`, `customer shot gunman [city] [year]`.
2. **40 min** — follow up anything that looks real. Open the article. Save it.
3. **20 min** — capture and archive what you found: `python scripts/capture_source.py S####`.
4. **20 min** — fill the intake form, submit.
5. **20 min** — review someone else's submission (this is the part people skip, and it's the part that makes the data trustworthy).

**Five searches, one case, one review, per week.** Twelve months of that per state is 2,600 searches and — on the pre-2014 evidence — most of the missing cases in the country.

---

## 4. The records request

When the press release doesn't exist and the paper is silent, ask the agency. This template works for police departments, sheriffs and prosecutors:

> **Subject:** Public records request — firearm discharge by a civilian, [date], [location]
>
> Under [your state's public records act], I request:
> 1. Any incident report, offense report or supplemental narrative concerning a shooting on [date] at [location] in which a civilian discharged a firearm at an assailant.
> 2. Any press release, public statement or media advisory concerning the same incident.
> 3. Any prosecutor's determination letter or charging decision concerning the civilian who discharged the firearm.
>
> I request these records in electronic form where available. I am a private researcher and this request is not for commercial purposes. If any portion is exempt, please release the remainder and cite the specific exemption for each redaction.

Send it, log the date, and wait. Agencies answer in 5–30 days depending on state law. **When they answer, capture the response** — a PDF of the email or letter — and enter it as an A-tier source.

---

## 5. The quality bar

Before you submit, ask yourself three questions:

1. **Could a stranger find this exact page in ten years?** If no, capture it.
2. **Is this a citizen?** Off-duty police are not citizens for this purpose. Neither are professional guards. A volunteer with a permit is.
3. **Am I coding what the source says, or what I want it to say?** If the article doesn't say "permit," the field is `unknown`.

Three rejections of your own submissions in a month is a good sign, not a bad one.

---

## 6. What gets a lead removed

- **Fabricating or upgrading a source.** One invented URL ends the project's credibility permanently.
- **Deleting an exclusion.** Excluded records stay in the file with a reason. Always.
- **Self-certifying.** Promoting your own record to `verified` without a second reviewer.
- **Selective coverage.** Dropping counter-cases, or stopping the sweep once you find what you were hoping to find.

The first is unrecoverable. The other three are correctable, and the correction is public — that's the design.

---

## 7. Getting started

1. Claim your state in the issue tracker (one lead per state, listed publicly).
2. Run `python scripts/validate.py` to confirm the repo is clean before you touch it.
3. Do **one** case end to end — search, source, capture, intake, submit — before scaling.
4. Then work backwards from 2026 toward 1996. The recent years are already well covered; the early years are where the missing cases are, and where a volunteer's hour is worth the most.
