#!/usr/bin/env python3
"""Validate the ACI ledger: cases + sources, against the schema and the protocol.

Usage:
    python scripts/validate.py [data/cases.csv] [data/sources.csv]

ERRORS  - enum/format violations, missing sources, sources with neither a URL nor a filed capture,
          verified records without an A/B/C source, gated sources with no capture.
WARNING - duplicates, web sources not archived, captures referenced but not on disk.

Exit 0 = clean, 1 = errors. Pure stdlib.
"""
import csv, re, sys, collections, datetime, os

STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
VENUES = {"retail","bar_restaurant","place_of_worship","school","workplace","outdoors","residence","government","other",""}
STATUS = {"candidate","verified","disputed","excluded"}
CONF = set("ABCDE")
INTERVENER = {"civilian","volunteer_security","professional_security","off_duty_police","on_duty_police","unknown","citizen_claimed"}
LEGAL = {"permit_holder","constitutional_carry","lawful_ownership_unknown_carry_status","prohibited_person","illegally_carried","claimed_legal","unknown"}
MECH = {"shot_attacker","held_at_gunpoint","disarmed_physically","fled_after_confrontation","surrendered","no_effect","unknown"}
PREVENT = {"yes","no","unknown","contested"}
STYPE = {"court_record","police_report","prosecutor_statement","coroner_report","nibrs_extract","official_dataset",
         "news_contemporaneous","news_retrospective","broadcast","secondary_compilation","social_post","other"}
ACCESS = {"public","paywalled","blocked","offline_print","broadcast"}
REL = {"primary","corroborating","contradicting"}

def check_case(row):
    errs = []
    rid = row.get("incident_id") or "?"
    def e(m): errs.append(f"{rid}: {m}")
    if not re.fullmatch(r"US-\d{4}-[A-Z]{2}-[A-Z]\d{3}", row.get("incident_id","")):
        e("incident_id does not match US-YYYY-ST-Pnnn")
    if row.get("status") not in STATUS: e(f"status invalid: {row.get('status')!r}")
    if row.get("confidence") not in CONF: e(f"confidence invalid: {row.get('confidence')!r}")
    if row.get("state") not in STATES: e(f"state invalid: {row.get('state')!r}")
    if not row.get("city"): e("city empty")
    if row.get("venue_type") not in VENUES: e(f"venue_type invalid: {row.get('venue_type')!r}")
    if row.get("intervener_type") not in INTERVENER: e(f"intervener_type invalid: {row.get('intervener_type')!r}")
    if row.get("firearm_legal_status") not in LEGAL: e(f"firearm_legal_status invalid: {row.get('firearm_legal_status')!r}")
    if row.get("mechanism") not in MECH: e(f"mechanism invalid: {row.get('mechanism')!r}")
    if row.get("prevented_further_deaths") not in PREVENT: e("prevented_further_deaths invalid")
    try:
        d = datetime.date.fromisoformat(row.get("date",""))
        if row.get("year") and row["year"] != str(d.year): e("year does not match date")
    except Exception:
        e(f"date unparseable: {row.get('date')!r}")
    return errs

def check_source(s, case_by_id):
    errs, warns = [], []
    sid = s.get("source_id") or "?"
    def e(m): errs.append(f"{sid}: {m}")
    if not re.fullmatch(r"S\d{4}", sid): e("source_id must be S0001 format")
    if s.get("source_type") not in STYPE: e(f"source_type invalid: {s.get('source_type')!r}")
    if s.get("access") not in ACCESS: e(f"access invalid: {s.get('access')!r}")
    if s.get("relationship") not in REL: e(f"relationship invalid: {s.get('relationship')!r}")
    if s.get("tier") not in CONF: e(f"tier invalid: {s.get('tier')!r}")
    if s.get("incident_id") not in case_by_id: e("incident_id does not exist in cases.csv")
    url = (s.get("url") or "").strip()
    cap = (s.get("captured_file") or "").strip()
    if not url and not cap:
        e("SOURCE HAS NEITHER A URL NOR A FILED CAPTURE — record cannot be checked later")
    if url and not url.startswith("http"):
        e(f"url is not a link: {url!r}")
    if s.get("access") in {"paywalled","blocked","offline_print","broadcast"} and not cap:
        e(f"access={s.get('access')} requires a captured_file (screenshot/PDF) under captures/")
    if cap:
        p = os.path.join("captures", cap.replace("captures/",""))
        if not os.path.exists(p): e(f"captured_file not found on disk: {cap}")
    if url and not s.get("archive_url"):
        warns.append(f"{sid}: no archive_url — run Save Page Now and record the snapshot URL")
    return errs, warns

def main():
    cpath = sys.argv[1] if len(sys.argv) > 1 else "data/cases.csv"
    spath = sys.argv[2] if len(sys.argv) > 2 else "data/sources.csv"
    for p in (cpath, spath):
        if not os.path.exists(p):
            print(f"no such file: {p}"); return 1
    cases = list(csv.DictReader(open(cpath, encoding="utf-8")))
    sources = list(csv.DictReader(open(spath, encoding="utf-8")))
    by_id = {c["incident_id"]: c for c in cases}

    errs, warns = [], []
    for c in cases: errs += check_case(c)
    for s in sources:
        e, w = check_source(s, by_id); errs += e; warns += w

    live = {c["incident_id"] for c in cases if c["status"] != "excluded"}
    with_src = {s["incident_id"] for s in sources}
    for i in sorted(live - with_src):
        errs.append(f"{i}: no source rows at all")

    tier_by_inc = collections.defaultdict(set)
    for s in sources: tier_by_inc[s["incident_id"]].add(s["tier"])
    for c in cases:
        if c["status"] == "verified" and not (tier_by_inc[c["incident_id"]] & {"A","B","C"}):
            errs.append(f"{c['incident_id']}: verified but has no A/B/C source")

    seen = collections.Counter((c["date"], (c["city"] or "").lower().strip()) for c in cases if c["status"] != "excluded")
    dups = [k for k, v in seen.items() if v > 1]

    print(f"cases: {len(cases)}   sources: {len(sources)}")
    print("confidence:  ", dict(sorted(collections.Counter(c["confidence"] for c in cases).items())))
    print("status:      ", dict(sorted(collections.Counter(c["status"] for c in cases).items())))
    print("source tiers:", dict(sorted(collections.Counter(s["tier"] for s in sources).items())))
    print(f"filed captures: {sum(1 for s in sources if s.get('captured_file'))}   archived: {sum(1 for s in sources if s.get('archive_url'))}")
    v = [c for c in cases if c["status"] == "verified"]
    print(f"verified: {len(v)}  |  verified citizen interventions: {sum(1 for c in v if c['intervener_type'] in {'civilian','volunteer_security'})}")
    if dups:
        print(f"\npossible duplicates — same date and city ({len(dups)}):")
        for d in dups[:10]: print("   ", d)
    if warns:
        print(f"\nwarnings ({len(warns)}):")
        for x in warns[:10]: print("   ", x)
        if len(warns) > 10: print(f"    ... and {len(warns)-10} more")
    if errs:
        print(f"\nERRORS ({len(errs)}):")
        for x in errs[:30]: print("   ", x)
        print("\nvalidation failed")
        return 1
    print("\nvalidation passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
