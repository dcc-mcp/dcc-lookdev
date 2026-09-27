# `lookdev_sheet` host-run evidence

Status: **not run on a real host** (B-class, non-blocking).

No DCC host, renderer, or GPU was available on the machine that authored this
recipe, so the deliverable is the plan plus the gate that will judge the receipt —
not a recorded run. Nothing below is a synthesized artifact passed off as a real
one.

## What is reproducible today

```bash
python examples/lookdev_sheet/materialize_plan.py --inputs examples/lookdev_sheet/inputs.example.json
```

Resolves `tool_routing` for `--adapter`, applies `inputs_schema` defaults,
substitutes every `${x}` placeholder, and prints the five-step dispatch plan
together with the `undo_steps` and the `output_contract` the receipt will be
validated against. No host is required; it runs in CI.

## What a real run must produce

Dispatch the plan to a live instance in order, then validate the observed receipt
against `skill/lookdev-turntable/RECIPES.yaml` →
`recipes[lookdev_sheet].output_contract`:

| Field | Evidence it carries | Fails when |
|---|---|---|
| `rendered_exr_count` | how many variants actually rendered (≥2) | fewer frames than variants |
| `lighting_variant_count` | how many rigs were staged (2-8) | the rig was never swapped |
| `sheet_sha256` | SHA-256 of the delivered sheet, `^[0-9a-f]{64}$` | the sheet was not written or was truncated |
| `camera_fixed` | `const: true` — the point of the sheet | the camera moved between variants |
| `working_space` | `const: ACEScg` | the render was not scene-linear ACES |
| `output_encoding_count` | `const: 1` | zero or stacked display encodings |

The last three are the `STANDARD.md` gates re-expressed as contract constants, so
a sheet that cannot prove them is rejected rather than merely warned about.

Record here: host and version, the commands in dispatch order, the run log, the
per-variant EXR paths with their `sha256sum`, and the sheet's `sha256sum`. A run
that cannot produce these fields has not delivered the recipe.

## Rollback

`undo` is `manual`: staging a rig and rendering mutates the scene and writes
frames to disk. Remove the frames under `variants_dir` and the sheet at
`sheet_path`, then restore the previous rig or reopen the last saved scene.
