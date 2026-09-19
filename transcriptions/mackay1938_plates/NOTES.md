# Mackay (1938) vol. II seal plates - readings and matches

Source: Internet Archive item in.gov.ignca.9954, full-resolution page images
(https://iiif.archive.org/iiif/in.gov.ignca.9954$<index>/full/full/0/default.jpg).
Plate LXXXII = PDF page 178 (IIIF index 177) and holds Nos. 687-704 (DK-H and SD areas);
Nos. 1-686 are on the following plates.

Key facts
- The plates number each photograph with Mackay's own seal numbers, so every photo is
  already tied to a find-spot, level and phase via outputs/mackay_seal_table.csv.
- Plate LXXXII shows SEALS (mirror image of the text); other plates are headed
  "Impressions of seals" and read the same way round as the corpus. Mirror before
  comparing where needed.
- At ~4855 x 6782 px per page the signs are legible; the 300 dpi PDF is not.

Workflow (scripts/plate_candidates.py)
1. Read the sign count (and any clear signs) from the photo.
2. Run `python3 plate_candidates.py <mackay_no> <n_signs> [tol_mm]`: filters CISI
   Mohenjo-daro texts by sign count and by seal size (calibrated: scale 1.015,
   offset -0.5 mm) and renders each candidate's signs in impression order.
3. Compare the rendered candidates with the photo and record the match here.

matches.csv columns: mackay_no,cisi,confidence,n_signs,note

## Automatic segmentation (scripts/plate_segment.py)
Input: a full-resolution plate scan (IIIF `full/full`, ~4855 x 6782 px).
Output: one PNG per seal plus `boxes.json` (photo box + the printed number read by OCR).

Plate contents (important)
- Plates LXXXIII-LXXXIX carry seals Nos. 1-378, all "Upper Levels".
- Plates XC-XCII are amulets and start their own numbering at 1: not seals.
- Plates XCIV-XCIX (pp.202-212) carry seals 379-686, all "Lower Levels".
- Plate XCIII (p.200) is copper tablets (drawings), numbered separately.
- The photographic coverage of Nos. 1-704 is therefore complete.
- Plate LXXXII (Nos. 687-704) covers the DK-H trench and the SD area.

Working method (OCR of the printed numbers fails: the digits are hand-lettered)
1. `plate_labels.py <plate.jpg> <dir>` extracts every printed number into a grid image.
2. Read the grid by eye, write `{label index: seal number}` into readings.json.
3. `plate_assign.py <plate.jpg> <dir> readings.json` attaches them to the photo boxes
   (assignment by distance) and writes assigned.json.
4. Spot-check with a verification sheet before using the result.

Status per plate
- LXXXII  (p.178, Nos. 687-704): 18 photos located by hand; SEALS, so mirror before reading.
- LXXXIII (p.180, Nos. 1-52): 54 photo regions found, 26 numbers read reliably
  (`plate_LXXXIII_boxes.json`). Remaining numbers need a visual pass.
- LXXXIV-LXXXVII (pp.182-188, Nos. 53-271): scans received, not yet segmented.
- LXXXVIII (p.190, Nos. 272-333): 63 photos found, 43 numbers read and assigned
  (`plate_LXXXVIII_assigned.json`). Spot check: No. 287 looks wrong, recheck.
- LXXXIX (p.192, Nos. 334-378): segmented, numbers not yet read.
- XCIV (p.202, Nos. 379-430): 59 photos, 47 numbers read and assigned
  (`plate_XCIV_assigned.json`).
- XCV-XCIX (pp.204-212, Nos. 431-686): segmented, label grids generated,
  numbers not yet read.

What did not work
- Assigning numbers by reading order: the plates are laid out by seal size, not by number
  (agrees with only 6 of 26 OCR labels), so each number must be read from the page.
- OCR of the printed numbers is ~50% reliable; numbers read twice are discarded rather
  than guessed.

Reading the signs still needs a human pass; `plate_candidates.py` narrows each seal to a
shortlist using sign count plus the calibrated size filter.

## Coding the photographs directly (photo_codings.csv)
Rather than matching every seal to a CISI text, features are read straight from the
photographs: number of signs, whether the text ends with the jar, and whether a fish or
arrow sign is present. Each row carries a confidence (high/medium/low); low-confidence
and blank-inscription rows are excluded from tests.

Convention: on an impression the reading runs right to left, so a jar ENDING appears at
the LEFT edge of the photograph.

Sheets come from `plate_sheets.py <plate.jpg> <dir> <n> <start>` (12 seals per sheet).

Depth contrast available with the two plates coded/assigned so far:
- Pl. LXXXVIII (Nos. 272-333): 43 seals, levels -10.8 to -9.4 ft, all "Late III".
- Pl. XCIV (Nos. 379-430): 47 seals, levels -16.8 to -12.0 ft, mostly "Intermediate I".
Coded so far: all 47 of plate XCIV (34 usable). Plate LXXXVIII still to code.

## Coding complete
All thirteen seal plates are coded: 531 seals in photo_codings.csv, 419 with a find-spot.
