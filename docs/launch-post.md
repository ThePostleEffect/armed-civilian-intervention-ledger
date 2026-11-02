# Two of sixty-one

*Launch post for the Armed Civilian Intervention Ledger. Draft — 2 November 2026.*

---

In July 2022, a 20-year-old walked into the food court of a mall in Greenwood, Indiana, and killed three people. Fifteen seconds later, a 22-year-old named Elisjsha Dicken — carrying a handgun he was licensed to carry — shot him dead from forty yards away.

The wire coverage that week quoted a number. Reuters, citing the FBI's active-shooter report: *"It is rare for a bystander to stop an 'active shooter' attack in the United States... only two out of 61 such attacks last year ended when 'citizens engaged the shooter.'"*

Two out of sixty-one. Three per cent. That number did real work in the days after Greenwood. It is also not a measurement of how often armed civilians stop attacks. It is a measurement of how often the FBI's coding scheme recorded a civilian as the final, terminal cause of an attack's end — which is a different and much narrower thing.

This post is about the gap between those two things, and about a project to close it.

## One code per attack

The federal data — the FBI's annual reports, built on the ALERRT Center's Active Attack Data — records a single resolution for each incident. Across 634 attacks from 2000 to 2025, the largest single category is **"Fled": 198 attacks, 31%.**

There is no field that records *why* the attacker fled.

That absence is not a conspiracy. It is a research dataset doing what it was designed to do, which is describe how incidents end, not attribute cause. The FBI says as much: its data is "not intended to explore all active shooting incidents but rather to provide a baseline understanding."

But a baseline is not a verdict, and it is being quoted as one.

Consider Clackamas Town Center, Oregon, December 2012. A concealed-carry permit holder named Nick Meli drew his pistol, took aim at the shooter, and held fire because of the crowd behind him. The shooter broke off the attack, ran into a stairwell and shot himself.

In the federal data, that event appears as **"Suicide before police arrival."** No indication that a civilian was present, armed, or decisive. Nothing in the record is false. The record simply cannot hold the fact.

Do that 198 times and you get a dataset that systematically undercounts civilian intervention — not through bias, but through schema.

## The number five

For 2000–2013, the FBI's founding study identified five incidents in which "armed individuals who were not law enforcement personnel exchanged gunfire with the shooters." Five, out of 160 attacks. That is the figure that gets cited as proof that armed citizens are statistically irrelevant.

Look at what the five actually were. One was a bar patron in Winnemucca, Nevada. One was a volunteer at a church in Colorado Springs — Jeanne Assam, a private citizen with a concealed-handgun permit, on her church's unpaid security team — who shot the gunman as he came through the door. The rest were armed guards: an airport, a museum, a school board meeting.

**At most two of the five were private citizens.** The published category — "armed individuals who were not law enforcement" — is accurate. The public reading of it, "citizens," is not.

There is a second problem with the same five. A volunteer with a permit gets filed under "security," and the citizen column shrinks accordingly. In the 2000–2013 data, armed guards outnumber citizens four to one among the people who intervened. Some of that is real — guards are posted where attacks happen. Some of it is a filing decision.

## What we found when we looked

Nobody has published an incident-level inventory for 1996–2013. So we built one: four parallel sweeps across 1996–1999, 2000–2006, 2007–2010 and 2011–2013, using local newspaper archives, wire copy, prosecutor statements and court reporting, with strict criteria — public attack, private citizen, lawfully possessed firearm, and *any* mechanism of stopping including flight and surrender.

Nine cases in eighteen years. Pearl High School in 1997, where an assistant principal held the shooter at gunpoint as he tried to drive away. Edinboro in 1998, where a restaurant owner chased a 14-year-old down with a shotgun and talked him into dropping it. A courthouse square in Tyler, Texas in 2005. New Life Church. Winnemucca. And four in 2012 alone: a church in South Carolina, an RV park in Texas, a bar in Pennsylvania, a mall in Oregon.

Seven of those nine fall inside 2000–2013 — the period where the federal count is five, at most two of them citizens.

We also found eight cases that are cited constantly on both sides of this argument and **do not qualify**: Appalachian School of Law (both armed students were serving police officers), Trolley Square (off-duty officer), the AT&T store in New York Mills (off-duty officer), the Mayan Palace theater (off-duty deputy), the Holocaust Museum and the Panama City school board (professional security), Sullivan Central High (a school resource officer). They are in the dataset as exclusions, with reasons, because a list that only contains the cases you like is not evidence.

## The honest version of the numbers

| What is counted | Window | Count |
|---|---|---|
| Citizens who shot the attacker, federal series | 2000–2025 | **15** (2.4% of 634 attacks) |
| Same, adding armed security and off-duty police | 2000–2025 | **29** |
| Documented armed-civilian stops, any mechanism | 2014–2025 | **225** |
| Same, widest definition | 2014–2025 | **271** |
| Independent sweep | 1996–2013 | **9** |
| **30-year total, broad definition** | 1996–2025 | **≈234–280** |

