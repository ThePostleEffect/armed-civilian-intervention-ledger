## What this PR does

<!-- one or two lines -->

## Records added or changed

| Incident ID | Change | Confidence | Second reviewer |
|---|---|---|---|
|  |  |  |  |

## Sources

- [ ] Every source has a URL **or** a filed capture in `captures/`
- [ ] Every web source has an `archive_url` (Wayback snapshot)
- [ ] Gated sources (paywalled / blocked / print / broadcast) have a capture on disk
- [ ] No aggregator is being used as a primary source

## Validation

```
$ python scripts/validate.py
```

<!-- paste the output. CI runs this too, but paste it so reviewers can see the tier counts. -->

## Checklist

- [ ] One incident per row; no merged events
- [ ] `intervener_type` reflects what the source establishes, not what I assume
- [ ] Counter-cases (`mechanism=no_effect`) are included where they exist
- [ ] Exclusions are logged in `data/adjudication_log.csv`, not deleted
- [ ] I am not the second reviewer on my own records
