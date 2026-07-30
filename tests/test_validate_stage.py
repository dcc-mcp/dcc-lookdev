import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).parents[1]
    / "skill"
    / "lookdev-turntable"
    / "scripts"
    / "validate_stage.py"
)


def _load():
    spec = importlib.util.spec_from_file_location("validate_stage", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _standard():
    return {
        "visible_subjects": 1,
        "subject_transform_tracks": 1,
        "reference_transform_tracks": 0,
        "environment_transform_tracks": 0,
        "camera_transform_tracks": 0,
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


def test_validate_stage_passes_standard_and_reports_clearance_failure():
    module = _load()
    result = module.validate_stage(**_standard())
    assert result["context"]["passed"] is True

    too_close = _standard()
    too_close["clearance_width_fraction"] = 0.04
    result = module.validate_stage(**too_close)
    assert result["context"]["passed"] is False
    assert (
        "clearance_width_fraction must be at least 0.08"
        in result["context"]["failures"]
    )
