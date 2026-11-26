# Changelog

## 0.3.1

FE-278 (https://linear.app/velo-space/issue/FE-278), owner's decisions 26.11:
headings and buttons of the golden skin are Bold, and the TrueType hinting
comes back. Needs velo with the heading weight token `velo.fw.heading` (velo
PR #240); contract stays `2.4`.

- `skin/tokens/skin.tokens.json`: new `velo.fw.heading` = `{velo.fw.bold}`
  (headings, header titles and buttons use Bold; the velo core keeps its medium
  step, so Goodo does not change). 185 tokens. velo preloads the Regular face
  and the heading face, so the first paint gets Regular and Bold.
- `skin/assets/fonts/`: the subsets keep hinting. 0.3.0 dropped it, and Chromium
  on Linux (the CI Visual job) set Regular text differently from 0.2.0 because
  it rounds the advance widths of a hinted face. Regular carries the
  instructions it was built with (identical to the 0.2.0 file: same
  instructions in all 288 shared glyphs that have any, same fpgm / prep / cvt /
  gasp). Medium and Bold had no instructions in the sources, so
  `tools/autohint-missing.py` runs ttfautohint (ttfautohint-py 0.6.1, default
  settings, `no_info`: name ID 5 stays "Version 1.102") on them first; the
  glyph outlines and widths are untouched.
  Sizes: Regular 23 916 -> 35 552 B, Medium 39 440 -> 58 972 B, Bold 40 712 ->
  60 860 B (0.2.0: one file, 31 868 B). The output is reproducible.
- **Known gap, Medium and Bold.** ttfautohint gives no instructions to 28
  glyphs of the Medium subset and 30 of the Bold subset (Regular: none). They
  render unhinted, so on Linux and Windows they sit on the pixel grid a little
  differently from their neighbours. The ones the app text uses: `! $ K M N Y
  k`, `И Й Ч д и ф` (Bold also `Д Ж`); the rest are rare (`¡ ¢ þ ћ`, Cyrillic
  extensions such as `ү Ҷ ҷ Ҹ ҹ Ӌ ӌ`, Bold also `ѣ Ѫ Җ Һ`). In the sources these
  letters are one dense contour of 330 to 780 points (in Regular: 28 to 44
  points), the outline of a stroke. The fix is in the sources (the `.sfd`
  outlines), not in this package, and is a separate task.
- `tools/subset-fonts.sh` runs the autohint step and no longer passes
  `--no-hinting`.

**Order of release.** A velo without `velo.fw.heading` refuses the token as
unknown, so the package does not build there: the velo PR that raises the pin
carries the token, and that PR is the first to read `0.3.1`.

## 0.3.0

FE-278 (https://linear.app/velo-space/issue/FE-278): the golden skin gets its
own fonts, VELO Marmelad (Regular, Medium, Bold), instead of one
Regular face with a browser-drawn bold. Owner's decision 26.11: weight 600
becomes Medium 500, weight 700 becomes Bold 700. Light is not shipped until
the app uses it (its TTF and SFD stay in `fonts-src/`). Needs
velo with FE-278 (weight tokens `velo.fw.*`, preload of the regular face only);
contract `2.4`.

- `skin/primer-package.yaml`: contract `2.4` (the weight tokens `velo.fw.*`;
  velo FE-278 refuses them in a package that declares less).
- `skin/assets/fonts/`: `marmelad-subset.woff2` (31 868 B) is replaced by three
  subsets, `velo-marmelad-regular|medium|bold.woff2` (23 916, 39 440,
  40 712 B). Latin + Cyrillic with the Ukrainian letters, apostrophes,
  punctuation, ₽ € ₴; hinting dropped.
- `skin/tokens/brand.tokens.json`: `fonts` lists the three faces, family
  `VELO Marmelad`, weights 400 / 500 / 700.
- `skin/tokens/skin.tokens.json`: `bare.font-body` is `VELO Marmelad, Noto Sans,
  sans-serif`; new `velo.fw.medium` = 500 and `velo.fw.bold` = 700. 184 tokens.
- `skin/LICENSE`: the OFL text of VELO Marmelad with the VELO line (modified
  and renamed, 2026); the scope section now names the font subsets.
- `fonts-src/`: TTF and SFD sources of the four faces, `OFL.txt`, a README.
  `tools/subset-fonts.sh` rebuilds the `woff2` files from them.
- Font metadata fixed by `tools/patch-font-metadata.py` (glyphs, widths and
  layout tables untouched; checked against the original files): Bold is now
  flagged Bold (`OS/2.fsSelection` BOLD, not REGULAR; `head.macStyle` bold; the
  `.sfd` `StyleMap` 0x0020), and nameID 0 of all four faces, like the `.sfd`
  `Copyright:`, carries `Copyright 2026 VELO.` Installed from `fonts-src/*.ttf`,
  the four faces form one family "VELO Marmelad" (nameID 16 / 17: Light,
  Regular, Medium, Bold; weight classes 300 / 400 / 500 / 700).

**Order of release.** A velo older than FE-278 refuses `velo.fw.*` as unknown
tokens, so the package does not build there. The contract minor cannot stop
that earlier: an older reader checks the major only (the slot says `>=2,<3`).
From FE-278 on, `validate-skin` requires `2.4` for `velo.fw.*`.
1. Merge the velo FE-278 PR (weight tokens, Regular-only preload, 600 / 700
   replaced by the tokens). The CI pin stays on `v0.2.0`: gold does not change.
2. Merge this PR, then the owner tags `v0.3.0`.
3. A velo PR raises the pin (`.github/brand-skins.json`, `skinned` of
   `frontend/bundle-budget.json`). It changes gold on screen (`visual-change`)
   and grows the gold precache by about 73 KB (`bundle-growth`).
4. The passports move to `0.3.0` after the velo rollout.

## 0.2.0

FE-251 (https://linear.app/velo-space/issue/FE-251): the support address
comes from the brand package. velo no longer carries `support@velo.app`; the
support screens of the user and the master show the address of the brand
record, and no address line without one. Needs velo with FE-251 (contract
`2.2`).

- `skin/primer-package.yaml`: contract `2.2`.
- `skin/tokens/brand.tokens.json`: `supportEmail` `support@velo.app`.

**Order of release: merge the velo FE-251 PR first, then tag `v0.2.0`.** A
velo older than FE-251 refuses `supportEmail` as an unknown field, so the
package does not build there. After the tag, velo raises its CI pin
(`.github/brand-skins.json`) and the passports move to `0.2.0`.

## 0.1.1

FE-230 (https://linear.app/velo-space/issue/FE-230): the package for the
neutral velo core. velo no longer carries a golden look; everything golden
comes from this package. Needs velo with FE-230 (contract `2.1`).

- `skin/primer-package.yaml`: contract `2.1`.
- `skin/tokens/skin.tokens.json`: `velo.text.secondary` (`rgba(76, 101, 137,
  0.7)`) and `velo.bg.card.solid` (`#ffffff`), the golden values. 182 tokens.
- `skin/tokens/brand.tokens.json`: `contrastExceptions` declares the pair
  `velo.text.secondary` on `velo.bg.card.solid` (3.12:1) with its reason;
  `validate-skin` reports it as a warning.

## 0.1.0

FE-229 (https://linear.app/velo-space/issue/FE-229): the golden VELO look of
velo `deploy-machine` (commit 1b57405e) as a skin package, contract `2.0`.

- `skin/tokens/skin.tokens.json`: 180 tokens at their golden values (every
  `velo.*` colour, shadow, radius, size and `bare.font-body`).
- `skin/tokens/brand.tokens.json`: VELO / VELO, `themeColor` `#334D6E`,
  `backgroundColor` `#ffffff`, font Marmelad.
- `skin/assets/`: logos, mandalas, favicon, PWA icons, `bg/background.webp`,
  nine `onboarding/` illustrations, `fonts/marmelad-subset.woff2`
  (Cyrillic + Latin subset, SIL OFL 1.1, text in `skin/LICENSE`).
- Copied byte for byte from velo `frontend/public/`; nothing redrawn.

Not in the package, on purpose (the golden value stays the product's):
- 14 tokens the product re-sets in its `prefers-reduced-motion` block:
  `--velo-dur-press`, `-fast`, `-base`, `-page`, `-page-exit`, `-tab`,
  `-tab-out`, `-tab-in`, `-resize`, `-sheet`, `-sheet-exit`, `-calm`,
  `-calm-long` (all `--velo-dur-*`) and `--velo-shift-page`. A skin's `:root`
  rule comes after that block and would switch reduced motion off.
- `velo.text.secondary` and `velo.bg.card.solid`. The golden pair measures
  3.12:1, under the 4.5:1 gate of `validate-skin`; the gate skips a pair the
  skin does not override. Carrying both would make `pnpm build` fail. This is
  an open design decision (see `skin/README.md`).

Checked against velo `deploy-machine` 1b57405e: `validate-skin` 0 fail, 0 warn;
a build with this package against a build without it: same custom properties,
same CSS rules, same manifests and static assets byte for byte; 19 key screens
of `e2e/visual` pixel-identical. The only difference in `index.html` is the
font preload, which points into `/skin/`.
