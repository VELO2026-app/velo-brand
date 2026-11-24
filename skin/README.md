# VELO gold -- VELO skin package

The golden look of velo (token generation 2), as data. Values were taken from
velo `frontend/tokens.json` (`deploy-machine` 1b57405e); assets are the files
of `frontend/public/` (icons, `bg/`, `onboarding/`, `fonts/`).

```
primer-package.yaml          schema: 1, contract: "2.2"
tokens/brand.tokens.json     $extensions["velo-skin"]: displayName, shortName,
                             themeColor, backgroundColor, fonts,
                             contrastExceptions, supportEmail
tokens/skin.tokens.json      W3C DTCG values at the paths of velo's
                             frontend/tokens.json (velo.*, bare.font-body)
assets/                      logos, mandalas, favicon, PWA icons;
                             assets/bg/, assets/onboarding/, assets/fonts/
LICENSE                      SIL OFL 1.1 of Marmelad (the shipped font)
```

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
