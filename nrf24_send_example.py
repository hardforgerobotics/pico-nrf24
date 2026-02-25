from machine import Pin, SPI
import struct
import time

from nrf24l01 import NRF24L01

csn = Pin(1, mode=Pin.OUT, value=1)  # chip select not
ce  = Pin(0, mode=Pin.OUT, value=0)  # chip enable

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    nrf = NRF24L01(SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4)), csn, ce, payload_size=32)
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()
    return nrf

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes

def send(nrf, message):
    data = message.encode("utf-8")   # convert string → bytes
    data = data + b"\x00" * (32 - len(data))
    nrf.stop_listening()             # must be in TX mode
    try:
        nrf.send(data)
    except OSError:
        print('message lost')
    

nrf = setup()
auto_ack(nrf)

message = "Temp is 30.2c"          
send(nrf, message)
