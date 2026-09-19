#!/usr/bin/env bash
# Fetch pinned source data (re-run safe)
set -e
mkdir -p data && cd data
[ -d indus_decipher ] || git clone https://github.com/joyboseroy/indus_decipher.git
(cd indus_decipher && git fetch -q --all && git checkout -q cd600349f6d3193a241c3eb87ff80a2a65377efc)
[ -d indus-website ] || git clone https://github.com/yajnadevam/indus-website.git
(cd indus-website && git fetch -q --all && git checkout -q 2434249618b1e74de3f26d28b90dfde093c3dd94)
for p in "lineara.xyz LinearAInscriptions.js 43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a" \
         "linearb.xyz LinearBInscriptions.js 84e0b00ec00292e7afd4f88315dd715b11666efb"; do
  set -- $p   # sparse checkout: only the inscription file, not the 1.9 GB of images
  [ -d "$1" ] || git clone -q --filter=blob:none --no-checkout https://github.com/mwenge/$1.git
  (cd "$1" && git sparse-checkout set --no-cone "$2" >/dev/null && git checkout -q "$3")
done
echo "data ready (add cdliatf_unblocked.atf manually for the CDLI steps)"
