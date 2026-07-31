# LookDev Turntable Standard

## Framing

- Output: 16:9.
- Subject: centered, complete silhouette, approximately 55-70% of frame width.
- Reference group: lower-left, at most 12% of frame width.
- Clearance: at least 8% of frame width between the reference group and the
  subject silhouette.
- Order: gray sphere left, chrome sphere right, ColorChecker below them.
- Keep all reference items inside 5% title-safe margins.
- Keep `ReferenceRoot` in camera space so its screen position is invariant.
- The ColorChecker plane must be perpendicular to the camera view axis: 90 degrees
  with at most 1 degree error. Its front surface must face the camera.

These are normalized screen-space acceptance values. World transforms are host,
asset, camera, and focal-length dependent.

## Reference materials

`assets/reference-kit.json` is the portable source of truth for the three-sphere
materials, technical chart, measured-chart provenance, and common HDRI presets.
Create host geometry and materials from these values; do not copy host scene files
between adapters.

### 18% gray sphere

- Base color: linear RGB `(0.18, 0.18, 0.18)`.
- Metallic: `0`.
- Roughness: `0.65`.
- Non-emissive; neutral specular response.

For an 8-bit sRGB texture, approximately `118/255` decodes to `0.181` linear.
Do not store the literal value `0.18` in an sRGB-encoded texture.

### Chrome sphere

- Neutral base color.
- Metallic: `1`.
- Roughness: `0`.
- Non-emissive.

### ColorChecker

- Use a measured modern ColorChecker Classic 24 dataset with recorded provenance.
- Import display-encoded chart textures as sRGB/color; never as non-color data.
- Material: non-emissive, metallic `0`, roughness `0.65`.
- Keep chart geometry flat and front-facing. Validate row/column orientation before
  judging color.
- Use the bundled MIT-0 digital chart only as an unlit technical reference. It is
  not a measured physical ColorChecker. For lit evaluation, supply or generate the
  external measured chart named by the reference kit and preserve its provenance.

## Color and texture intent

- Base Color and ColorChecker: color textures with the declared source gamut.
- Normal, Roughness, Metallic, and AO: non-color/data textures.
- Work scene-linearly. Use one validated OCIO config where the host supports it.
- Default review output: ACEScg to Rec.709 SDR, encoded once, with BT.709 container
  metadata. Do not apply a second LUT during video encoding.

## Animation and output

- One combined sequence is 12 seconds at 30 fps and produces 360 output frames.
- First 180 output frames, material inspection: `SubjectRoot` rotates on one axis,
  `0 -> 360` degrees with linear interpolation; `LightingRoot` is fixed.
- Final 180 output frames, lighting inspection: `LightingRoot` rotates on one axis,
  `0 -> 360` degrees with linear interpolation; `SubjectRoot` is fixed at its
  starting orientation.
- Fixed for the complete sequence: reference group, camera, exposure, ground, and
  color transform.
- `LightingRoot` may own physical lights or the lighting-only HDRI orientation.
  Keep the visible HDRI backdrop separate and fixed when the host permits it.
- Light helpers and emitter geometry must not be camera-visible.
- Every output frame must come from the DCC renderer. Optical-flow or other
  synthetic frame interpolation is not accepted as render evidence.
- Final media: 1920x1080 minimum, H.264 High, yuv420p, 30 fps, BT.709 primaries,
  transfer, and matrix.

## Acceptance gates

1. Scene contains one visible subject with valid material assignments.
2. The combined sequence has one subject track and one lighting track.
3. The first 180 frames rotate only the subject; the final 180 rotate only lighting.
4. Reference group and camera have no animation tracks. A visible HDRI may reuse
   the one lighting track when the host cannot decouple lighting from the backdrop.
5. Preview frames from both halves pass layout, chart direction, exposure, OCIO,
   light-helper visibility, and material checks.
6. The final image sequence contains exactly 360 native rendered frames.
7. First, middle, and last frames preserve fixed reference-pixel locations.
8. The single video reports 1920x1080 or greater, 30 fps, 12 seconds, and BT.709 tags.
