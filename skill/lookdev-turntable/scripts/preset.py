"""Built-in host-neutral LookDev stage preset."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

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

ASSET_TYPE_PRESETS = {
    item["asset_type"]: item for item in REFERENCE_KIT["asset_type_presets"]
}
HDRI_PRESETS = {item["id"]: item for item in REFERENCE_KIT["hdri_presets"]}


def _override(profile: dict, key: str, value) -> None:
    if value is not None:
        profile[key] = value


def _sphere(sphere_id: str) -> dict:
    return deepcopy(next(item for item in REFERENCE_KIT["spheres"] if item["id"] == sphere_id))


@skill_entry
def get_preset(**kwargs) -> dict:
    """Return the standard camera-facing combined-turntable preset."""
    return skill_success(
        "Returned standard LookDev preset",
        preset=STANDARD_PRESET,
        reference_kit=REFERENCE_KIT,
    )


@skill_entry
def recommend_hdr_preset(
    asset_type: str,
    hdri_id: Optional[str] = None,
    rotation_degrees: Optional[float] = None,
    exposure_ev: Optional[float] = None,
    white_balance_kelvin: Optional[int] = None,
    ground_shadow_enabled: Optional[bool] = None,
    ground_albedo_linear: Optional[List[float]] = None,
    ground_roughness: Optional[float] = None,
    gray_linear_reflectance: Optional[float] = None,
    white_linear_reflectance: Optional[float] = None,
    chrome_base_color_linear: Optional[float] = None,
    chrome_roughness: Optional[float] = None,
    **kwargs,
) -> dict:
    """Recommend a neutral PBR HDR profile, with explicit typed overrides."""
    if asset_type not in ASSET_TYPE_PRESETS:
        raise ValueError(f"Unsupported asset_type: {asset_type}")
    if hdri_id is not None and hdri_id not in HDRI_PRESETS:
        raise ValueError(f"Unknown hdri_id: {hdri_id}")

    profile = deepcopy(ASSET_TYPE_PRESETS[asset_type])
    _override(profile, "hdri_id", hdri_id)
    _override(profile, "rotation_degrees", rotation_degrees)
    _override(profile, "exposure_ev", exposure_ev)
    _override(profile, "white_balance_kelvin", white_balance_kelvin)
    if ground_shadow_enabled is not None:
        profile["ground_shadow"]["enabled"] = ground_shadow_enabled
        profile["ground_shadow"]["contact_shadow"] = ground_shadow_enabled
    _override(profile["ground_shadow"], "albedo_linear", ground_albedo_linear)
    _override(profile["ground_shadow"], "roughness", ground_roughness)

    spheres = {
        "gray_18": _sphere("gray_18"),
        "diffuse_white_80": _sphere("diffuse_white_80"),
        "chrome_mirror": _sphere("chrome_mirror"),
    }
    if gray_linear_reflectance is not None:
        spheres["gray_18"]["material"]["base_color_linear"] = [gray_linear_reflectance] * 3
    if white_linear_reflectance is not None:
        spheres["diffuse_white_80"]["material"]["base_color_linear"] = [white_linear_reflectance] * 3
    if chrome_base_color_linear is not None:
        spheres["chrome_mirror"]["material"]["base_color_linear"] = [chrome_base_color_linear] * 3
    if chrome_roughness is not None:
        spheres["chrome_mirror"]["material"]["roughness"] = chrome_roughness

    profile["hdri"] = deepcopy(HDRI_PRESETS[profile["hdri_id"]])
    profile["reference_spheres"] = spheres
    profile["color_pipeline"] = {
        "mode": "OCIO",
        "config_id_required": True,
        "working_space": "ACEScg",
        "display": "Rec.709 SDR",
        "view_transform": "ACES SDR-video",
        "output_encoding_count": 1,
        "gray_rendered_linear_luminance_range": [0.14, 0.22],
        "highlight_clipping_fraction_max": 0.005,
        "auto_exposure_enabled": False,
        "white_balance_kelvin": profile["white_balance_kelvin"],
    }
    profile["pbr_validation"] = {
        "enabled": True,
        "stylized_tint_allowed": False,
        "additional_sun_allowed": not profile["hdri"].get("contains_sun", False),
    }
    return skill_success(
        f"Recommended neutral PBR HDR preset for {asset_type}",
        profile=profile,
        reference_kit=REFERENCE_KIT,
    )


main = get_preset