Roughly **28%** of these attacks were ended by an armed civilian, measured against everything the two datasets together identify — with the range running from 2.4% to 37% depending almost entirely on how the denominator is drawn.

That is the finding. Not "the Second Amendment solves mass shootings." The finding is that the number in circulation is off by roughly an order of magnitude, and the error is traceable to specific coding decisions that anyone can inspect.

## What this project does not claim

Three things, stated plainly, because a dataset that only points one way is a pamphlet:

**Unarmed civilians end more attacks than armed ones.** Sixty attacks in the federal data were stopped by people physically subduing the attacker with no firearm at all, against fifteen where a civilian shot him — four to one. Any argument that armed citizens are the decisive civilian response has to get past that number.

**Nothing here establishes causation.** There is no finding in this data that more carry produces fewer deaths. The econometric literature on right-to-carry is genuinely contested and this project does not settle it.

**The share is contested and definition-dependent.** 2.4% and 37% are both defensible and neither settles what people actually want to know, which is whether an armed civilian was *present* when an attack began.

## Why it's open source, and why it deletes nothing

The dataset lives at **[github.com/ThePostleEffect/armed-civilian-intervention-ledger](https://github.com/ThePostleEffect/armed-civilian-intervention-ledger)**. Every record carries its sources; every source carries a link or a filed PDF; every exclusion is logged with a reason and stays in the file.

Three rules make it auditable rather than merely public:

1. **An aggregator is not a source.** "Organisation X says it happened" is a lead. The record is the article or the court document.
2. **Two reviewers, one of whom did not do the research.** Self-certification is how volunteer datasets die.
3. **Counter-cases are required.** Intervener shot, bystander hit, weapon taken, attack not stopped — all kept, or the project can't publish a risk rate, and the risk rate is the most useful thing it could contribute.

Here is our own seed data failing the test, in public: **267 source rows, 12 unique URLs.** The entire 2014–2025 block rests on one aggregator page that has not been verified case by case. That is exactly the weakness this project exists to fix, and it is sitting in our own `data/sources.csv` in plain text where anyone can see it.

## The ask

We need one person per state. Two hours a week:

- 20 minutes: one targeted search — `"justified" shooting [county] [year] bystander`, or a county prosecutor's press-release feed
- 40 minutes: follow up anything real, open the article, save it
- 20 minutes: archive it (`python scripts/capture_source.py S0037`)
- 20 minutes: submit it
- 20 minutes: review someone else's submission — the step everyone skips and the one that makes the data worth having

The early years are where the cases are missing, and where an hour of a volunteer's time is worth the most. Start at 1996 and work forward, or take 2011 — either way, claim a window and finish it, including the years where you find nothing. A documented null is a result.

## Check us in ten minutes

You don't have to take any of this on trust:

1. Open `data/cases.csv` and sort by `confidence`. Fifteen records are B (official dataset). Two hundred and forty-two are E — leads we have not verified.
2. Open `data/adjudication_log.csv` and read what we threw out.
3. Run `python scripts/validate.py`. It will fail if a source has no link and no capture.
4. Pick a record marked `verified`, open its source, and see whether it says what we claim.

If it doesn't, open an issue. Corrections are logged, the record changes, and the correction stays visible. That is the entire mechanism, and it works in both directions — including against us.

---

*The Armed Civilian Intervention Ledger is independent research. Not affiliated with the FBI, ALERRT, the Crime Prevention Research Center, or any advocacy organisation. Data CC BY 4.0, code MIT.*

---

## Appendix: short version (thread)

1. Reuters, July 2022: "only two out of 61" active-shooter attacks last year ended when citizens engaged the shooter. That number is not a count of civilians stopping attacks. It's a count of one coding decision. 🧵

2. The federal dataset records one resolution per attack. Largest category: "Fled" — 198 of 634 attacks, 31%. There is no field for *why* they fled. A civilian who draws and the attacker runs is coded as a flight, not an intervention.

3. Clackamas 2012: a permit holder drew on the shooter, who broke off and shot himself. In the federal data that appears as "Suicide before police arrival." Nothing false. The schema just can't hold it.

4. The famous "5 incidents, 2000–2013" — at most two were private citizens. The rest were armed guards. The category is "armed individuals who were not law enforcement." People read "citizens."

5. We swept 1996–2013 properly. Nine civilian interventions in 18 years. Seven of them inside the period where the federal count is five, and at most two of those were citizens.

6. Widest documented count for 30 years: ~234–280. Strict federal count: 15. Roughly 28% on the widest reading. The spread is the denominator, not the facts.

7. What we don't claim: unarmed civilians stop 4x as many attacks (60 v 15). No causal claim. Share is contested.

8. Everything is open, every source has a link or a filed PDF, every exclusion is logged with a reason: github.com/ThePostleEffect/armed-civilian-intervention-ledger — one volunteer per state.
