# Host Routing

Keep the workflow host-neutral. Discover current tools by intent and call only
described schemas.

## Common intents

Search for these capabilities in order:

1. list/import asset and inspect PBR texture color intent;
2. create/assign materials for chart, gray sphere, chrome sphere, ground, and HDRI;
3. spawn/list/transform actors or objects;
4. configure HDRI/environment, camera exposure, and lights;
5. attach or constrain the reference group in camera space;
6. create or inspect the subject and lighting turntable sequences;
7. queue, start, poll, and cancel the native renderer;
8. save the scene and inspect logs.

## Host notes

- Unreal Engine: use Level/Actor/Asset/Material/Cinematics skills and Movie Render
  Queue. Attach `ReferenceRoot` to the fixed camera while preserving a camera-local
  lower-left offset. A visible interior backdrop requires a two-sided material.
  Keep the backdrop sphere separate from the rotating light rig or SkyLight, then
  confirm each Level Sequence has exactly one transform owner.
- Maya, Blender, Houdini, and 3ds Max: prefer a dedicated subject root and separate
  camera-constrained reference, lighting, and environment roots. Use the host
  renderer's native HDRI and animation tools.
- Marmoset Toolbag: use it for material and output-boundary comparison. If only an
  ACES tone mapper is exposed, report `tone-mapper-only`; do not claim OCIO parity.
- Substance 3D Painter/Designer: keep Base Color as color and PBR data maps linear.
  Hand the result to a scene-capable host for the standardized stage.

## Missing capability

When a host cannot express one contract item, add the smallest typed primitive to
the owning adapter, test it in the real host, and keep this Skill unchanged unless
the cross-host workflow contract itself changes.
