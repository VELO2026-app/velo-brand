# velo-brand

The golden VELO brand as data packages of the deploy machine `pridem`
(PRIMER-PROTOCOL 1.9, contract 3 rule 10). No code, no instance values; which
version an instance shows is in its passport. Same layout as `goodo-brand`.

```
skin/       the look -- slot packages.skin of velo (apply: build)
texts/      (later) terminology overlays -- slot texts of velo (FE-133)
seeds/      (later) demo data (BE-232)
fonts-src/  sources of the VELO Marmelad fonts (TTF, SFD, OFL.txt); not part of
            any package
tools/      subset-fonts.sh -- builds skin/assets/fonts/*.woff2 from fonts-src/
```

Each subdirectory carries its own `primer-package.yaml`; ONE tag `vX.Y.Z`
versions them together, and an instance takes this repository by that tag
through `subpath` in the passport (`subpath` is required -- the repository
root is not a package). X.Y.Z is the tag: v0.1.0 (contract 2.0, any velo
with skin contract 2.x), v0.1.1 (contract 2.1, velo with FE-230 and later),
v0.2.0 (contract 2.2, velo with FE-251 and later), v0.3.0 (contract 2.4, velo
with FE-278 and later: the weight tokens `velo.fw.*` and the preload of the
regular face only):

```yaml
packages:
  skin: { repo: git@github.com:VELO2026-app/velo-brand.git, version: X.Y.Z, subpath: skin }
```

The repository is public; the machine reads it with the deploy key of its
passport, velo CI clones it over https (the skinned bundle budget, FE-230).

Releases are tags; a released tag is never moved. The format and its checks
are defined by the product: velo `tz-whitelabel.md` §3 / §3.2, engine
`frontend/scripts/lib/skin-package.mjs`.
