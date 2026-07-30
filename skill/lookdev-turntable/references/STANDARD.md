# LookDev Turntable Standard

## Framing

- Output: 16:9.
- Subject: centered, complete silhouette, approximately 55-70% of frame width.
- Reference group: lower-left, at most 12% of frame width.
- Clearance: at least 8% of frame width between the reference group and the
  subject silhouette.
- Order: gray sphere left, chrome sphere right, ColorChecker below them.
- Keep all reference items inside 5% title-safe margins.

These are normalized screen-space acceptance values. World transforms are host,
asset, camera, and focal-length dependent.

## Reference materials

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

## Color and texture intent

- Base Color and ColorChecker: color textures with the declared source gamut.
- Normal, Roughness, Metallic, and AO: non-color/data textures.
- Work scene-linearly. Use one validated OCIO config where the host supports it.
- Default review output: ACEScg to Rec.709 SDR, encoded once, with BT.709 container
  metadata. Do not apply a second LUT during video encoding.

## Animation and output

- Subject rotation: one axis, `0 -> 360` degrees, linear interpolation.
- Duration: 12 seconds at 30 fps, 360 output frames.
- Fixed during the take: reference group, camera, exposure, HDRI rotation/intensity,
  lights, ground, and color transform.
- Final media: 1920x1080 minimum, H.264 High, yuv420p, 30 fps, BT.709 primaries,
  transfer, and matrix.

## Acceptance gates

1. Scene contains one visible subject and one animated subject root.
2. Reference group and environment have no animation tracks.
3. Three-frame preview passes layout, chart direction, exposure, and OCIO checks.
4. Final image sequence contains exactly 360 frames.
5. First, middle, and last frames preserve fixed reference-pixel locations.
6. Video probe reports 1920x1080 or greater, 30 fps, 12 seconds, and BT.709 tags.
