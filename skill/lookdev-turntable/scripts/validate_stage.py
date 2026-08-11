"""Validate measured facts for the standard LookDev turntable."""

from __future__ import annotations

from math import isclose

from dcc_mcp_core.skill import skill_entry, skill_success
from preset import STANDARD_PRESET


@skill_entry
def validate_stage(
    visible_subjects: int,
    subject_transform_tracks: int,
    lighting_transform_tracks: int,
    reference_transform_tracks: int,
    environment_transform_tracks: int,
    camera_transform_tracks: int,
    reference_camera_space: bool,
    reference_anchor: str,
    chart_plane_view_axis_degrees: float,
    subject_width_fraction: float,
    reference_width_fraction: float,
    clearance_width_fraction: float,
    gray_linear_reflectance: float,
    material_phase_frame_count: int,
    lighting_phase_frame_count: int,
    material_phase_subject_rotation_degrees: float,
    material_phase_lighting_rotation_degrees: float,
    lighting_phase_subject_rotation_degrees: float,
    lighting_phase_lighting_rotation_degrees: float,
    linear_interpolation: bool,
    subject_material_valid: bool,
    visible_light_geometry: bool,
    native_rendered_frame_count: int,
    synthetic_interpolation_used: bool,
    duration_seconds: float,
    fps: float,
    output_frame_count: int,
    auto_exposure_enabled: bool,
    color_transform_valid: bool,
    pbr_validation_mode: bool = True,
    stylized_tint_enabled: bool = False,
    hdri_contains_sun: bool = False,
    additional_sun_lights: int = 0,
    **kwargs,
) -> dict:
    layout = STANDARD_PRESET["layout"]
    timeline = STANDARD_PRESET["timeline"]
    failures = []
    checks = (
        (visible_subjects == 1, "visible_subjects must equal 1"),
        (subject_transform_tracks == 1, "subject_transform_tracks must equal 1"),
        (lighting_transform_tracks == 1, "lighting_transform_tracks must equal 1"),
        (reference_transform_tracks == 0, "reference_transform_tracks must equal 0"),
        (
            environment_transform_tracks in (0, 1),
            "environment_transform_tracks must be 0 or the one lighting-owned HDRI track",
        ),
        (camera_transform_tracks == 0, "camera_transform_tracks must equal 0"),
        (reference_camera_space, "reference_camera_space must be true"),
        (
            reference_anchor == layout["reference_anchor"],
            "reference_anchor must be lower-left",
        ),
        (
            isclose(
                chart_plane_view_axis_degrees,
                layout["chart_plane_view_axis_degrees"],
                abs_tol=layout["chart_plane_view_axis_tolerance_degrees"],
            ),
            "chart_plane_view_axis_degrees must be 90 ± 1",
        ),
        (
            layout["subject_width_fraction"]["min"]
            <= subject_width_fraction
            <= layout["subject_width_fraction"]["max"],
            "subject_width_fraction must be between 0.55 and 0.70",
        ),
        (
            reference_width_fraction <= layout["reference_width_fraction_max"],
            "reference_width_fraction must be at most 0.12",
        ),
        (
            clearance_width_fraction >= layout["clearance_width_fraction_min"],
            "clearance_width_fraction must be at least 0.08",
        ),
        (
            isclose(
                gray_linear_reflectance,
                STANDARD_PRESET["gray_linear_reflectance"],
                abs_tol=0.005,
            ),
            "gray_linear_reflectance must be 0.18 ± 0.005",
        ),
        (
            material_phase_frame_count
            == timeline["material_inspection"]["frame_count"],
            "material_phase_frame_count must equal 180",
        ),
        (
            lighting_phase_frame_count
            == timeline["lighting_inspection"]["frame_count"],
            "lighting_phase_frame_count must equal 180",
        ),
        (
            isclose(material_phase_subject_rotation_degrees, 360.0, abs_tol=0.01),
            "material phase subject rotation must equal 360 degrees",
        ),
        (
            isclose(material_phase_lighting_rotation_degrees, 0.0, abs_tol=0.01),
            "material phase lighting rotation must equal 0 degrees",
        ),
        (
            isclose(lighting_phase_subject_rotation_degrees, 0.0, abs_tol=0.01),
            "lighting phase subject rotation must equal 0 degrees",
        ),
        (
            isclose(lighting_phase_lighting_rotation_degrees, 360.0, abs_tol=0.01),
            "lighting phase lighting rotation must equal 360 degrees",
        ),
        (linear_interpolation, "linear_interpolation must be true"),
        (subject_material_valid, "subject_material_valid must be true"),
        (not visible_light_geometry, "visible_light_geometry must be false"),
        (
            native_rendered_frame_count == STANDARD_PRESET["output_frame_count"],
            "native_rendered_frame_count must equal 360",
        ),
        (
            not synthetic_interpolation_used,
            "synthetic_interpolation_used must be false",
        ),
        (
            isclose(
                duration_seconds, STANDARD_PRESET["duration_seconds"], abs_tol=0.01
            ),
            "duration_seconds must equal 12",
        ),
        (isclose(fps, STANDARD_PRESET["fps"], abs_tol=0.01), "fps must equal 30"),
        (
            output_frame_count == STANDARD_PRESET["output_frame_count"],
            "output_frame_count must equal 360",
        ),
        (not auto_exposure_enabled, "auto_exposure_enabled must be false"),
        (color_transform_valid, "color_transform_valid must be true"),
        (
            not (pbr_validation_mode and stylized_tint_enabled),
            "stylized_tint_enabled must be false in PBR validation mode",
        ),
        (
            not (hdri_contains_sun and additional_sun_lights > 0),
            "additional_sun_lights must equal 0 when the HDRI contains the sun",
        ),
    )
    failures.extend(message for passed, message in checks if not passed)

    passed = not failures
    return skill_success(
        "LookDev sequence passed"
        if passed
        else f"LookDev sequence failed {len(failures)} check(s)",
        passed=passed,
        failures=failures,
    )


main = validate_stage
