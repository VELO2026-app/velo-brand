# VELO gold -- VELO skin package

The golden look of velo (token generation 2), as data. Values were taken from
velo `frontend/tokens.json` (`deploy-machine` 1b57405e); assets are the files
of `frontend/public/` (icons, `bg/`, `onboarding/`). The font is VELO Marmelad
(since 0.3.0, FE-278).

```
primer-package.yaml          schema: 1, contract: "2.4"
tokens/brand.tokens.json     $extensions["velo-skin"]: displayName, shortName,
                             themeColor, backgroundColor, fonts,
                             contrastExceptions, supportEmail
tokens/skin.tokens.json      W3C DTCG values at the paths of velo's
                             frontend/tokens.json (velo.*, bare.font-body)
assets/                      logos, mandalas, favicon, PWA icons;
                             assets/bg/, assets/onboarding/, assets/fonts/
LICENSE                      SIL OFL 1.1 of VELO Marmelad (the shipped font)
                             and the scope of that license
```

## Font: VELO Marmelad (FE-278)

Marmelad, modified and renamed by VELO (SIL OFL 1.1, no reserved font name;
the notice of the modification is in `LICENSE`). Three faces of a four-face
family (Light stays in `fonts-src/` until the app uses it), each a `woff2`
subset of Latin + Cyrillic with the Ukrainian letters (і ї є ґ), the
apostrophes (U+0027, U+2019, U+02BC), the punctuation and symbols the app text
uses, and the currencies ₽ € ₴ (530 code points; kerning and ligatures kept,
TrueType hinting kept in all three).

| File (`assets/fonts/`) | Face | `weight` | Bytes |
|---|---|---|---|
| `velo-marmelad-regular.woff2` | Regular | 400 (preloaded) | 35 552 |
| `velo-marmelad-medium.woff2` | Medium | 500 | 59 036 |
| `velo-marmelad-bold.woff2` | Bold | 700 (preloaded: the heading face) | 61 000 |

- `bare.font-body` names the family `VELO Marmelad`; `fonts` of the brand record
  lists the three faces. velo writes one `@font-face` per face, so a face
  loads when text of its weight is drawn; velo preloads Regular and the face of
  headings and buttons (Bold).
- `velo.fw.medium` = 500 and `velo.fw.bold` = 700 map the app's emphasis steps
  to the Medium and Bold faces; `velo.fw.heading` = `{velo.fw.bold}` puts
  headings, header titles and buttons on Bold (owner, 26.11; the velo core
  keeps them on its medium step, so Goodo (variable Manrope) is unchanged).
- Hinting: Regular carries the TrueType instructions it was built with (the
  same as in 0.2.0 and before); Medium and Bold had none in the sources, so
  `tools/autohint-missing.py` runs ttfautohint on them before the subset. A
  renderer that applies hinting (Chromium on Linux, DirectWrite on Windows)
  then sets all three faces alike, and Regular text sets as it did before.
- The `woff2` files are built, not edited: `tools/subset-fonts.sh` reads the TTF
  files of `fonts-src/` (the SFD files there are the editable source) and
  writes `assets/fonts/`. The metadata of the sources (Bold style bits, the
  VELO copyright line) is set by `tools/patch-font-metadata.py`. `validate-skin`
  allows no other file in the package, so the sources live next to `skin/`, not
  inside it.

## Open (owner / designer decisions)

- **Secondary text.** `velo.text.secondary` (`rgba(76, 101, 137, 0.7)`) on the
  white card `velo.bg.card.solid` is 3.12:1; the contract floor is 4.5:1. Since
  0.1.1 the package carries both tokens and declares the pair in
  `contrastExceptions` of the brand record (contract `2.1`, velo FE-230):
  `validate-skin` warns with the reason instead of failing, down to 3:1. A
  value that clears 4.5:1 stays a designer decision; it would drop the
  declaration.
- **Motion tokens** (`--velo-dur-*` except `dur.pulse`, and `--velo-shift-page`)
  are not carried: they are product motion, not brand, and the core's values
  are the golden ones. Since velo FE-230 a skin may set them; the product's
  reduced-motion rule still wins.
- The maskable icon's 80% safe zone is a manual check (as for any skin).

## Check

From velo's `frontend/`: `node scripts/validate-skin.mjs <this dir>`, then
`pnpm skin <this dir> && pnpm build`. To prove "same as golden": build with and
without the package and run `sh e2e/visual/run.sh <dist-without> <dist-with>`.
