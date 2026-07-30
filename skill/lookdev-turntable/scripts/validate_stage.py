"""Validate measured facts for the standard LookDev turntable."""

from __future__ import annotations

from math import isclose

from dcc_mcp_core.skill import skill_entry, skill_success


@skill_entry
def validate_stage(
    visible_subjects: int,
    subject_transform_tracks: int,
    reference_transform_tracks: int,
    environment_transform_tracks: int,
    camera_transform_tracks: int,
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
    failures = []
    checks = (
        (visible_subjects == 1, "visible_subjects must equal 1"),
        (subject_transform_tracks == 1, "subject_transform_tracks must equal 1"),
        (reference_transform_tracks == 0, "reference_transform_tracks must equal 0"),
        (
            environment_transform_tracks == 0,
            "environment_transform_tracks must equal 0",
        ),
        (camera_transform_tracks == 0, "camera_transform_tracks must equal 0"),
        (
            0.55 <= subject_width_fraction <= 0.70,
            "subject_width_fraction must be between 0.55 and 0.70",
        ),
        (
            reference_width_fraction <= 0.12,
            "reference_width_fraction must be at most 0.12",
        ),
        (
            clearance_width_fraction >= 0.08,
            "clearance_width_fraction must be at least 0.08",
        ),
        (
            isclose(gray_linear_reflectance, 0.18, abs_tol=0.005),
            "gray_linear_reflectance must be 0.18 ± 0.005",
        ),
        (
            isclose(duration_seconds, 12.0, abs_tol=0.01),
            "duration_seconds must equal 12",
        ),
        (isclose(fps, 30.0, abs_tol=0.01), "fps must equal 30"),
        (output_frame_count == 360, "output_frame_count must equal 360"),
        (not auto_exposure_enabled, "auto_exposure_enabled must be false"),
        (color_transform_valid, "color_transform_valid must be true"),
    )
    failures.extend(message for passed, message in checks if not passed)
    passed = not failures
    return skill_success(
        "LookDev stage passed"
        if passed
        else f"LookDev stage failed {len(failures)} check(s)",
        passed=passed,
        failures=failures,
    )
