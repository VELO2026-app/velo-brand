#!/bin/sh
# Rebuild skin/assets/fonts/*.woff2 from the TTF sources in fonts-src/.
#
#   tools/subset-fonts.sh [SRC_DIR] [OUT_DIR]
#
# SRC_DIR defaults to fonts-src, OUT_DIR to skin/assets/fonts (paths relative
# to the repository root). Needs `uvx` (uv). The tool versions are pinned so
# the output is the same on every machine.
#
# The subset is Latin + Cyrillic with the Ukrainian letters (і ї є ґ, Ґ) and
# both apostrophes (U+0027, U+2019, U+02BC), the punctuation and symbols the
# app text uses, and the currencies ₽ € ₴. Layout features stay (kerning,
# marks, ligatures).
#
# TrueType hinting stays (v0.3.1): a renderer that applies it (Chromium on
# Linux, DirectWrite on Windows) rounds the advance widths of a hinted face, so
# an unhinted Regular sets text slightly differently from the old hinted one.
# Regular comes hinted from the source; Medium and Bold have no instructions
# in the source, so tools/autohint-missing.py runs ttfautohint on them first.
#
# The script reads the fonts as data and writes only into OUT_DIR. It runs
# the tool from an empty temporary directory so nothing from the font
# directory or from the current directory is picked up.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SRC=${1:-$ROOT/fonts-src}
OUT=${2:-$ROOT/skin/assets/fonts}

# Basic Latin, Latin-1, Latin Extended-A, spacing accents and the modifier
# apostrophe; Cyrillic block (Ukrainian included); general punctuation and
# the symbols and currencies used by the app.
UNICODES='U+0020-007E,U+00A0-017F,U+02BC,U+02C6,U+02C7,U+02D8-02DD,U+0400-04FF,U+2010-2015,U+2018-201E,U+2020-2022,U+2026,U+2030,U+2039-203A,U+2044,U+20AC,U+20B4,U+20BD,U+2116,U+2122,U+2212,U+2215,U+2248,U+2264-2265'

# weight name -> output file (the file name is the contract: lower case)
mkdir -p "$OUT"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"

# Light is not shipped until the app uses it (owner, 26.11): its TTF and SFD stay
# in fonts-src/. To ship it again, add Light to the list and to `fonts` of
# skin/tokens/brand.tokens.json (weight 300).
FACES="Regular Medium Bold"
mkdir "$WORK/in"
for style in $FACES; do cp "$SRC/VELOMarmelad-$style.ttf" "$WORK/in/"; done
uvx --from ttfautohint-py==0.6.1 --with fonttools==4.69.1 python -I \
  "$ROOT/tools/autohint-missing.py" "$WORK/in" "$WORK/hinted"

for style in $FACES; do
  lower=$(printf '%s' "$style" | tr 'A-Z' 'a-z')
  uvx --with brotli==1.2.1 --from fonttools==4.69.1 pyftsubset \
    "$WORK/hinted/VELOMarmelad-$style.ttf" \
    --unicodes="$UNICODES" \
    --flavor=woff2 \
    --layout-features='*' \
    --name-IDs='0,1,2,3,4,5,6,13,14' \
    --notdef-outline \
    --output-file="$OUT/velo-marmelad-$lower.woff2"
  printf '%s %s bytes\n' "velo-marmelad-$lower.woff2" "$(wc -c < "$OUT/velo-marmelad-$lower.woff2" | tr -d ' ')"
done
