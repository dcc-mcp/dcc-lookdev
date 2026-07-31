"""Built-in host-neutral LookDev stage preset."""

from __future__ import annotations

import json
from pathlib import Path

from dcc_mcp_core.skill import skill_entry, skill_success

REFERENCE_KIT = json.loads(
    (Path(__file__).parents[1] / "assets" / "reference-kit.json").read_text(
        encoding="utf-8"
    )
)

STANDARD_PRESET = {
    "id": "camera-facing-lower-left-combined-turntable",
    "layout": {
        "aspect_ratio": "16:9",
        "subject_width_fraction": {"min": 0.55, "max": 0.70},
        "reference_anchor": "lower-left",
        "reference_width_fraction_max": 0.12,
        "clearance_width_fraction_min": 0.08,
        "title_safe_margin_fraction": 0.05,
        "reference_camera_space": True,
        "chart_plane_view_axis_degrees": 90.0,
        "chart_plane_view_axis_tolerance_degrees": 1.0,
    },
    "timeline": {
        "material_inspection": {
            "start_output_index": 0,
            "end_output_index": 179,
            "frame_count": 180,
            "rotation_owner": "SubjectRoot",
            "fixed_owner": "LightingRoot",
        },
        "lighting_inspection": {
            "start_output_index": 180,
            "end_output_index": 359,
            "frame_count": 180,
            "rotation_owner": "LightingRoot",
            "fixed_owner": "SubjectRoot",
        },
    },
    "rotation_degrees": 360.0,
    "duration_seconds": 12.0,
    "fps": 30.0,
    "output_frame_count": 360,
    "gray_linear_reflectance": 0.18,
}


@skill_entry
def get_preset(**kwargs) -> dict:
    """Return the standard camera-facing combined-turntable preset."""
    return skill_success(
        "Returned standard LookDev preset",
        preset=STANDARD_PRESET,
        reference_kit=REFERENCE_KIT,
    )


main = get_preset
