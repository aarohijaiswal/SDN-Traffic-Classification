# SDN Traffic Classification System

## Project Description

This project implements a Software Defined Networking (SDN) based Traffic Classification System using Mininet and POX controller. The system classifies network traffic into TCP, UDP, and ICMP protocols.

## Objectives

* Identify TCP, UDP, ICMP packets
* Maintain statistics
* Display classification results
* Analyze traffic distribution

## Setup Instructions

1. Install Mininet and POX
2. Run controller:
   ./pox.py log.level --DEBUG traffic_classification
3. Run Mininet:
   sudo mn --controller=remote,ip=127.0.0.1 --topo=single,3

## Testing

* pingall → ICMP traffic
* iperf → TCP traffic
* iperf -u → UDP traffic

## Output

Controller displays packet type and statistics.

## Author

Aarohi Jaiswal
