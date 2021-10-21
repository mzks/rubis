import argparse
import json
from glob import glob
import pkg_resources
from rubis.core import run


def main():

    parser = argparse.ArgumentParser(description='Rubis Control tool')
    parser.add_argument('-c', '--config', default='default_config',
                        help='Config json filename with path')
    parser.add_argument('-g', '--generate_config', action='store_true',
                        help='Generate config example')
    parser.add_argument('-p', '--path', default='default',
                        help='File output path')
    parser.add_argument('-f', '--file_header', default='default')
    parser.add_argument('-n', '--naming', default='default')
    parser.add_argument('-t', '--time_interval_sec', default=0,
                        help='Time interval to collect data', type=int)

    args = parser.parse_args()

    if args.generate_config:
        config_filename = pkg_resources.resource_filename('rubis','data') + '/default_config.json'
        shutil.copyfile(config_filename, './custom_config.json')
        return

    if args.config == 'default_config':
        config_filename = pkg_resources.resource_filename('rubis','data') + '/default_config.json'
    else:
        config_filename = args.config

    with open(config_filename) as f:
        config = json.load(f)

    if args.file_header != 'default':
        config['file_header'] = args.file_header
    if args.naming != 'default':
        config['naming'] = args.naming
    if args.time_interval_sec > 0:
        config['time_interval_sec'] = args.time_interval_sec

    run(config)


if __name__ == "__main__":
    main()
