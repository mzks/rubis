import os, sys
import socket
import time
import datetime
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from rubis.hash import deterministic_hash


def run(config):

    config_hash = deterministic_hash(config, 6)
    config_json = open(config['path'] + config_hash + ".json", "w")
    json.dump(config, config_json, indent = 4)
    config_json.close()

    i2c = busio.I2C(board.SCL, board.SDA)
    # Four boards are inplemented (ADDR <-> GND, Vdd, SDA, SCL)
    board_address = {"1": 0x48, "2": 0x49, "3": 0x4A, "4": 0x4B}
    try:
        adss = [ADS.ADS1115(i2c, address=board_address[str(board_id)]) for board_id in config['available_boards']]
        chs = []
        for ads, board_id in zip(adss, config['available_boards']):
            ads.gain = config['boards'][str(board_id)]['gain']
            chs.append(AnalogIn(ads, ADS.P0))
            chs.append(AnalogIn(ads, ADS.P1))
            chs.append(AnalogIn(ads, ADS.P2))
            chs.append(AnalogIn(ads, ADS.P3))
    except:
        print('Please check your ADC boards availavility')
        print("See 'available_boards' configuration or '-a'")

    sources, ch_str = [], []
    for board_id in config['available_boards']:
        for ch in range(4):
            ch_id = str((int(board_id) - 1) * 4 + ch + 1)
            ch_str.append(ch_id)
            sources.append(config['sources'][ch_id])

    print('Data taking on the hash '+config_hash)

    ocsv, odb = True, False
    if config['output'] == 'db':
        ocsv, odb = False, True
    if config['output'] == 'both':
        ocsv, odb = True, True
    if odb:
        import pymysql.cursors
        conn = pymysql.connect(**config['db']['login'])
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + config['db']['name'])
        cursor.execute("USE " + config['db']['name'])
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS data (id INT AUTO_INCREMENT, 
                        time TIMESTAMP not null default CURRENT_TIMESTAMP, 
                        ch1 FLOAT, ch2 FLOAT, ch3 FLOAT, ch4 FLOAT, ch5 FLOAT, ch6 FLOAT,
                        ch7 FLOAT, ch8 FLOAT, ch9 FLOAT, ch10 FLOAT, ch11 FLOAT, ch12 FLOAT,
                        ch13 FLOAT, ch14 FLOAT, ch15 FLOAT, ch16 FLOAT, hash VARCHAR(6), 
                        rubis_id VARCHAR(10), log_time DATETIME,
                        PRIMARY KEY (id))
                        ''')
        sql = ('''
                INSERT INTO data (log_time, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10,
                ch11, ch12, ch13, ch14, ch15, ch16, hash, rubis_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ''')
        
    delim = config['delimiter']
    commentout_string = config['commentout_string']

    while True:
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        if config['time_format'] == 'timestamp':
            time_str = str(int(now.timestamp()))
        elif config['time_format'] == 'datetime':
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = now.strftime(config['time_format'])
            
        if ocsv:
            outfilename = get_outfilename(config, config_hash, date)
            # File existance check
            if not os.path.isfile(outfilename):
                with open(outfilename, mode='a') as f:
                    f.write(commentout_string+'time')
                    for source in sources:
                        f.write(delim + source['name'])
                    f.write('\n')
            with open(outfilename, mode='a') as f:
                f.write(time_str)

        if odb:
            db_data = [now.strftime("%Y-%m-%d %H:%M:%S")]+["0"]*16+[config_hash,config['rubis_id']]

        for ch, s, ch_st in zip(chs, sources, ch_str):
            value = ch.value
            volt = ch.voltage
            if ocsv:
                with open(outfilename, mode='a') as f:
                    if s['type'] == 'raw':
                        f.write(delim+"{:>5}".format(value))
                    elif (s['type'] == 'volt') or (s['type'] == 'V'):
                        f.write(delim+"{:>5.7f}".format(volt))
                    elif s['type'] == 'millivolt' or (s['type'] == 'mV'):
                        f.write(delim+"{:>5.4f}".format(volt*1.e3))
                    elif s['type'] == 'linear':
                        f.write(delim+"{:>5.4f}".format(volt*s['a']+s['b']))
                    else:
                        f.write(delim)
            if odb:
                if s['type'] == 'raw':
                    db_data[int(ch_st)] = "{:>5}".format(value)
                elif (s['type'] == 'volt') or (s['type'] == 'V'):
                    db_data[int(ch_st)] = "{:>5.7f}".format(volt)
                elif s['type'] == 'millivolt' or (s['type'] == 'mV'):
                    db_data[int(ch_st)] = "{:>5.4f}".format(volt*1.e3)
                elif s['type'] == 'linear':
                    db_data[int(ch_st)] = "{:>5.4f}".format(volt*s['a']+s['b'])


        if ocsv:
            with open(outfilename, mode='a') as f:
                f.write('\n')
        if odb:
            cursor.execute(sql, tuple(db_data))

        time.sleep(config['time_interval_sec'])


def get_outfilename(config, config_hash, date):

    outfilename = ''
    c = 0
    while c < len(config['naming']):
        if config['naming'][c:c+4] == 'head':
            outfilename += config['file_header']
            c += 4
        elif config['naming'][c:c+4] == 'date':
            outfilename += date
            c += 4
        elif config['naming'][c:c+4] == 'hash':
            outfilename += config_hash
            c += 4
        elif config['naming'][c:c+4] == 'host':
            outfilename += socket.gethostname()
            c += 4
        elif config['naming'][c:c+2] == 'id':
            outfilename += config['rubis_id']
            c += 2
        else:
            outfilename += config['naming'][c]
            c += 1

    outfilename = config['path'] + outfilename    
    return outfilename
