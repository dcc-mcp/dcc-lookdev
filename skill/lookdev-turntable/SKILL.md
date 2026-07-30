---
name: lookdev-turntable
description: >-
  Build and verify a standardized PBR LookDev turntable with one centered subject,
  a fixed visible HDRI environment, fixed ColorChecker, 18% gray sphere, chrome
  sphere, fixed camera/exposure, and subject-only rotation. Use for repeatable
  material review and showcase renders across supported DCC hosts.
license: MIT-0
compatibility: "dcc-mcp-core 0.19+, typed scene/material/camera/animation/render tools"
allowed-tools: Bash Read Write
metadata:
  dcc-mcp:
    dcc: multi-dcc
    version: "0.1.1"
    layer: domain
    stage: presentation
    tags: [lookdev, pbr, turntable, hdri, color-management, render]
    search-hint: "standard PBR lookdev stage, fixed ColorChecker, 18 percent gray sphere, chrome sphere, HDRI, subject-only turntable"
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

- `SubjectRoot`: centered on the turntable pivot; the only animated transform.
- `ReferenceRoot`: ColorChecker, gray sphere, and chrome sphere; never animated.
- `EnvironmentRoot`: visible HDRI backdrop and environment lighting; fixed rotation,
  intensity, and exposure during the take.
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
3. Build the four roots above. Parent only the subject to the animated root.
4. Frame the subject and fixed reference group using the normalized layout contract.
5. Author one linear 0 to 360 degree rotation over 12 seconds at 30 fps.
6. Render exactly three preview frames first. Reject overlap, clipping, duplicate
   subjects/reflections, automatic exposure, invalid color transforms, or moving
   reference objects.
7. Render 360 final frames, encode H.264/BT.709 for review, and retain the image
   sequence for pixel-level validation.
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
