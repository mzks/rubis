import os, sys
import time
import datetime

import numpy as np
import pandas as pd
import json

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from rubis.hash import deterministic_hash

def run(config):

    config_hash = deterministic_hash(config, 6)
    config_json = open(config_hash+".json", "w")
    json.dump(config, config_json, indent = 4)
    config_json.close()

    i2c = busio.I2C(board.SCL, board.SDA)
    # Four boards are inplemented (ADDR <-> GND, Vdd, SDA, SCL)
    board_address = {"1": 0x48, "2": 0x49, "3": 0x4A, "4": 0x4B}

    adss = [ADS.ADS1115(i2c, address=board_address[str(board_id)]) for board_id in config['available_boards']]
    chs = []
    for ads, board_id in zip(adss, config['available_boards']):
        ads.gain = config['boards'][str(board_id)]['gain']
        chs.append(AnalogIn(ads, ADS.P0))
        chs.append(AnalogIn(ads, ADS.P1))
        chs.append(AnalogIn(ads, ADS.P2))
        chs.append(AnalogIn(ads, ADS.P3))

    sources = []
    for board_id in config['available_boards']:
        for ch in range(4):
            ch_id = str((int(board_id) - 1) * 4 + ch + 1)
            sources.append(config['sources'][ch_id])

    print('Data taking on the hash '+config_hash)

    while True:
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        if config['time_format'] == 'timestamp':
            time_str = str(int(now.timestamp()))
        elif config['time_format'] == 'datetime':
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = now.strftime(config['time_format'])
            
        outfilename = get_outfilename(config, config_hash, date)

        # File existance check
        if not os.path.isfile(outfilename):
            with open(outfilename, mode='a') as f:
                f.write('time')
                for source in sources:
                    f.write(',' + source['name'])
                f.write('\n')
                

        with open(outfilename, mode='a') as f:
            f.write(time_str)
            for ch, s in zip(chs, sources):
                if s['type'] == 'raw':
                    f.write(','+"{:>5}".format(ch.value))
                elif (s['type'] == 'volt') or (s['type'] == 'V'):
                    f.write(', '+"{:>5.7f}".format(ch.voltage))
                elif s['type'] == 'millivolt' or (s['type'] == 'mV'):
                    f.write(', '+"{:>5.4f}".format(ch.voltage*1.e3))
                elif s['type'] == 'linear':
                    f.write(', '+"{:>5.4f}".format(ch.voltage*s['a']+s['b']))
                else:
                    f.write(', ')
            f.write('\n')

        time.sleep(config['time_interval_sec'])


def get_outfilename(config, config_hash, date):

    if config['naming'] == "head-date-hash":
        outfilename = config['file_header'] + "-" + date + "-" + config_hash + ".txt"
    elif config['naming'] == "head-date":
        outfilename = config['file_header'] + "-" + date + ".txt"
    elif config['naming'] == "head-hash":
        outfilename = config['file_header'] + "-" + config_hash + ".txt"
    elif config['naming'] == "date-hash":
        outfilename = date + "-" + config_hash + ".txt"
    elif config['naming'] == "hash":
        outfilename = config_hash + ".txt"
    return outfilename
