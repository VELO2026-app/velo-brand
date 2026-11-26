#!/usr/bin/env python3
"""Fix the metadata of the VELO Marmelad sources in fonts-src/ (FE-278 review).

  uvx --from fonttools==4.69.1 python -I tools/patch-font-metadata.py [SRC_DIR]

Idempotent: a second run changes nothing. It touches metadata only; every
glyph, advance width and layout table stays byte for byte as it was.

What it sets, so that the four faces install as ONE family "VELO Marmelad"
(Mac and Figma group by nameID 16 / 17, Windows by nameID 1 / 2 and the
style bits):

  * all faces: the copyright notice (nameID 0, and Copyright: of the .sfd)
    names VELO as the author of the modifications, as OFL.txt does;
  * Bold: OS/2.fsSelection has BOLD (bit 5) and not REGULAR (bit 6),
    head.macStyle has bold (bit 0), and the .sfd says the same
    (StyleMap 0x0020; its MacStyle: 1 was already right).
  * Light, Regular, Medium: only checked -- the weight class, the typographic
    family / subfamily (16 / 17) and the REGULAR style bit are right.

The script reads the fonts as data. Run it from this repository, never from a
folder that holds untrusted font archives.
"""
import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

VELO_LINE = "Copyright 2026 VELO."
FACES = {  # face -> (usWeightClass, typographic subfamily, legacy subfamily)
    "Light": (300, "Light", "Regular"),
    "Regular": (400, "Regular", "Regular"),
    "Medium": (500, "Medium", "Regular"),
    "Bold": (700, "Bold", "Bold"),
}
FAMILY = "VELO Marmelad"
BOLD_BIT, REGULAR_BIT = 1 << 5, 1 << 6


def name(font, name_id):
    record = font["name"].getName(name_id, 3, 1, 0x409)
    return record.toUnicode() if record else None


def patch_ttf(path, face):
    weight, typo_sub, legacy_sub = FACES[face]
    font = TTFont(path, recalcTimestamp=False)
    os2, head, names = font["OS/2"], font["head"], font["name"]

    for record in names.names:
        if record.nameID == 0 and VELO_LINE not in record.toUnicode():
            record.string = record.toUnicode().rstrip() + " " + VELO_LINE

    if face == "Bold":
        os2.fsSelection = (os2.fsSelection | BOLD_BIT) & ~REGULAR_BIT
        head.macStyle |= 1
    else:
        assert os2.fsSelection & REGULAR_BIT and not os2.fsSelection & BOLD_BIT, face
        assert head.macStyle == 0, face

    assert os2.usWeightClass == weight, (face, os2.usWeightClass)
    assert name(font, 16) == FAMILY and name(font, 17) == typo_sub, face
    assert name(font, 2) == legacy_sub, face
    assert name(font, 1) == (FAMILY if face in ("Regular", "Bold") else f"{FAMILY} {face}"), face
    assert VELO_LINE in name(font, 0), face

    font.save(path)
    print(f"{path.name}: fsSelection={os2.fsSelection:#010b} macStyle={head.macStyle} "
          f"weight={os2.usWeightClass} 1/2={name(font, 1)!r}/{name(font, 2)!r} "
          f"16/17={name(font, 16)!r}/{name(font, 17)!r}")


def patch_sfd(path, face):
    # The .sfd files use CRLF line endings: read and write bytes, so nothing
    # but the lines below changes.
    text = path.read_bytes().decode("utf8")
    out = re.sub(
        r"^(Copyright: [^\r\n]*?)\.?(?=\r?\n)",
        lambda m: m.group(0) if VELO_LINE in m.group(0) else f"{m.group(1)}. {VELO_LINE}",
        text, count=1, flags=re.M,
    )
    if face == "Bold":
        out = re.sub(r"^StyleMap: 0x0040(?=\r?\n)", "StyleMap: 0x0020", out, count=1, flags=re.M)
        assert re.search(r"^StyleMap: 0x0020\r?$", out, re.M) and re.search(r"^MacStyle: 1\r?$", out, re.M)
    if out != text:
        path.write_bytes(out.encode("utf8"))


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "fonts-src"
    for face in FACES:
        patch_ttf(src / f"VELOMarmelad-{face}.ttf", face)
        patch_sfd(src / f"VELOMarmelad-{face}.sfd", face)


if __name__ == "__main__":
    main()
