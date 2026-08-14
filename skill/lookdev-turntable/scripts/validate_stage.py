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
    ocio_config_id: str,
    working_space: str,
    display: str,
    view_transform: str,
    output_encoding_count: int,
    gray_rendered_linear_luminance: float,
    highlight_clipping_fraction: float,
    color_texture_intent_valid: bool,
    data_texture_intent_valid: bool,
    chart_reference_mode: str,
    chart_emission_enabled: bool,
    chart_inverse_view_calibrated: bool,
    chart_light_variant_max_rgb_delta: float,
    reference_spheres_lit: bool,
    reference_spheres_emission_enabled: bool,
    reference_sphere_materials_valid: bool,
    chrome_reflection_visible: bool,
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
            bool(ocio_config_id.strip()),
            "ocio_config_id must identify the active OCIO config",
        ),
        (working_space == "ACEScg", "working_space must equal ACEScg"),
        (bool(display.strip()), "display must identify the active display"),
        (
            bool(view_transform.strip()),
            "view_transform must identify the active OCIO view",
        ),
        (
            output_encoding_count == 1,
            "output_encoding_count must equal 1",
        ),
        (
            0.14 <= gray_rendered_linear_luminance <= 0.22,
            "gray_rendered_linear_luminance must be between 0.14 and 0.22",
        ),
        (
            highlight_clipping_fraction <= 0.005,
            "highlight_clipping_fraction must be at most 0.005",
        ),
        (
            color_texture_intent_valid,
            "color_texture_intent_valid must be true",
        ),
        (
            data_texture_intent_valid,
            "data_texture_intent_valid must be true",
        ),
        (
            chart_reference_mode in ("measured_lit", "technical_unlit"),
            "chart_reference_mode must be measured_lit or technical_unlit",
        ),
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

    if chart_reference_mode == "technical_unlit":
        chart_checks = (
            (
                chart_emission_enabled,
                "chart_emission_enabled must be true for technical_unlit",
            ),
            (
                chart_inverse_view_calibrated,
                "chart_inverse_view_calibrated must be true for technical_unlit",
            ),
            (
                chart_light_variant_max_rgb_delta <= 2.0 / 255.0,
                "chart_light_variant_max_rgb_delta must be at most 2/255 for technical_unlit",
            ),
        )
    elif chart_reference_mode == "measured_lit":
        chart_checks = (
            (
                not chart_emission_enabled,
                "chart_emission_enabled must be false for measured_lit",
            ),
        )
    else:
        chart_checks = ()

    reference_checks = (
        (reference_spheres_lit, "reference_spheres_lit must be true"),
        (
            not reference_spheres_emission_enabled,
            "reference_spheres_emission_enabled must be false",
        ),
        (
            reference_sphere_materials_valid,
            "reference_sphere_materials_valid must be true",
        ),
        (chrome_reflection_visible, "chrome_reflection_visible must be true"),
    )
    failures.extend(
        message
        for passed, message in (*chart_checks, *reference_checks)
        if not passed
    )

    passed = not failures
    return skill_success(
        "LookDev sequence passed"
        if passed
        else f"LookDev sequence failed {len(failures)} check(s)",
        passed=passed,
        failures=failures,
    )


main = validate_stage
