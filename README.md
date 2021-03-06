# network-probe

A probe for checking the network health and reporting the health to a remote **InfluxDB** via [HTTP API](https://github.com/influxdata/influxdb-python).

Intended to be run on a ***Raspberry Pi*** connected to the target network. The software will **ping** predefined adresses inside and outside the network, with predefined freaquency, to catch connection drops. Also probes the **default DNS** to see if it has outages.

The target server is an **InfluxDB**. The data from multiple probes can be easily analyzed with [Grafana](https://grafana.com/), for example.

### Compatibility: ###
> **Compatability Notice:**
> 
> **This version has legacy support for ***Python 3.5***.** This support, however **will be discontinued in the future.** In the future, you will need ***Python 3.6*** **or newer**.
> Older versions of ***Raspbian***, such as ***Raspbian 9 Stretch***, don't have ***Python 3.6***. 

This version is designed to work with ***Raspbian Stretch*** and ***Python 3.5*** and newer and ***Windows***. Compatability with ***other Linux versions*** varies. It is dependent on the output of ```ping``` and ```traceroute``` commands.

## Features ##

- pinging predefined addresses
- crude network detection
- logging to file
- Config with config.json
  - see: example_config.json

## Install ##

### Install Python 3 on Linux ###

```
$ sudo apt-get update
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

### Install dependencies ###

```
pip3 install -r requirements.txt
```

### Dependencies ###

- **Python 3.5[*](https://github.com/JValtteri/network-probe#compatibility)** or newer
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
| `"detection_depth"` | 0 | How meny hops from the probe are added to ping list |
| `"event_queue"`     | 15000 | How meny pings are buffered if network is interrupted. |
| `"db_name"`         | "db" | The InfluxDB name |
| `"db_user"`         | "user" | Username to log in to the InfluxDB |
| `"db_password"`     |   | the InfluxDB password |
| `"db_host"`         | "localhost" | the address to the InfluxDB. ```!! omit 'https:\\' !!``` |
| `"db_port"`         | 8086 | Port used to connect to the InfluxDB |

### detection_depth: ###
The probe can automatically ping devices on *path* to **1.1.1.1**. These devices may include your **router**, your **ISP** and other network infrasturcture. Can be used for a quick and dirty [*shotgun approach*](https://en.wiktionary.org/wiki/shotgun_approach).

Select the number of devices or *"hops"*, counting from the probe, you want to ping.

**Zero (0)** disables this feature. Disabling is recommended for long deployments and multiple devices. The *path* may change between restarts and mess with your data. Different probes on the same network may get different *paths* which makes their data un-comparable. See also [**notes on pinging the internet**](https://github.com/JValtteri/network-probe#notes-on-pinging-the-internet).

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
python3 probe.py
```

stop with ```Ctrl``` + ```C```

## Run on boot (Raspbian Linux) ##

**Disclaimer:**
> Included is a simple systemd service that automatically starts the probe on boot after network is up.
> Please note that both the installation script and the service itself have hardcoded paths for specific use case with Raspberry Pi.

**Assuming** 
- the OS **Raspbian Linux** and 
- user the **pi** (raspbian default user)

If you have not yet done so, clone network-probe to Pi home directory: 
```
cd /home/pi
git clone https://github.com/JValtteri/network-probe.git
```

**Run** 
```
$ install-service.sh
```

You can check the **status**, **restart** and **stop** the service with the following commands respectively.
```
$ sudo sytemctl status network-probe
$ sudo sytemctl restart network-probe
$ sudo sytemctl stop network-probe
```

## Notes on Pinging the internet ##

Note that pinging the same device or IP on any network may be interpreted by some firewalls as a [*DOS attack*](https://en.wikipedia.org/wiki/Denial-of-service_attack). In our experience, even Cloudflares **1.1.1.1** will start to **throttle** our pings after a day or two of pinging at a total *rate* of **~3 pings/s**, equivalent to six (6) devices on default settings, pinging from the same IP.
Consider using internet [**root servers**](https://en.wikipedia.org/wiki/Root_name_server) as targets for longer or larger deployments.
