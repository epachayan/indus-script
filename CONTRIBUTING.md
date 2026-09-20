# Contributing

The most useful contributions, in order:

1. **A second coder.** `transcriptions/mackay1938_plates/photo_codings.csv` was coded by one
   person. An independent coding of even 50 seals would convert our reliability figure from
   consistency into accuracy. The plate images are free (see REPRODUCING.md).
2. **CISI volume 1** (Joshi & Parpola 1987). It carries the Mackay-to-CISI concordance and
   publishes both faces of two-sided seals, which would unlock two questions this project
   could not answer.
3. **Corrections to the transcriptions.** Both seal tables were read by eye. Errors are
   likely; each folder's NOTES.md lists the anomalies found so far, including printing
   errors in the books themselves. Please cite the printed page when reporting one.
4. **Marshall vol. III plates and Vats (1940) on Harappa**, to extend the coded corpus to a
   second excavation and a second city.

Please keep the repo's habit of marking retired and corrected results in place rather than
deleting them: `docs/STATUS.md` records the status of every finding.

## Cutting a release

1. Update `CHANGELOG.md` with a dated entry naming what changed - a correction or
   retraction should be named explicitly, not buried in a general "fixes" line.
2. Bump the `version` in `CITATION.cff`.
3. Confirm the `doi:` field in `CITATION.cff` and the DOI badges in `README.md` are already
   present on `main` before tagging - not after. The archived snapshot behind a Zenodo
   version should state its own DOI; landing the badge commit after the tag means the
   frozen artifact contradicts the record about it.
4. Tag, then push the tag.

## When does a new Zenodo version get cut?

The concept DOIs (10.5281/zenodo.22852769 for the dataset, 10.5281/zenodo.22852774 for the
preprint) always resolve to the latest version, so a citation made before a new version
stays valid after it - adding a version extends the chain, it does not fragment the record.
That means new versions are cheap to justify but not free to produce (each one needs a
review pass and, for the preprint, a rebuilt PDF), so the following rule decides when one is
warranted rather than relying on judgement each time:

> A new Zenodo version is cut only when (a) a reported result changes, is retracted or is
> added, or (b) a dataset gains or loses rows. Wording, formatting, typos, version strings,
> CI configuration and repository hygiene accumulate on `main` and ride along with the next
> qualifying release.
