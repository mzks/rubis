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
 - [ADC Board](https://www.marutsu.co.jp/pc/i/574270/) * 1--4
 - [BNC Connector](https://akizukidenshi.com/catalog/g/gC-00134/) ( * 4, optional)
 - [SMA Connector](https://akizukidenshi.com/catalog/g/gC-02569/) ( * 4, optional)
 - LEMO Connector (Optional)


## Software

### Install
Before run, enable I2C on Raspberry Pi. (`sudo raspi-config`)
Then, type `pip install rubis`
The `rubis` binary will be provided at `~/.local/bin/rubis`


### Usage
When you execute `rubis` without option, default configurations will be used.
You can use your custom configuration file with `-f` option.
Some options can be overwrited with options.

`rubis -g` generates template config file.
Edit them, then run `rubis -c custom_config.json`.


### Config option
| Configure name    | Description                      | Option                                                          | Overwrite option |
| ----------------- | -------------------------------- | --------------------------------------------------------------- | ---------------- |
| `path`             | Path to store the data           | Default: "./"                                                   | -p               |
| `file_header`       | File header of generated file    | Default: "sc"                                                   | -h               |
| `naming`            | Naming style of file             | 'head-date-hash', 'head-hash', 'date-hash', 'hash', 'head-date' | -n               |
| `time_interval_sec` | Data taking time interval (sec)  | Default: 10                                                     | -t               |
| `available_boards`  | List of available ADS1115 boards | Default: [1,2,3,4]                                              |                  |
| `time_format`  | Time column format | "timestamp", "datetime" (default), or strftime format (for example, "%H:%M:%S")                                              |                  |
| `sources`           | Setting for each channels        |                                                                 |                  |

The sources should be set like,
```
"1":{
    "name": "ch1",
    "description": "channel 1",
    "type": "raw"
    },
```
The `name` is used for csv header. For the `type`, `"raw"`, `"millivolt"`, and `"volt"` are available.

