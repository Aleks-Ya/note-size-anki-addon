import sys

from note_size.config.level_parser import LevelParser, Level, LevelDict
from note_size.common.types import SizeBytes, SizeStr


def test_parse_levels(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "Orange", "Max Size": "1 MB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    levels: list[Level] = level_parser.parse_levels(levels_dict)
    assert levels == [
        Level("PaleGreen", SizeBytes(0), SizeBytes(102_400), SizeStr("0 B"), SizeStr("100 KB")),
        Level("Orange", SizeBytes(102_400), SizeBytes(1_048_576), SizeStr("100 KB"), SizeStr("1 MB")),
        Level("LightCoral", SizeBytes(1_048_576), SizeBytes(sys.maxsize), SizeStr("1 MB"), SizeStr("∞"))
    ]


def test_parse_levels_single(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": None})]
    levels: list[Level] = level_parser.parse_levels(levels_dict)
    assert levels == [
        Level("PaleGreen", SizeBytes(0), SizeBytes(sys.maxsize), SizeStr("0 B"), SizeStr("∞"))
    ]


def test_add_level(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "Orange", "Max Size": "1 MB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {"Color": "PaleGreen", "Max Size": "100 KB"},
        {"Color": "Orange", "Max Size": "1 MB"},
        {"Color": "LightCoral", "Max Size": "2 MB"},
        {"Color": "Yellow", "Max Size": None}]


def test_add_level_to_two(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {"Color": "PaleGreen", "Max Size": "100 KB"},
        {"Color": "LightCoral", "Max Size": "200 KB"},
        {"Color": "Yellow", "Max Size": None}]


def test_add_level_to_single(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {"Color": "PaleGreen", "Max Size": "100 KB"},
        {"Color": "Yellow", "Max Size": None}]


def test_remove_level_middle(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "Orange", "Max Size": "1 MB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.remove_level(levels_dict, 1)
    assert levels_dict == [
        {"Color": "PaleGreen", "Max Size": "100 KB"},
        {"Color": "LightCoral", "Max Size": None}]


def test_remove_level_first(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "Orange", "Max Size": "1 MB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.remove_level(levels_dict, 0)
    assert levels_dict == [
        {"Color": "Orange", "Max Size": "1 MB"},
        {"Color": "LightCoral", "Max Size": None}]


def test_remove_level_last(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "PaleGreen", "Max Size": "100 KB"}),
        LevelDict({"Color": "Orange", "Max Size": "1 MB"}),
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.remove_level(levels_dict, 2)
    assert levels_dict == [
        {"Color": "PaleGreen", "Max Size": "100 KB"},
        {"Color": "Orange", "Max Size": None}]


def test_remove_level_last_level(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({"Color": "LightCoral", "Max Size": None})]
    level_parser.remove_level(levels_dict, 0)
    assert levels_dict == [
        {"Color": "LightCoral", "Max Size": None}]
