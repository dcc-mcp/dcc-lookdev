import importlib.util
import json
from pathlib import Path

SCRIPTS = Path(__file__).parents[1] / "skill" / "lookdev-turntable" / "scripts"
SKILL_ROOT = SCRIPTS.parent


def _load(monkeypatch, name):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _standard():
    return {
        "visible_subjects": 1,
        "subject_transform_tracks": 1,
        "lighting_transform_tracks": 1,
        "reference_transform_tracks": 0,
        "environment_transform_tracks": 1,
        "camera_transform_tracks": 0,
        "reference_camera_space": True,
        "reference_anchor": "lower-left",
        "chart_plane_view_axis_degrees": 90.0,
        "subject_width_fraction": 0.62,
        "reference_width_fraction": 0.10,
        "clearance_width_fraction": 0.09,
        "gray_linear_reflectance": 0.18,
        "material_phase_frame_count": 180,
        "lighting_phase_frame_count": 180,
        "material_phase_subject_rotation_degrees": 360.0,
        "material_phase_lighting_rotation_degrees": 0.0,
        "lighting_phase_subject_rotation_degrees": 0.0,
        "lighting_phase_lighting_rotation_degrees": 360.0,
        "linear_interpolation": True,
        "subject_material_valid": True,
        "visible_light_geometry": False,
        "native_rendered_frame_count": 360,
        "synthetic_interpolation_used": False,
        "duration_seconds": 12,
        "fps": 30,
        "output_frame_count": 360,
        "auto_exposure_enabled": False,
        "color_transform_valid": True,
    }


def test_preset_and_combined_turntable_pass(monkeypatch):
    preset_module = _load(monkeypatch, "preset")
    assert preset_module.main is preset_module.get_preset
    preset = preset_module.main()["context"]["preset"]
    assert preset["id"] == "camera-facing-lower-left-combined-turntable"
    assert preset["timeline"]["material_inspection"]["frame_count"] == 180
    assert preset["timeline"]["lighting_inspection"]["frame_count"] == 180
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
    assert validate(**_standard())["context"]["passed"] is True


def test_camera_facing_and_render_integrity_fail_closed(monkeypatch):
    validate = _load(monkeypatch, "validate_stage").validate_stage
    wrong = _standard()
    wrong["chart_plane_view_axis_degrees"] = 75
    wrong["visible_light_geometry"] = True
    wrong["synthetic_interpolation_used"] = True
    result = validate(**wrong)

    assert result["context"]["passed"] is False
    assert (
        "chart_plane_view_axis_degrees must be 90 ± 1" in result["context"]["failures"]
    )
    assert "visible_light_geometry must be false" in result["context"]["failures"]
    assert "synthetic_interpolation_used must be false" in result["context"]["failures"]


def test_tools_yaml_registers_complete_validation_schema():
    from dcc_mcp_core import SkillCatalog, ToolRegistry

    registry = ToolRegistry()
    catalog = SkillCatalog(registry)
    catalog.discover(extra_paths=[str(SKILL_ROOT.parent)])
    catalog.load_skill("lookdev-turntable")

    tools = {item["name"]: item for item in registry.list_actions()}
    schema = tools["lookdev_turntable__validate_stage"]["input_schema"]
    if isinstance(schema, str):
        schema = json.loads(schema)

    properties = schema["properties"]
    assert len(properties) == 29
    assert len(schema["required"]) == 29
    assert "lighting_transform_tracks" in properties
    assert "native_rendered_frame_count" in properties
