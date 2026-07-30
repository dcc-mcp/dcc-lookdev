"""Validate measured facts for the standard LookDev turntable."""

from __future__ import annotations

from math import isclose

from dcc_mcp_core.skill import skill_entry, skill_success
from preset import STANDARD_PRESET


@skill_entry
def validate_stage(
    take_mode: str,
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
    duration_seconds: float,
    fps: float,
    output_frame_count: int,
    auto_exposure_enabled: bool,
    color_transform_valid: bool,
    **kwargs,
) -> dict:
    layout = STANDARD_PRESET["layout"]
    take_modes = STANDARD_PRESET["takes"]
    failures = []
    checks = (
        (
            take_mode in take_modes,
            "take_mode must be subject_turntable or lighting_turntable",
        ),
        (visible_subjects == 1, "visible_subjects must equal 1"),
        (reference_transform_tracks == 0, "reference_transform_tracks must equal 0"),
        (
            environment_transform_tracks == 0,
            "environment_transform_tracks must equal 0",
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
    )
    failures.extend(message for passed, message in checks if not passed)

    if take_mode in take_modes:
        subject_tracks = 1 if take_mode == "subject_turntable" else 0
        lighting_tracks = 1 if take_mode == "lighting_turntable" else 0
        if subject_transform_tracks != subject_tracks:
            failures.append(
                f"subject_transform_tracks must equal {subject_tracks} for {take_mode}"
            )
        if lighting_transform_tracks != lighting_tracks:
            failures.append(
                f"lighting_transform_tracks must equal {lighting_tracks} for {take_mode}"
            )

    passed = not failures
    return skill_success(
        "LookDev take passed"
        if passed
        else f"LookDev take failed {len(failures)} check(s)",
        passed=passed,
        take_mode=take_mode,
        failures=failures,
    )


main = validate_stage
