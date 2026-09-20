# Roadmap: making sense of the Mohenjo-daro texts

Working model (FINDINGS 6, 11-13):
**[opener unit] + [name-like core, often with a small count] + [pre-final + jar] + (closer)**

## A. Pin down the slots (data we have)
1. ~~Sub-structure of the core~~ (FINDINGS 17: last unit not a title set; it
   pairs with the ending).
2. ~~Opener choice~~ (FINDINGS 17: openers interchangeable; opener fills the first
   core slot).
3. ~~Counts inside cores~~ (FINDINGS 17).
3a. ~~Two-part endings~~ (FINDINGS 17: open set; the ending sign is the fixed part).
3b. ~~First slot without opener~~ (FINDINGS 17: open; openers are an optional prefix).
3c. ~~Space limit~~ (FINDINGS 17: no; a conventional ~5-sign length instead).
3d. ~~Ending as counted item~~ (FINDINGS 17: yes for the arrow G520 with 2 or 3).
3e. ~~"2/3 + arrow" across sites~~ (FINDINGS 18: "3 + arrow" is a seal ending that
    replaces the jar at both MJ and Harappa).

## B. Context the texts lack (manual data)
4. ~~Find-spots joined to texts~~ - done a different way: features coded from the plate
   photographs instead of a CISI concordance (FINDINGS 21-22). ~~widen the depth contrast~~ done
   (FINDINGS 22: four bands over ~26 ft; texts stable, seal shapes change). Done since: space tests, stroke-group
   numerals, and the two flagged corrections (FINDINGS 23). Fish and arrow signs are not
   reliably readable at this resolution. Remaining: more coded seals per group (~94
   needed for a 20-point test), which is the only route to sharper results.
4-old. Find-spots: parser for Mackay (1938) is built and tested (`parse_mackay.py`,
   `findspots.py`). Still needed:
   a. the report's OCR text in `data/mackay1938_vol1.txt` (link in README);
   b. a CISI <-> Mackay number concordance (CISI vol. 1), transcribed into
      `data/concordance_cisi_mackay.csv` - the real bottleneck;
   b2. ~~hand transcription of Mackay's seal table~~ (done, FINDINGS 19).
   b3. IN PROGRESS: link Mackay numbers to CISI texts through the plates. Plate LXXXII
      (Nos. 687-704) received at full resolution and readable; workflow in
      transcriptions/mackay1938_plates/. Remaining: plates LXXXIII onwards
      (IIIF indices ~178-211).
   b3-old. Link Mackay numbers to CISI texts through the plates. Plates confirmed to use
      Mackay's own numbers (FINDINGS 21), so the link only needs sign readings. Two
      routes: (i) higher-resolution plate images (Archive JP2 originals) for full
      readings; (ii) coarse features from the current scan (sign count, motif, a few
      distinctive signs) plus the size/type filter, which leaves ~10 candidates alone
      (FINDINGS 20);
   c. later, the same for Marshall (1931), which covers the 1922-27 seasons.
5. More MJ-type seals abroad (Gulf, Mesopotamia) from excavation reports.

## C. Stronger models
6. Stricter near-duplicate grouping, then an HMM with sign-shape features. Also re-run the
   distance-decay curve (FINDINGS 32a, `conditioning_shape.py`) under this stricter
   grouping: distance 5 already draws on a minority tail of longer texts (now printed
   alongside each result, per external review), and if the non-first-order result holds up
   there too, it is the strongest claim in the note and should be said so explicitly.
7. Merge the three corpora through the concordances, weighting disagreements.

## C2. Line and object structure (after FINDINGS 24)
9. ~~Second lines modelled explicitly~~ done (FINDINGS 34). Remaining: which object types
   carry two lines (M77 records object type as "unknown"), which needs CISI or the plates.
10. ~~Faces from the plates~~ - not possible: Mackay illustrates one face per seal, and
   the CISI file here holds only "A" faces. Two-sided seals are countable (types C and D,
   33 of 701) but their reverse texts need the CISI volumes or museum photographs.
11. Check whether the sign before the arrow (jar variant / "two" / fish) varies with the
   main text, the animal, or the find-spot.

## C3. Reliability
12. ~~Double-coding~~ done (FINDINGS 25: kappa 0.89 for jar endings, sign counts good to
   within one). Still open: coding by a second person, which is the only test of accuracy
   rather than consistency.

## D. Write-up
8. A methods paper: template, two count systems, seal-legend comparison,
   typology - each claim tied to a script and log.
