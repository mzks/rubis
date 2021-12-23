import os
import re
import argparse
import json
import shutil
import pkg_resources

from rubis.core import run, add_log, show_log


def read_jsonc(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    re_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
    json_obj = json.loads(re_text)
    return json_obj


def main():

    parser = argparse.ArgumentParser(description='Rubis Control tool')
    parser.add_argument('-c', '--config', default='default_config', help='Config json filename with path')
    parser.add_argument('-g', '--generate_config', action='store_true', help='Generate config example')
    parser.add_argument('-t', '--time_interval_sec', default=0., help='Time interval to collect data', type=float)
    parser.add_argument('-o', '--output', default='default', choices=['default', 'csv', 'db', 'both'],
                        help='Output style (file or database)')
    parser.add_argument('-p', '--path', default='default', help='File output path')
    parser.add_argument('-n', '--naming', default='default',
                        help='File naming style e.g., date-hash-id.csv etc.')
    parser.add_argument('-f', '--file_header', default='default', help='File header')
    parser.add_argument('-i', '--rubis_id', default='default', help='Rubis ID')
    parser.add_argument('-d', '--delimiter', default='default', help='Delimiter for csv output')
    parser.add_argument('-a', '--available_boards', default=[], type=int, nargs='+',
                        help='Available board numbers e.g., -a 1 3')
    parser.add_argument('-r', '--dryrun', action='store_true', help='Generate dummy files even not on RaspPi.')
    parser.add_argument('-b', '--booked', default=None, help='Find configure file booked.')
    parser.add_argument('-s', '--stored', action='store_true', help='Use the previous configuration stored')
    parser.add_argument('-l', '--log', action='store_true', help='Show all log')
    parser.add_argument('-q', '--quit', action='store_true', help='Kill all running rubis')
    parser.add_argument('-v', '--version', action='store_true')
    # ejkmquwxyz

    args = parser.parse_args()
    version = '1.0.1'
    if args.version:
        print('rubis version : ' + version)
        return

    if args.quit:
        import psutil
        pids = psutil.pids()
        self_pid = os.getpid()
        for pid in pids:
            if pid == self_pid:
                continue
            try:
                p = psutil.Process(pid)
                cmd = ''.join(p.cmdline())
                if (cmd.find('rubis') != -1) & (cmd.find('rubis-q') == -1):
                    p.kill()
                    add_log('Killed PID: ' + str(pid))
            except:
                pass
        return

    if args.log:
        show_log()
        return

    if args.booked != None:
        config_filename = pkg_resources.resource_filename('rubis', 'data') + '/' + args.booked + '.json'
        if os.path.exists(config_filename):
            shutil.copyfile(config_filename, './'+args.booked+'.json')
        else:
            print(args.booked + '.json does not exist. Nothing to do.')
        return

    if args.generate_config:
        config_filename = pkg_resources.resource_filename('rubis', 'data') + '/default_config.json'
        if os.path.exists('./custom_config.json'):
            print('custom_config.json exists in this directory. Nothing to do.')
            return
        shutil.copyfile(config_filename, './custom_config.json')
        return

    if args.config == 'default_config':
        config_filename = pkg_resources.resource_filename('rubis', 'data') + '/default_config.json'
    else:
        config_filename = pkg_resources.resource_filename('rubis', 'data') + '/' + args.config
        if os.path.exists(config_filename):
            pass
        else:
            config_filename = args.config

    if args.stored:
        config_filename = pkg_resources.resource_filename('rubis', 'data') + '/.previous_config.json'
        if os.path.exists(config_filename):
            pass
        else:
            config_filename = pkg_resources.resource_filename('rubis', 'data') + '/default_config.json'

    print('Use config ' + config_filename)

    config = read_jsonc(config_filename)
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
    if args.available_boards:
        config['available_boards'] = args.available_boards
    if args.delimiter == 'space':
        config['delimiter'] = ' '
    elif args.delimiter != 'default':
        config['delimiter'] = args.delimiter
    if config['delimiter'] == 'space':
        config['delimiter'] = ' '
    if args.time_interval_sec > 0:
        config['time_interval_sec'] = args.time_interval_sec

    filename = pkg_resources.resource_filename('rubis', 'data') + '/.previous_config.json'
    config_json = open(filename, "w")
    json.dump(config, config_json, indent=4)
    config_json.close()

    run(config, args.dryrun)


if __name__ == "__main__":
    main()
