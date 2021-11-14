# network-probe

A probe for checking the network health and reporting the health to a remote **InfluxDB** via [HTTP API](https://github.com/influxdata/influxdb-python).

Intended to be run on a Raspberry Pi connected to the target network. The software will **ping** predefined adresses inside and outside the network, with predefined freaquency, to catch connection drops. Also probes the **default DNS** to see if it has outages.

The target server is an **InfluxDB**. The data from multiple probes can be easily analyzed with [Grafana](https://grafana.com/), for example.

## Features ##

- pinging predefined adresses
- crude network detection
- logging to file
- Config with config.json

### In progress ###

- ~~Config with config.json~~
  - ~~Example config~~
- Implementing **[InfluxDB HTTP API](https://github.com/influxdata/influxdb-python)**
- lots of testing

## Install ##

### Dependencies ###

[HTTP API](https://github.com/influxdata/influxdb-python)

## Config ##

configure with **config.json** file

## Run ##

### Run on boot (Linux) ###
