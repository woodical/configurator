import io

import pytest
import config_properties


def test_empty_properties_str():
    assert config_properties.properties_string_to_dict("") == {}


def test_missing_properties_file():
    with pytest.raises(FileNotFoundError, match="missing"):
        config_properties.parse_properties_file("missing")


def test_properties_skips_comments_and_blank_lines():
    content = """# empty file

     # whitespace leading comment
# no content
"""
    assert config_properties.properties_string_to_dict(content) == {}


def test_properties_creates_flat_dict():
    # using comment a dubious whitespace
    content = """# line 1
name=bob     
status = bewildered    
"""
    assert config_properties.properties_string_to_dict(content) == {
        "name": "bob",
        "status": "bewildered",
    }


def test_properties_creates_nested_dict():
    # using comment a dubious whitespace
    content = """# line 1
agent.name=bob     
agent.status = bewildered    
"""
    assert config_properties.properties_string_to_dict(content) == {
        "agent": {"name": "bob", "status": "bewildered"}
    }


def test_properties_creates_deeper_nested_dict():
    # using comment a dubious whitespace
    content = """# line 1
agent.name=bob     
agent.status = bewildered    
heroes.batman = winged
heroes.superman  = strong
weapons.weak.stick   = bamboo
weapons.weak.water   = wet
weapons.strong.iron   = sword
homes.batman.house = mansion
homes.batman.work = cave

"""
    assert config_properties.properties_string_to_dict(content) == {
        "agent": {"name": "bob", "status": "bewildered"},
        "heroes": {"batman": "winged", "superman": "strong"},
        "homes": {"batman": {"house": "mansion", "work": "cave"}},
        "weapons": {
            "strong": {"iron": "sword"},
            "weak": {"stick": "bamboo", "water": "wet"},
        },
    }


def test_properties_read_from_file():
    assert config_properties.parse_properties_file("example.jinit") == {
        "mkv": {
            "dyn_sub_algo": {"topic": "BIG/DATA"},
            "generic": {
                "log": {
                    "dir": "/tmp/logs",
                    "file": "mylog.txt",
                },
                "profile_name": "qa",
                "project_name": "Project1",
            },
        }
    }


def test_merge_simple_dicts():
    a = dict(a=1, b=1, c=1)
    b = dict(b=2, d=2)
    c = dict(c=3, e=3)

    assert config_properties.merge_dicts(a, b, c) == {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 2,
        "e": 3,
    }


def test_merge_nested_dicts():
    a = {"a": {"aa": 10, "ab": 20, "ac": {"aca": 100}}}
    b = {"a": {"ad": 30, "ac": {"aca": 200}}, "b": "top"}
    c = {"a": {"ac": {"acb": "fish"}}}
    assert config_properties.merge_dicts(a, b, c) == {
        "a": {"aa": 10, "ab": 20, "ac": {"aca": 200, "acb": "fish"}, "ad": 30},
        "b": "top",
    }


def test_ini_missing_file():
    with pytest.raises(FileNotFoundError, match="missing"):
        config_properties.parse_ini_file("missing")


def test_init_read_from_file():
    assert config_properties.parse_ini_file("example.ini") == {
        "dyn_sub_algo": {"timeout": "200", "topic": "BIG/DATA"},
        "generic": {
            "log.dir": "/tmp/logs",
            "log.file": "mylog.txt",
            "profile_name": "dev",
            "project_name": "Project1",
        },
    }


def test_ini_creates_nested_dict():
    content = """[top]
    leader = boss
    salary = 100
    
    [bottom]
    best = Malcom
    salary = 12
    # ignored
    """
    assert config_properties.ini_string_to_dict(content) == {
        "bottom": {"best": "Malcom", "salary": "12"},
        "top": {"leader": "boss", "salary": "100"},
    }


def test_can_write_dict_as_ini():
    config_dict = {
        "bottom": {"best": "Malcom", "salary": "12"},
        "top": {"leader": "boss", "salary": "100"},
    }

    expected = """[bottom]
best = Malcom
salary = 12

[top]
leader = boss
salary = 100

"""
    assert config_properties.dict_to_ini_string(config_dict) == expected
