# Source archiving rule

**Every claim in this dataset must be checkable by a stranger, in ten years, without asking us for help.**

That means two things for every source, and the validator enforces both:

1. **A link** — a permanent URL, recorded in `data/sources.csv`.
2. **A copy** — because links die, paywalls close, and pages change. Every source gets either a Wayback snapshot or a filed capture (PDF or screenshot) in `captures/`.

A source with **neither** a URL nor a filed capture is a validation **error**. The record will not pass CI and cannot be published.

---

## What counts as a filed capture

| Source type | Capture method | Stored as |
|---|---|---|
| Live web page | headless PDF + Wayback Save Page Now | `captures/S0001_2026-11-02_domain.pdf` |
| Paywalled article | full-page screenshot of the visible text **plus** a PDF of whatever renders | `captures/S0001_..._shot.png` |
| Blocked / bot-walled | screenshot of the block page itself (proves the access attempt and date) + archive link if one exists | `captures/S0001_..._blocked.png` |
| Print newspaper, microfilm | phone photo or scan of the page, including the masthead and date line | `captures/S0001_..._scan.jpg` |
| TV / radio broadcast | screenshot of the segment with the chyron, plus the station/timestamp noted in the `notes` field | `captures/S0001_..._tv.png` |
| Court PDF (PACER etc.) | the document itself | `captures/S0001_..._docket.pdf` |
| Police press release, emailed | save the email as PDF, or screenshot with headers visible | `captures/S0001_..._release.pdf` |

**Rule of thumb:** if a reviewer cannot see the same page you saw, the source is not yet archived.

---

## Doing it

One command archives and captures a source:

```bash
python scripts/capture_source.py S0037
```

It will:
- render the page to PDF with headless Chrome/Edge into `captures/`
- ask the Wayback Machine for a snapshot and record the resulting URL
- write `captured_file`, `archive_url` and `captured_at` back into `data/sources.csv`

Batch mode for a whole backlog (slow — Wayback throttles):

```bash
python scripts/capture_source.py --all-missing
```

Skip the archive step when you only need a local copy:

```bash
python scripts/capture_source.py S0037 --no-archive
```

### When the script can't do it

It cannot capture a paywall, a microfilm reel, or a courthouse clerk. In those cases capture manually and set the fields:

```csv
S0037,US-2011-OH-D003,primary,news_retrospective,"Akron Beacon Journal","Spa shooting: bystander fired once",, ,captures/S0037_2026-11-02_scan.jpg,2026-11-02,offline_print,C,"Microfilm, Akron Public Library, reel 14"
```

Note `access=offline_print` — the validator requires a `captured_file` for any non-public source. There is no way to enter a gated source without a copy.

---

## Naming and dates

```
captures/<source_id>_<capture-date>_<domain-or-label>.<ext>
captures/S0037_2026-11-02_akron-beacon-journal.pdf
```

The date is the **capture** date, not the publication date. A page captured twice gets two files; the row records the best one and the notes field records the other.

---

## Why both an archive and a local copy

The Wayback snapshot protects against link rot and is publicly checkable by anyone. The local PDF protects against the archive itself: pages get excluded from Wayback on request, robots rules change, and a snapshot of a paywalled article often captures only the wall. Belt and braces is cheap here — one command, two artefacts.

---

## What this costs, honestly

267 sources in the seed dataset; roughly 20–40 seconds each to archive. That is about three hours of unattended runtime for the current file, and it grows with every submission. Two practical consequences:

- **Archive on submission, not in a batch later.** The backlog is the only part of this project that gets worse with success.
- **Prioritise by tier.** A-tier court records and C-tier news that could vanish get archived first; the 242 E-tier aggregator rows are one URL pointing at one page, so they cost one capture, not 242.

---

## The counter-rule

If a source is archived but no longer says what the record claims it says, the record is **disputed**, not quietly edited. The capture is evidence of what the source said on the date it was taken, and that is exactly why it is kept.
