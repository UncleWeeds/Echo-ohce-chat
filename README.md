# UDP Echo Server and Client (Project details)

Imagine a world without TCP. Make a network server that reverses any received string and
sends it back to the client. ( A CLI for the client will be sufficient a UI is not necessary).
Objectives:
● The client-server connection should only be over UDP sockets.

● Data transmission must be reliable and in-order byte stream (data must be sent
character by character) (refer to stop and wait protocol).

● Server should be able to handle multiple clients simultaneously.

Brownie points:

● Make the data transmission efficient by reducing the overhead of data sent to ensure
reliability and in-order transmission.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Installation

`git clone https://github.com/UncleWeeds/Echo-ohce-chat`

`cd Echo-ohce-chat`

## Basic Server & Client ( Have implemented all the objectives, the only issue is stop and wait protocol has been implemented for client -> server, not the other way around)
### Success rate - 100% (Benchmark)
### Speed - 100%(Benchmark)

Running the Basic Server
To start the basic UDP server, run:

`python server.py`

This will start the server listening on localhost:12345.

Running the Basic Client
To start the basic client, run:

`python client.py`

When prompted, enter the message you wish to send to the server.

## Advanced Server & Client

The client_Adv.py and server_Adv.py scripts enhance the basic functionality by implementing the stop-and-wait protocol for `both client -> server` and `server -> client` 
### Success rate - 95% (If it's not working try restarting the server)
### Speed - 50% (Please have patience with this, it might take a bit of time)

Running the Enhanced Server
Start the enhanced server with:

`python server_Adv.py`

Running the Enhanced Client
Start the enhanced client with:

`python client_Adv.py`

When prompted, enter the message you wish to send to the server.

# Advanced Features (Only for client -> server)

The client_brownie.py and server_brownie.py scripts enhance the basic functionality by sending data in clumps of 10 characters and compressing data during transfer.

### Success rate - 80%
### Speed - 90%

Running the Enhanced Server
Start the enhanced server with:

`python server_brownie.py`

Running the Enhanced Client
Start the enhanced client with:

`python client_brownie.py`

When prompted, enter the message you wish to send to the server.
