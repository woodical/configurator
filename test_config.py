from pprint import pp

import pytest
import config_properties
import config


def test_merged_config_dicts():
    actual = config.config("qa")
    expected = {
        "postgres": {"db_host": "host-qa", "db_port": 200},
        "prometheus": {"port": 5790},
        "sub_dyn_alog_prices": {"timeout": 100, "topic": "SOW/PRICES"},
        "sub_dyn_inventory": {"timeout": 1200, "topic": "SOW/INVENTORY"},
    }

    print(config_properties.dict_to_ini_string(actual))
    print(config_properties.dict_to_properties_string(actual, prefix="mkv."))
    assert actual == expected


def test_missing_overrides():
    with pytest.raises(FileNotFoundError, match="(?i)no such file .*missing.jinit"):
        config.config("missing.jinit")


def test_empty_overrides():
    with pytest.raises(KeyError, match="(?i)missing key mkv.generic.profile_name"):
        config.config("empty.jinit")


def test_merged_config_dicts_from_file():
    actual = config.config("example.jinit")
    expected = {
        "dyn_sub_algo": {"topic": "BIG/DATA"},
        "generic": {
            "log": {"dir": "/tmp/logs", "file": "mylog.txt"},
            "profile_name": "qa",
            "project_name": "Project1",
        },
        "postgres": {"db_host": "host-qa", "db_port": 200},
        "prometheus": {"port": 5790},
        "sub_dyn_alog_prices": {"timeout": 100, "topic": "SOW/PRICES"},
        "sub_dyn_inventory": {"timeout": 1200, "topic": "SOW/INVENTORY"},
    }

    # print(config_properties.dict_to_properties_string(actual, prefix="mkv."))
    # print(config_properties.dict_to_properties_string(expected, prefix="mkv."))
    assert actual == expected
