# velo-brand

The golden VELO brand as data packages of the deploy machine `pridem`
(PRIMER-PROTOCOL 1.9, contract 3 rule 10). No code, no instance values; which
version an instance shows is in its passport. Same layout as `goodo-brand`.

```
skin/     the look -- slot packages.skin of velo (apply: build)
texts/    (later) terminology overlays -- slot texts of velo (FE-133)
seeds/    (later) demo data (BE-232)
```

Each subdirectory carries its own `primer-package.yaml`; ONE tag `vX.Y.Z`
versions them together, and an instance takes this repository by that tag
through `subpath` in the passport (`subpath` is required -- the repository
root is not a package). X.Y.Z is the tag; the first one is not set yet:

```yaml
packages:
  skin: { repo: git@github.com:VELO2026-app/velo-brand.git, version: X.Y.Z, subpath: skin }
```

The repository is private: the machine reads it with its deploy key.

Releases are tags; a released tag is never moved. The format and its checks
are defined by the product: velo `tz-whitelabel.md` §3 / §3.2, engine
`frontend/scripts/lib/skin-package.mjs`.
