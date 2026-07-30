import importlib.util
from pathlib import Path

SCRIPTS = Path(__file__).parents[1] / "skill" / "lookdev-turntable" / "scripts"


def _load(monkeypatch, name):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _standard(take_mode):
    lighting_turntable = take_mode == "lighting_turntable"
    return {
        "take_mode": take_mode,
        "visible_subjects": 1,
        "subject_transform_tracks": 0 if lighting_turntable else 1,
        "lighting_transform_tracks": 1 if lighting_turntable else 0,
        "reference_transform_tracks": 0,
        "environment_transform_tracks": 0,
        "camera_transform_tracks": 0,
        "reference_camera_space": True,
        "reference_anchor": "lower-left",
        "chart_plane_view_axis_degrees": 90.0,
        "subject_width_fraction": 0.62,
        "reference_width_fraction": 0.10,
        "clearance_width_fraction": 0.09,
        "gray_linear_reflectance": 0.18,
        "duration_seconds": 12,
        "fps": 30,
        "output_frame_count": 360,
        "auto_exposure_enabled": False,
        "color_transform_valid": True,
    }


def test_preset_and_both_turntable_takes_pass(monkeypatch):
    preset_module = _load(monkeypatch, "preset")
    assert preset_module.main is preset_module.get_preset
    preset = preset_module.main()["context"]["preset"]
    assert preset["id"] == "camera-facing-lower-left-dual-turntable"
    kit = preset_module.main()["context"]["reference_kit"]
    assert [sphere["id"] for sphere in kit["spheres"]] == [
        "gray_18",
        "diffuse_white_80",
        "chrome_mirror",
    ]
    assert len(kit["charts"][0]["swatches_srgb8"]) == 24
    assert len(kit["hdri_presets"]) == 3

    validate_module = _load(monkeypatch, "validate_stage")
    assert validate_module.main is validate_module.validate_stage
    validate = validate_module.main
    assert validate(**_standard("subject_turntable"))["context"]["passed"] is True
    assert validate(**_standard("lighting_turntable"))["context"]["passed"] is True


def test_camera_facing_and_transform_ownership_fail_closed(monkeypatch):
    validate = _load(monkeypatch, "validate_stage").validate_stage
    wrong = _standard("subject_turntable")
    wrong["chart_plane_view_axis_degrees"] = 75
    wrong["lighting_transform_tracks"] = 1
    result = validate(**wrong)

    assert result["context"]["passed"] is False
    assert (
        "chart_plane_view_axis_degrees must be 90 ± 1" in result["context"]["failures"]
    )
    assert (
        "lighting_transform_tracks must equal 0 for subject_turntable"
        in result["context"]["failures"]
    )
