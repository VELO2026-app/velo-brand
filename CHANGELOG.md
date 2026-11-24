# Changelog

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
