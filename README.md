# rubis

ADC board for 16 channels Slow Control on Raspberry pi.
This repository provides board design and control software.

<img src="https://user-images.githubusercontent.com/12980386/138100032-73b48425-1298-4935-a816-715054cd197c.png" width="400">
<img src="https://user-images.githubusercontent.com/12980386/138100048-b96825b0-636b-4689-a27d-31d813c87a6c.png" width="400">

## Feature

 - Standalone
 - Inexpensive
 - Multi channels (16 ch) and additional connectors (4 ch)

## Hardware components
 - rubis board - less than 5 dollars at elecrow 
 - [PIN Socket](https://akizukidenshi.com/catalog/g/gC-00085/) 
 - [ADC Board](https://www.marutsu.co.jp/pc/i/574270/) * 1--4 / 20 dollers per board
 - [BNC Connector](https://akizukidenshi.com/catalog/g/gC-00134/) ( * 4, optional)
 - [SMA Connector](https://akizukidenshi.com/catalog/g/gC-02569/) ( * 4, optional)
 - LEMO Connector (Optional)


## Software

### Install
Before run, enable I2C on Raspberry Pi. (`sudo raspi-config`)
Then, you can find the i2c devices like this.
```
> sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 49 4a 4b -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

If you need, run `sudo apt install libatlas-base-dev` to use `numpy` (This tool doesn't depend on `numpy`).

Then, type `pip3 install rubis`
The `rubis` binary will be provided at `~/.local/bin/rubis`


If you want database store, do like that additionaly
```
sudo apt install mariadb-server
sudo mysql -u root
MariaDB [(none)]> UPDATE mysql.user SET password=password('newpassword') WHERE User = 'root';
MariaDB [mysql]> UPDATE mysql.user SET plugin='' WHERE User='root';
MariaDB [mysql]> exit
sudo systemctl restart mysql
```


### Usage
When you execute `rubis` without option, logging immidiately starts with default configurations.
You can use your custom configuration file with `-c` option.
Some options can be overwrited with options.

`rubis -g` generates template config file.
Edit them, then run `rubis -c custom_config.json`.

`rubis -h` provides option descriptions.


### Config option

| Configure name      | Description                      | Option                                                          | Overwrite option |
| ------------------- | -------------------------------- | --------------------------------------------------------------- | ---------------- |
| `path`              | Path to store the data           | Default: "./"                                                   | -p               |
| `file_header`       | File header of generated file    | Default: "sc"                                                   | -h               |
| `naming`            | Naming style of file             | 'head-date-hash', 'head-hash', 'date-hash', 'hash', 'head-date' | -n               |
| `time_interval_sec` | Data taking time interval (sec)  | Default: 10                                                     | -t               |
| `available_boards`  | List of available ADS1115 boards | Default: [1,2,3,4]                                              |                  |
| `output`            | Output format                    | `"csv"`, `"db"`, or `"both"`                                    | -o               |
| `time_format`       | Time column format               | "timestamp", "datetime" (default), or strftime format (for example, "%H:%M:%S") |  |
| `boards`            | Setting for each ADS1115 board   | `"gain"` option is available                                    |                  |
| `sources`           | Setting for each channels        |                                                                 |                  |


The sources should be set like,
```
"1":{
    "name": "ch1",
    "description": "channel 1",
    "type": "volt"
    },
"2":{
    "name": "ch2",
    "description": "channel 2",
    "type": "linear"
    "a": 2.0,
    "b": 1.2
    },
```
The `name` is used for csv header. For the `type`, `"volt"`, `"raw"`, `"millivolt"`, and `"linear"` are available.
`"linear"` returns the value `"a" * (volt) + "b"`. The "a" and "b" should be written in the config file, for each sources.

If you set `"db"` or `"both"` for `output`, the following settings are required.
```
"db":{
    "login":{
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "newpassword",
        "autocommit": true},
    "name": "rubis"
    }
```
