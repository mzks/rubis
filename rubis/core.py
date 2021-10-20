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
    for ads in adss:
        ads.gain = 1
        chs.append(AnalogIn(ads, ADS.P0))
        chs.append(AnalogIn(ads, ADS.P1))
        chs.append(AnalogIn(ads, ADS.P2))
        chs.append(AnalogIn(ads, ADS.P3))

    names, types = [], []
    for board_id in config['available_boards']:
        for ch in range(4):
            ch_id = str((int(board_id) - 1) * 4 + ch + 1)
            names.append(config['sources'][ch_id]['name'])
            types.append(config['sources'][ch_id]['type'])

    print('Data taking...')

    while True:
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        timestamp = int(now.timestamp())
        outfilename = get_outfilename(config, config_hash, date)

        # File existance check
        if not os.path.isfile(outfilename):
            with open(outfilename, mode='a') as f:
                f.write('timestamp')
                for name in names:
                    f.write(',' + name)
                f.write('\n')
                

        with open(outfilename, mode='a') as f:
            f.write(str(timestamp))
            for ch, typ in zip(chs, types):
                if typ == 'raw':
                    f.write(','+"{:>5}".format(ch.value))
                if typ == 'volt':
                    f.write(','+"{:>5.3f}".format(ch.voltage))
            f.write('\n')

        time.sleep(config['time_interval_sec'])


def get_outfilename(config, config_hash, date):

    if config['naming'] == "head-date-hash":
        outfilename = config['file_header'] + "-" + date + "-" + config_hash + ".txt"
    if config['naming'] == "date-hash":
        outfilename = date + "-" + config_hash + ".txt"
    if config['naming'] == "hash":
        outfilename = config_hash + ".txt"
    return outfilename
