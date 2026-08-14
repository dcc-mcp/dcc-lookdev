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
materials, technical chart, measured-chart provenance, common HDRI presets, and
the six asset-type TT recommendations.
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

- Neutral measured-style chromium base color: linear RGB `(0.55, 0.56, 0.55)`.
- Metallic: `1`.
- Roughness: `0.03`.
- Non-emissive.

### 80% diffuse white sphere

- Base color: linear RGB `(0.80, 0.80, 0.80)`.
- Metallic: `0`.
- Roughness: `0.65`.
- Non-emissive; neutral specular response.

### Reference-sphere contract

- All three spheres are true lit PBR references. They must respond to physical
  lights and the HDRI; never make them emission materials or compensate them with
  a baked display LUT.
- Judge gray and white from the scene-linear render before the display transform.
  The gray median gate is defined below. Use the white sphere to reveal highlight
  clipping and diffuse-energy errors, not as a fixed display-code swatch.
- The chrome sphere must show a readable, neutral environment reflection. A flat,
  black, invisible, or self-lit chrome sphere fails the reference gate.

### ColorChecker

- Use a measured modern ColorChecker Classic 24 dataset with recorded provenance.
- Import display-encoded chart textures as sRGB/color; never as non-color data.
- Material: non-emissive, metallic `0`, roughness `0.65`.
- Keep chart geometry flat and front-facing. Validate row/column orientation before
  judging color.
- Use the bundled MIT-0 digital chart only as an unlit technical reference. It is
  not a measured physical ColorChecker. For lit evaluation, supply or generate the
  external measured chart named by the reference kit and preserve its provenance.

Choose and record exactly one chart mode:

- `measured_lit`: a physical/reflectance chart. Use a non-emissive PBR material
  and let it respond to lighting. It is evidence for illumination and material
  color, not an invariant display-code target.
- `technical_unlit`: a digital display reference. Convert each target display
  code through the inverse of the active OCIO display/view into the scene working
  space, write that value to emission, disable base/specular contribution, and
  then let the complete image receive the same single normal display transform.
  Do not write ordinary scene-linear sRGB values directly and expect the ACES view
  to preserve their display codes.

For `technical_unlit`, render a second frame after changing only actual scene-light
intensities. Keep camera, exposure, OCIO config/display/view, and chart material
fixed. Patch-center RGB values must differ by at most `2/255`. This proves light
independence without bypassing OCIO. Never bake a LUT into the chart and apply the
same LUT again at output.

### Encoded-media temporal reference contract

Validate every GIF, video, or other review derivative by decoding it back to RGB
and comparing it with the display-encoded source image sequence. Both sides of
this comparison are after the one normal OCIO display/view transform. These RGB
code values are display references, not scene-linear reflectance or shader input;
never copy them into Base Color, emission, or the scene-linear gray-sphere gate.

- For a `technical_unlit` chart, decoded patch-center RGB values may vary by at
  most `2/255` across the sequence.
- Each decoded patch center may differ from its corresponding display-encoded
  source frame by at most `4/255` per channel.
- Palette-indexed media such as GIF must use one palette for the entire sequence.
  Explicitly reserve entries for all 24 chart patches and three neutral reference
  representatives, then jointly quantize the remaining scene colors.
- Disable dithering for indexed review media. Per-frame adaptive palettes and
  frame-local quantization are invalid even when the source image sequence passes.
- Continuous-tone or YUV video has no indexed palette. Record
  `encoded_media_has_indexed_palette=false` instead of inventing palette evidence,
  but still perform the decoded temporal and source-error checks.

The three reference spheres remain true lit PBR objects, so their pixel values may
change when physical lighting changes. Reserving their neutral representative
entries prevents quantization-induced flicker; it does not make their response
light-invariant.

## Color and texture intent

- Base Color and ColorChecker: color textures with the declared source gamut.
- Normal, Roughness, Metallic, and AO: non-color/data textures.
- Work scene-linearly. Use one validated OCIO config where the host supports it.
- Default review output: ACEScg to Rec.709 SDR, encoded once, with BT.709 container
  metadata. Do not apply a second LUT during video encoding.
- Record a stable identifier for the active OCIO config plus the resolved working
  space, display, and view transform. A generic `valid` boolean is not evidence.
- Measure the 18% sphere in the scene-linear render before the display transform;
  its median luminance must remain between `0.14` and `0.22`.
- Measure the fraction of finite RGB samples above `1.0` in the scene-linear
  preview. It must not exceed `0.005`; diagnose lighting/exposure before grading.
- Verify Base Color and chart textures as color, and Normal/Roughness/Metallic/AO
  as data. Missing or ambiguous texture intent fails the preview gate.
- In PBR validation mode, use neutral illumination and disable stylized tint.
- When the selected HDRI contains a captured sun, do not add a second sun light.

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
5. Preview frames from both halves pass layout, chart direction/mode/light-variant,
   measured linear exposure, true-lit reference-sphere response, readable chrome,
   evidence-backed OCIO, single-encoding, texture-intent,
   light-helper visibility, and material checks.
6. The final image sequence contains exactly 360 native rendered frames.
7. First, middle, and last frames preserve fixed reference-pixel locations.
8. The single video reports 1920x1080 or greater, 30 fps, 12 seconds, and BT.709 tags.
9. Every encoded review derivative passes decoded chart temporal stability and
   source-error gates. Indexed derivatives additionally use one reserved,
   non-dithered sequence palette.
