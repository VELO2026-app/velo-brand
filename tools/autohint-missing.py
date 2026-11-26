#!/usr/bin/env python3
"""Hint the faces of fonts-src/ that carry no TrueType instructions (FE-278).

  uvx --from ttfautohint-py==0.6.1 --with fonttools==4.69.1 python -I \\
      tools/autohint-missing.py SRC_DIR OUT_DIR

Regular was hinted with ttfautohint when it was built; Light, Medium and Bold
were flattened from outlines afterwards and have no instructions in any glyph
(only the shared fpgm / prep / cvt tables remain). Without instructions a
renderer that applies hinting (Chromium on Linux, DirectWrite on Windows)
rounds Regular's advance widths and grid-fits its outlines, and leaves the
other faces linear: the three would not set alike.

For every VELOMarmelad-*.ttf in SRC_DIR this script writes the file to OUT_DIR:
copied as is when some glyph has instructions, run through ttfautohint with
its default settings (the ones the original Regular was built with) when none
has. The output is what tools/subset-fonts.sh subsets. The sources in
fonts-src/ are not touched. The input fonts are read as data.
"""
import shutil
import sys
from pathlib import Path

import ttfautohint
from fontTools.ttLib import TTFont


def has_instructions(path):
    font = TTFont(path, recalcTimestamp=False)
    glyf = font["glyf"]
    for name in font.getGlyphOrder():
        glyph = glyf[name]
        if glyph.numberOfContours == 0:
            continue
        glyph.expand(glyf)
        if hasattr(glyph, "program") and glyph.program.getBytecode():
            return True
    return False


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for ttf in sorted(src.glob("VELOMarmelad-*.ttf")):
        target = out / ttf.name
        if has_instructions(ttf):
            shutil.copyfile(ttf, target)
            print(f"{ttf.name}: has instructions, copied")
        else:
            ttfautohint.ttfautohint(in_file=str(ttf), out_file=str(target))
            # ttfautohint stamps head.modified with the time of the run; the
            # source's own value keeps the output (and the woff2) reproducible.
            hinted = TTFont(target, recalcTimestamp=False)
            hinted["head"].modified = TTFont(ttf, recalcTimestamp=False)["head"].modified
            hinted.save(target)
            print(f"{ttf.name}: no instructions, autohinted ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
