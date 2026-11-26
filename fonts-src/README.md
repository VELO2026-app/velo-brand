# VELO Marmelad -- font sources

VELO Marmelad is Marmelad (Cyreal, SIL OFL 1.1) modified and renamed by VELO:
Light, Regular, Medium, Bold. `OFL.txt` is the license of these files; the
copy in `skin/LICENSE` carries the same text.

| File | What |
|---|---|
| `VELOMarmelad-<Face>.sfd` | FontForge source of the face (the editable source) |
| `VELOMarmelad-<Face>.ttf` | the built font; the input of the subset, and the file to install on a machine (Figma, design tools) |
| `OFL.txt` | SIL Open Font License 1.1 with the VELO line |

The package ships subsets, not these files. To rebuild them (needs `uvx`):

```sh
tools/subset-fonts.sh        # fonts-src/*.ttf -> skin/assets/fonts/*.woff2
```

The script pins the tool versions, so the output is the same on every machine.
Run it from this repository, never from a folder that holds untrusted font
archives: it reads fonts as data only.
