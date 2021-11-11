import os, re, ast
import argparse
import json
from glob import glob
import shutil
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
    parser.add_argument('-i', '--rubis_id', default='default',
                        help='Rubis ID')
    parser.add_argument('-d', '--delimiter', default='default',
                        help='Delimiter for csv output')
    parser.add_argument('-f', '--file_header', default='default')
    parser.add_argument('-n', '--naming', default='default')
    parser.add_argument('-o', '--output', default='default')
    parser.add_argument('-t', '--time_interval_sec', default=0,
                        help='Time interval to collect data', type=int)
    parser.add_argument('-v', '--version', action='store_true')

    args = parser.parse_args()

    if args.version:
        PACKAGE_NAME = 'rubis'
        with open(os.path.join(PACKAGE_NAME, '__init__.py')) as f:
            match = re.search(r'__version__\s+=\s+(.*)', f.read())
        version = str(ast.literal_eval(match.group(1)))
        print('rubis version : ' + version)
        return

    if args.generate_config:
        config_filename = pkg_resources.resource_filename('rubis','data') + '/default_config.json'
        shutil.copyfile(config_filename, './custom_config.json')
        return

    if args.config == 'default_config':
        config_filename = pkg_resources.resource_filename('rubis','data') + '/default_config.json'
    else:
        config_filename = pkg_resources.resource_filename('rubis','data') + '/' + args.config
        if os.path.exists(config_filename):
            pass
        else:
            config_filename = args.config
    print('Use config ' + config_filename)

    with open(config_filename) as f:
        config = json.load(f)
    if args.path != 'default':
        config['path'] = args.path
    if config['path'][-1] != '/':
        config['path'] = config['path'] + '/'
    if args.file_header != 'default':
        config['file_header'] = args.file_header
    if args.naming != 'default':
        config['naming'] = args.naming
    if args.output != 'default':
        config['output'] = args.output
    if args.rubis_id != 'default':
        config['rubis_id'] = args.rubis_id
    if args.delimiter == 'space':
        config['delimiter'] = ' '
    elif args.delimiter != 'default':
        config['delimiter'] = args.delimiter
    if config['delimiter'] == 'space':
        config['delimiter'] = ' '
    if args.time_interval_sec > 0:
        config['time_interval_sec'] = args.time_interval_sec

    run(config)


if __name__ == "__main__":
    main()
