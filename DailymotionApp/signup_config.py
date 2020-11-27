from configparser import ConfigParser
import logging


def read_config(section):
    # create parser and read ini configuration file
    filename = 'config.ini'
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return config