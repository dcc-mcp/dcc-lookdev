# DCC LookDev

Cross-DCC workflow skills for repeatable PBR presentation and review.

The first package, `lookdev-turntable`, builds a fixed calibration stage around
one rotating subject: visible HDRI environment, measured ColorChecker, 18%
gray sphere, chrome sphere, fixed camera/exposure, and a verified turntable
render.

The package contains workflow contracts only. It reuses typed tools supplied by
the active DCC adapter and does not bundle third-party charts, HDRIs, or models.

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
