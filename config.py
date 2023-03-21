import config_properties
import config_values
import config_system


def read_overrides(file_path):
    config = config_properties.parse_properties_file(file_path)
    try:
        config_name = config['mkv']["generic"]["profile_name"]
    except KeyError:
        raise KeyError(f'Missing key mkv.generic.profile_name from {file_path}')

    if "mkv" in config:
        # reroot the config
        config = config["mkv"]

    return config_name, config


def config(config_name):
    overrides = {}
    if config_name not in config_values.ENV_CONFIG:
        config_name, overrides = read_overrides(config_name)

    return config_properties.merge_dicts(
        config_system.SYS_CONFIG[config_name],
        config_values.APP_CONFIG,
        config_values.ENV_CONFIG[config_name],
        overrides,
    )
