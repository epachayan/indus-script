#!/usr/bin/env bash
# Rebuild every intermediate, table and finding. Logs go to work/logs/.
set -e
cd "$(dirname "$0")"; mkdir -p work/logs outputs; cd work
for s in extract features cluster finalize motif motif_dedup site objtype functional crosscheck g400 finalize2 \
         abroad mj_segment mj_subst m77 numerals stock size_tab robust mj_motif refine rename_families export_ml ml_sequence align_cisi align_m77 neural_nextsign mj_core count_arrow build_mackay_table mackay_context mackay_spatial match_feasibility test_numbering_offset phase_test neighbourhood_test numeral_test object_parts recode_agreement build_marshall_table marshall_test constraint_miner affix_test slot_tests slot_followups conditioning_compare conditioning_shape length_control two_register astral_test minimal_pairs_test; do
  echo "== $s"; python3 ../scripts/$s.py > logs/$s.log 2>&1 || { echo "FAILED: $s (see work/logs/$s.log)"; exit 1; }
done
if [ -f ../data/cdliatf_unblocked.atf ]; then
  echo "== proto_elamite"; python3 ../scripts/proto_elamite.py > logs/proto_elamite.log 2>&1 || { echo "FAILED: proto_elamite"; exit 1; }
  for c in seal_legends name_slot numbered_titles typology; do
    echo "== $c"; python3 ../scripts/$c.py > logs/$c.log 2>&1 || { echo "FAILED: $c"; exit 1; }
  done
else echo "(skipping CDLI steps: data/cdliatf_unblocked.atf not found)"; fi
if [ -f ../data/tla_egyptian_earlier.jsonl ]; then
  echo "== determinative_test"; python3 ../scripts/determinative_test.py ../data/tla_egyptian_earlier.jsonl > logs/determinative_test.log 2>&1 || echo "FAILED: determinative_test"
  echo "== egyptian_labels"; python3 ../scripts/egyptian_labels.py ../data/tla_egyptian_earlier.jsonl > logs/egyptian_labels.log 2>&1 || echo "FAILED: egyptian_labels"
else echo "(skipping Egyptian label step: data/tla_egyptian_earlier.jsonl not found)"; fi
if [ -f ../data/tla_egyptian.jsonl ]; then
  echo "== egyptian_compare"; python3 ../scripts/egyptian_compare.py ../data/tla_egyptian.jsonl > logs/egyptian_compare.log 2>&1 || echo "FAILED: egyptian_compare"
else echo "(skipping Egyptian step: data/tla_egyptian.jsonl not found)"; fi
if [ -f ../data/marshall1931_vol2.pdf ]; then
  echo "== parse_marshall_table"; python3 ../scripts/parse_marshall_table.py ../data/marshall1931_vol2.pdf > logs/parse_marshall_table.log 2>&1 || echo "FAILED: parse_marshall_table"
else echo "(skipping Marshall step: data/marshall1931_vol2.pdf not found)"; fi
if [ -f ../data/mackay1938_vol1.txt ]; then
  for c in parse_mackay findspots; do
    echo "== $c"; python3 ../scripts/$c.py > logs/$c.log 2>&1 || { echo "FAILED: $c"; exit 1; }
  done
else echo "(skipping find-spot steps: data/mackay1938_vol1.txt not found)"; fi
echo "done: outputs/ and work/logs/"
