# DCC LookDev

Cross-DCC workflow skills for repeatable PBR presentation and review.

The first package, `lookdev-turntable`, builds a fixed calibration stage with a
camera-facing lower-left reference group, visible HDRI environment, measured
ColorChecker, three reference spheres, and one verified 12-second sequence:
rotating subject under fixed lighting, then fixed subject under rotating lighting.

The built-in reference kit also describes an 18% gray sphere, 80% diffuse-white
sphere, chrome sphere, a license-safe digital chart, and nine CC0 HDRI presets.
Large HDR files are downloaded on demand rather than committed to this repository.

The `TT` intent exposes typed HDR recommendations for insect/macro,
character/creature, hard-surface/product, glass/translucent, vegetation, and
environment assets. Every recommendation remains explicitly overridable and
uses neutral PBR validation rules.

The package contains workflow contracts only. It reuses typed tools supplied by
the active DCC adapter and does not bundle third-party charts, HDRIs, or models.

Encoded review media is validated after decode. A technical chart must remain
stable within `2/255` over time and within `4/255` of its display-encoded source.
GIF-style indexed outputs use one sequence palette with reserved chart/reference
entries and no dithering. These display-code checks remain separate from
scene-linear material and 18% gray-sphere measurements.

## Install

```powershell
dcc-mcp-cli marketplace install dcc-lookdev-turntable --dcc unreal
```

## Validate

```powershell
python -c "from dcc_mcp_core import validate_skill; r=validate_skill('skill/lookdev-turntable'); print(r); raise SystemExit(1 if r.has_errors else 0)"
```

## License

MIT-0. Referenced or user-supplied assets retain their own licenses.
