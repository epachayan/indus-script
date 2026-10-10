# Cross-checking the AI transcriptions

The seal tables were transcribed by an AI model reading the page images. These scripts
check that transcription against readers that share none of its machinery, and report
per-field agreement. Agreement measures consistency between readers, not accuracy:
an error every reader shares (a faint digit, a ditto mark) would pass unnoticed.

Readers
1. `read_marshall_tesseract.py` - Tesseract 5, one table cell at a time, with
   per-column character whitelists. Rows are located by projection profiles; columns
   are aligned to page 402 by profile correlation. Uses nothing from the AI output.
2. `outputs/marshall_seal_table.csv` - the repo's earlier whole-line OCR (Tesseract,
   different segmentation and settings), rows whose plate number OCR read cleanly.

Rows are matched by printed position (page, half, row), not by content.

Setup (Windows)
    winget install UB-Mannheim.TesseractOCR
    pip install opencv-python numpy scipy pytesseract

Page images: IIIF item in.ernet.dli.2015.107493, indices 55-58 = printed pp. 402-405,
saved as pages/marshall_p402.jpg ... marshall_p405.jpg.

Run
    python read_marshall_tesseract.py pages out_tess_marshall.csv      (about 10 min on CPU)
    python agreement.py ../../outputs/marshall_seal_table_transcribed.csv out_tess_marshall.csv --out results
    python vote.py ../../outputs/marshall_seal_table_transcribed.csv out_tess_marshall.csv ../../outputs/marshall_seal_table.csv results/vote_marshall.csv

Status categories in vote_marshall.csv
- AI confirmed by 2 OCR / by 1 OCR: an independent reader gives the same value
- AI confirmed by 1 OCR, other OCR differs: majority agrees with the AI
- both OCRs agree, AI differs: candidate AI error, check by eye
- unconfirmed: OCR differs: OCR misread or AI error, undecided
- AI only: no OCR reading for that cell
