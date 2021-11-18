# network-probe

A probe for checking the network health and reporting the health to a remote **InfluxDB** via [HTTP API](https://github.com/influxdata/influxdb-python).

Intended to be run on a ***Raspberry Pi*** connected to the target network. The software will **ping** predefined adresses inside and outside the network, with predefined freaquency, to catch connection drops. Also probes the **default DNS** to see if it has outages.

The target server is an **InfluxDB**. The data from multiple probes can be easily analyzed with [Grafana](https://grafana.com/), for example.

### Compatability Notice: ###
Older versions of ***Raspbian***, such as ***Raspbian 9 Stretch***, don't have ***Python 3.6***. **This version has legacy support for ***Python 3.5***.** This support, however **will be discontinued in the future.** In the future, you will need ***Python 3.6*** **or newer**.

This program is designed to work with ***Raspbian Stretch*** and newer and ***Windows***. Compatability with ***other Linux versions*** varies. It is dependent on the output of ```ping``` and ```traceroute``` commands.

## Features ##

- pinging predefined adresses
- crude network detection
- logging to file
- Config with config.json
  - see: example_config.json

### In progress ###

- [ ] production deployment
- [x] ~~lots of testing~~

## Install ##

### Install Python 3 on Linux ###

```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
```

### Install dependencies ###

```
pip3 install -r requirements.txt
```

### Dependencies ###

- **Python 3.5*** or newer
- [InfluxDB Python HTTP API](https://github.com/influxdata/influxdb-python)

## Config ##

configure with **config.json** file

The config part is divided in to two parts.

### Primary config ###
The first part has all the configuration you need to care about

First is the *name* of your probe and an *id*. These are used as *tags* in the data sent back to the **InfluxDB**.
```json
"name": "aProbe",
"id": 0,
```

*Targets* is the list of targets you want to ping.
```json
"targets": [
    "1.1.1.1",
    "1.0.0.1",
    "google.com"
],
```

| Key    | Default  | Explanation            |
| ----------------- | - | ------------------ |
| `"time_interval"`   | 2 | Time between pings |
| `"ping_count"`      | 1 | Times to ping per test |
| `"detection_depth"` | 3 | How meny hops from the probe are added to ping list |
| `"event_queue"`     | 15000 | How meny pings are buffered if network is interrupted. |
| `"db_name"`         | "db" | The InfluxDB name |
| `"db_user"`         | "user" | Username to log in to the InfluxDB |
| `"db_password"`     |   | the InfluxDB password |
| `"db_host"`         | "localhost" | the address to the InfluxDB. **Omit 'https:\\'** |
| `"db_port"`         | 8086 | Port used to connect to the InfluxDB |


### Message template config ###

The second part contains a template for the message body.

**YOU DO NOT NEED TO MODIFY IT**

Infact, best you leave it alone, unless you know what you're doing.

```json
  {
      "measurement": "ping",
      "tags": {
          "target": "",
          "name": "Test",
          "id": 0
      },
      "time": 0,
      "fields": {
          "up": 1
      }
  }
```

## Run ##

```
python probe.py
```

### Run on boot (Linux) ###

