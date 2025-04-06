import sys

from note_size.config.level_parser import LevelParser, Level, LevelDict
from note_size.common.types import SizeBytes, SizeStr
from tests.data import Colors


def test_parse_levels(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.orange, "Max Size": "1 MB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    levels: list[Level] = level_parser.parse_levels(levels_dict)
    assert levels == [
        Level(Colors.pale_green, SizeBytes(0), SizeBytes(102_400), SizeStr("0 B"), SizeStr("100 KB")),
        Level(Colors.orange, SizeBytes(102_400), SizeBytes(1_048_576), SizeStr("100 KB"), SizeStr("1 MB")),
        Level(Colors.light_coral, SizeBytes(1_048_576), SizeBytes(sys.maxsize), SizeStr("1 MB"), SizeStr("∞"))
    ]


def test_parse_levels_single(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": None})]
    levels: list[Level] = level_parser.parse_levels(levels_dict)
    assert levels == [
        Level(Colors.pale_green, SizeBytes(0), SizeBytes(sys.maxsize), SizeStr("0 B"), SizeStr("∞"))
    ]


def test_add_level(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.orange, "Max Size": "1 MB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"},
        {LevelParser.color_key: Colors.orange, "Max Size": "1 MB"},
        {LevelParser.color_key: Colors.light_coral, "Max Size": "2 MB"},
        {LevelParser.color_key: Colors.yellow, "Max Size": None}]


def test_add_level_to_two(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"},
        {LevelParser.color_key: Colors.light_coral, "Max Size": "200 KB"},
        {LevelParser.color_key: Colors.yellow, "Max Size": None}]


def test_add_level_to_single(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": None})]
    level_parser.add_level(levels_dict)
    assert levels_dict == [
        {LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"},
        {LevelParser.color_key: Colors.yellow, "Max Size": None}]


def test_remove_level_middle(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.orange, "Max Size": "1 MB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.remove_level(levels_dict, 1)
    assert levels_dict == [
        {LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"},
        {LevelParser.color_key: Colors.light_coral, "Max Size": None}]


def test_remove_level_first(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.orange, "Max Size": "1 MB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.remove_level(levels_dict, 0)
    assert levels_dict == [
        {LevelParser.color_key: Colors.orange, "Max Size": "1 MB"},
        {LevelParser.color_key: Colors.light_coral, "Max Size": None}]


def test_remove_level_last(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"}),
        LevelDict({LevelParser.color_key: Colors.orange, "Max Size": "1 MB"}),
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.remove_level(levels_dict, 2)
    assert levels_dict == [
        {LevelParser.color_key: Colors.pale_green, "Max Size": "100 KB"},
        {LevelParser.color_key: Colors.orange, "Max Size": None}]


def test_remove_level_last_level(level_parser: LevelParser):
    levels_dict: list[LevelDict] = [
        LevelDict({LevelParser.color_key: Colors.light_coral, "Max Size": None})]
    level_parser.remove_level(levels_dict, 0)
    assert levels_dict == [
        {LevelParser.color_key: Colors.light_coral, "Max Size": None}]
