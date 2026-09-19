# Relation to prior work

This project was carried out without first reading the literature, deliberately: the aim
was to see what the corpora say when approached from statistics alone. A novelty audit was
run afterwards to find out which results were already known. Most were. This file records
that audit, so no reader mistakes a replication for a discovery.

## Results here that replicate published work
| what we found | who found it first |
|---|---|
| Positional structure; distinct text beginners and enders; statistically significant sign pairs | Yadav, Vahia, Mahadevan, Joglekar, Adhikari, Rao et al., *PLOS ONE* (2010), using the same M77 corpus |
| Inscriptions overwhelmingly unique; strict positional rules; stroke marks as numerals | Kriger & Hunt (2026), analysing the same 179-seal Mohenjo-daro corpus |
| The jar sign and the arrow sign not co-occurring | Mahadevan (2011), who read them as gender markers |
| Multi-line and multi-side inscription structure | Mukhopadhyay (2019, 2023), who works with explicit side-and-line numbering |
| Short and long stroke groups as separate numeral systems | Mahadevan's sign list and subsequent work |
| Indus statistics falling within the range of real writing systems | Rao et al., *Science* (2009), and the debate that followed (Farmer, Sproat & Witzel 2004) |

## Where this project adds something
| contribution | why it is not already in the literature |
|---|---|
| Machine-readable Mackay (1938) and Marshall (1931) seal tables | The books are public domain but the tables are not, as far as we could find, available as data |
| Text features tested against find-spots at Mohenjo-daro | Kenoyer has criticised Indus statistical corpora for drawing on "chronologically mixed contexts"; Jamison & Uesugi (2022) test carving STYLE against chronology, not text structure |
| Held-out validated constraint set | Positional constraints are known; publishing them as machine-readable rules with held-out violation counts is not standard |
| Genre-matched comparisons (Sumerian seal legends, Egyptian title-and-name labels) with size and length corrections | Comparisons usually run against administrative tablets or running text rather than the same genre on the same kind of object |
| Quantified disagreement between digitised corpora (10-20% of sign positions) | Widely known informally; we did not find the figure stated |

## Positions this work does not take
- It offers no decipherment and argues that none is reachable from this evidence: the texts
  are too short (median 4-5 signs), there is no bilingual, and the language is unknown.
- It does not adjudicate the "is it writing?" debate (Rao et al. vs Farmer, Sproat & Witzel).
  Our measures show language-like conditioning, but section 36 shows that high conditioning
  does not by itself imply syntax, which cuts against over-reading such results.
- It neither supports nor refutes the Dravidian hypothesis. Section 28 rules out a prefixing
  profile; it cannot distinguish suffixing morphology from a phrase-final formula.

## Key references
- Farmer, S., Sproat, R. & Witzel, M. (2004) "The collapse of the Indus-script thesis", *EJVS* 11.
- Jamison, G. & Uesugi, A. (2022) "Mohenjo-daro and interregional connections in the Indus Civilization: evidence from inscribed seals".
- Joshi, J. P. & Parpola, A. (1987) *Corpus of Indus Seals and Inscriptions*, vol. 1.
- Kenoyer, J. M., various, on chronologically mixed contexts in Indus corpora.
- Kriger, C. & Hunt (2026) "Positional constraints, sequence uniqueness, and stroke numerals in Indus seal inscriptions from Mohenjo-Daro".
- Mackay, E. J. H. (1938) *Further Excavations at Mohenjo-daro*, 2 vols.
- Mahadevan, I. (1977) *The Indus Script: Texts, Concordance and Tables*; and (2011) on the jar sign.
- Marshall, J. (1931) *Mohenjo-daro and the Indus Civilization*, 3 vols.
- Mukhopadhyay, B. (2019, 2023) on Indus inscriptions as formalised data carriers.
- Rao, R. et al. (2009) "Entropic evidence for linguistic structure in the Indus script", *Science* 324.
- Yadav, N. et al. (2010) "Statistical analysis of the Indus script using n-grams", *PLOS ONE* 5(3).
