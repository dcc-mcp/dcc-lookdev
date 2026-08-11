---
name: lookdev-turntable
description: >-
  Build and verify a standardized PBR LookDev stage with one centered subject,
  a camera-facing lower-left ColorChecker and three reference spheres, a visible HDRI,
  fixed camera/exposure, and one combined subject-then-lighting turntable.
  Use for repeatable material review across supported DCC hosts.
license: MIT-0
compatibility: "dcc-mcp-core 0.19+, typed scene/material/camera/animation/render tools"
allowed-tools: Bash Read Write
metadata:
  dcc-mcp:
    dcc: multi-dcc
    version: "0.3.1"
    layer: domain
    stage: presentation
    tags: [lookdev, pbr, turntable, hdri, color-management, render]
    search-hint: "standard PBR lookdev stage, camera-facing lower-left ColorChecker, three spheres, HDRI, combined subject then lighting turntable"
    tools: tools.yaml
    references:
      - "references/*.md"
---

# LookDev Turntable

Use this Skill after the asset and PBR textures exist. It standardizes presentation;
it does not author the asset, invent chart values, or replace host-owned typed tools.

## Control path

1. Select one live DCC instance with `dcc-mcp-cli list`.
2. For each intent, use `search -> describe/load-skill -> call`.
3. Keep one task session id through setup, preview, render, and validation.
4. If a required typed capability is absent, fix the owning adapter minimally. Do
   not substitute open-ended UI automation or embed host-specific scripts here.

## Stage contract

- `SubjectRoot`: centered on the turntable pivot; rotates only during the first
  half of the sequence and remains fixed during the second half.
- `ReferenceRoot`: camera-space lower-left ColorChecker, 18% gray, 80% diffuse,
  and chrome spheres; never animated and always front-facing to the camera.
- `LightingRoot`: fixed during the first half and the only lighting transform
  animated during the second half.
- `EnvironmentRoot`: visible HDRI backdrop and environment lighting; fixed rotation,
  intensity, and exposure unless its lighting-only transform is owned by
  `LightingRoot`. Keep the visible backdrop fixed when the host can decouple it.
- `CameraRoot`: fixed transform, focal length, focus, and manual exposure.
- Ground: neutral, non-mirrored receiver. It may show contact shadow, not a second
  subject-like reflection.

Use the measured values, framing ratios, and render gates in
[STANDARD.md](references/STANDARD.md). Use
[HOST_ROUTING.md](references/HOST_ROUTING.md) to map the contract to the current
adapter without hard-coding one host's tool slugs.

## Workflow

1. Preflight the mesh, five PBR channels, texture color intent, and manual exposure.
2. Create or reuse a license-safe HDRI and a measured ColorChecker source. Record
   source URLs, licenses, and hashes. Never bundle an unlicensed chart or HDRI.
3. Build the five roots above. Parent only the subject to `SubjectRoot`.
4. Apply the built-in `camera-facing-lower-left-combined-turntable` preset through
   `lookdev_turntable__get_preset`. Its `reference_kit` includes procedural
   three-sphere materials, a license-safe digital chart, an external measured
   chart descriptor, and three CC0 HDRI download descriptors.
5. Author one 12-second, 30 fps sequence. The first 180 output frames inspect
   materials with fixed lighting and `SubjectRoot` rotating linearly 0 to 360
   degrees. The final 180 inspect lighting with the subject fixed and
   `LightingRoot` rotating linearly 0 to 360 degrees.
6. Render preview frames from both halves. Reject overlap, clipping, duplicate
   subjects/reflections, visible light helpers, fallback materials, automatic
   exposure, invalid color transforms, or moving reference objects.
7. Render all 360 frames natively in the DCC, encode one H.264/BT.709 review video,
   and retain the image sequence for pixel-level validation. Do not synthesize
   missing frames with optical flow.
8. Verify first/middle/last frames, frame count, transform ownership, OCIO status,
   and media metadata before reporting success.

Call `lookdev_turntable__validate_stage` with the measured scene/render facts as
the final host-neutral gate. A failed gate is a validation result, not a transport
error; fix the reported contract item and call it again.

## Honest boundaries

- A tone mapper is not an OCIO pipeline. Report host limitations explicitly.
- Substance Painter/Designer may produce or inspect materials, but the final
  reference stage requires a host that can place scene geometry and render it.
- Do not color-grade a wrong chart into looking correct. Fix source encoding,
  material intent, working space, or display transform at the owning boundary.
