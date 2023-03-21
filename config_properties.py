import configparser
import io


def parse_properties_file(file_path: str):
    """
    Parses a Java properties *like* file and returns a dictionary with the properties.
    """
    with open(file_path, "r") as f:
        return properties_string_to_dict(f.read())


def properties_string_to_dict(content: str):
    # remove BOM if present
    content = content.lstrip("\ufeff")

    # split content into lines
    lines = content.split("\n")

    # parse properties
    properties = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # create nested dictionaries for keys with dots
        key_parts = key.split(".")

        current_dict = properties
        for i, key_part in enumerate(key_parts):
            if i == len(key_parts) - 1:
                # last key, assign value
                current_dict[key_part] = value
            else:
                current_dict.setdefault(key_part, {})
            current_dict = current_dict[key_part]

    return properties


def merge_dicts(*dicts):
    """
    Merge multiple dictionaries recursively.
    """
    result = {}
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = merge_dicts(result.get(k, {}), v)
            else:
                result[k] = v
    return result


def parse_ini_file(file_path):
    with open(file_path) as fh:
        return ini_string_to_dict(fh.read())


def ini_string_to_dict(content):
    config = configparser.ConfigParser()
    config.read_string(content)

    config_dict = {}
    for section in config.sections():
        config_dict[section] = dict(config.items(section))

    return config_dict


def dict_to_ini_file(config_dict, output_fh):
    config = configparser.ConfigParser()
    config.read_dict(config_dict)
    config.write(output_fh)


def dict_to_ini_string(config_dict):
    out = io.StringIO()
    dict_to_ini_file(config_dict, out)
    return out.getvalue()


def dict_to_properties_file(config_dict, output_fh):
    with output_fh:
        output_fh.write(dict_to_properties_string(config_dict))


def dict_to_properties_string(properties_dict, prefix=""):
    """Convert a nested dictionary to Java properties format."""
    properties = ""
    for key, value in sorted(properties_dict.items()):
        if isinstance(value, dict):
            # Recursively convert nested dictionaries
            nested_prefix = f"{prefix}{key}."
            properties += dict_to_properties_string(value, nested_prefix)
        else:
            # Flatten keys and append to properties string
            flat_key = f"{prefix}{key}"
            properties += f"{flat_key}={str(value)}\n"
    return properties


