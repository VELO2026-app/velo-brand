# VELO gold -- VELO skin package

The golden look of velo (token generation 2), as data. Values were taken from
velo `frontend/tokens.json` (`deploy-machine` 1b57405e); assets are the files
of `frontend/public/` (icons, `bg/`, `onboarding/`, `fonts/`).

```
primer-package.yaml          schema: 1, contract: "2.0"
tokens/brand.tokens.json     $extensions["velo-skin"]: displayName, shortName,
                             themeColor, backgroundColor, fonts
tokens/skin.tokens.json      W3C DTCG values at the paths of velo's
                             frontend/tokens.json (velo.*, bare.font-body)
assets/                      logos, mandalas, favicon, PWA icons;
                             assets/bg/, assets/onboarding/, assets/fonts/
LICENSE                      SIL OFL 1.1 of Marmelad (the shipped font)
```

## Open (owner / designer decisions)

- **Secondary text.** `velo.text.secondary` (`rgba(76, 101, 137, 0.7)`) on the
  white card is 3.12:1; the contract floor is 4.5:1. The package therefore
  leaves `velo.text.secondary` and `velo.bg.card.solid` to the product (same
  values, the gate skips the pair). Before velo drops its built-in look, the
  designer picks a value that clears 4.5:1, or the gate changes.
- **Reduced-motion tokens** (`--velo-dur-*` except `dur.pulse`, and
  `--velo-shift-page`) are not carried: the product re-sets them in its
  `prefers-reduced-motion` block, which a skin's `:root` would override.
- The maskable icon's 80% safe zone is a manual check (as for any skin).

## Check

From velo's `frontend/`: `node scripts/validate-skin.mjs <this dir>`, then
`pnpm skin <this dir> && pnpm build`. To prove "same as golden": build with and
without the package and run `sh e2e/visual/run.sh <dist-without> <dist-with>`.
