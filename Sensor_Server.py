'''

    Author - Oliver Tattersfield

    Organisation: University Of Nottingham

Class for desciribing sensor server object that interacts with USB-CAN converter to 
extact data from configurable CAN network

'''

from Sensor_Node import sensorNode, START_PACKET, END_PACKET
from Sensors import sensor, BMP180, MPU6050

import time
from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import (
    CAN_EFF_FLAG,
    CAN_ERR_FLAG,
    CAN_RTR_FLAG,
)

# gs_usb general also can import from gs_usb_structures.py
GS_USB_ECHO_ID = 0
GS_USB_NONE_ECHO_ID = 0xFFFFFFFF
GS_USB_TIMEOUT = 10 # in ms
from gs_usb.gs_usb import (
    GS_CAN_MODE_NORMAL,
    GS_CAN_MODE_LISTEN_ONLY,
    GS_CAN_MODE_LOOP_BACK,
)

# sensor server constants
SENSOR_SERVER_CAN_ID = 0x01
SENSOR_SERVER_SEND_DELAY = 0.5 # in sceonds

SENSOR_NODE_TRANSMIT_PACKET = b"\xff\xff\xff\xff\xff\xff\xff\xff"
SENSOR_NODE_RECEIVE_PACKET = b"\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa"


class SensorServer:
    def __init__(self, sensor_nodes, baudrate):
        self.sensor_nodes = sensor_nodes # dictionary of the sensor nodes 
        self.baudrate = baudrate # data rate of CAN network
        self.timeout = GS_USB_TIMEOUT # usb timeout time in milliseconds
        self.sensor_node_command_packet = [0,0,0,0,0,0,0,0]
        # create USB connection from server to the USB-CAN converter
        usb_devices = GsUsb.scan() # find connected usb devices
        if len(usb_devices) == 0:
            print("Can not find gs_usb device\n")

        # first device is the connected USB2CAN converter
        self.usb_device = usb_devices[0]
        print(f"Baud rate: {self.baudrate} bit/s\n")
        
        # configure baud rate for USB-CAN converter
        if self.usb_device.set_bitrate(self.baudrate) == False:
            print("Baud NOT rate set for usb device\n")
        else:
            print("Baud rate set for usb device\n")
    
    def __del__(self):
        self.usb_device.stop() # drop usb connection upon deletion of object
    
    end_time = time.time()
    def start_data_loop(self):
        # Test command to be sent to development board 
        self.usb_device.start(GS_CAN_MODE_NORMAL)
        
        sensor_node_len =  len(self.sensor_nodes)
        sensor_node_count = 0

        end_time = time.time()
        
        while True:            
            current_sensor_node_id = self.sensor_nodes[sensor_node_count][0]
            current_sensor_node = self.sensor_nodes[sensor_node_count][1]
            # send out transmission frame for current sensor node
            self.sensor_node_command_packet[0] = current_sensor_node_id
            sensor_node_command_frame = GsUsbFrame( can_id=SENSOR_SERVER_CAN_ID, 
                                                    data=self.sensor_node_command_packet   )
            
            # unpack bytes for current sensor node
            # -------------------------------------------------------------------------
            iframe = GsUsbFrame()
            if self.usb_device.read(iframe, 1):
                if iframe.echo_id == GS_USB_NONE_ECHO_ID:
                    current_packet = bytes(iframe.data)
                    
                    # begin creating sensor buffer for current sensor node if start packet receievd
                    if current_packet == START_PACKET:
                        current_sensor_node.packets_flag = True
                    if current_sensor_node.packets_flag == True:
                        if current_packet == END_PACKET: # stop recording sensor buffer
                            current_sensor_node.convert_bytes()
                            current_sensor_node.packets_flag = False # reset sensor buffer and flags
                            current_sensor_node.reset_sensor_buffer()
                            sensor_node_count += 1
                            if self.usb_device.send(sensor_node_command_frame):
                                pass
                    
                        elif current_packet != START_PACKET:
                            current_sensor_node.increment_sensor_buffer( current_packet )
            # --------------------------------------------------------------------------
            


            
            '''
            # NOTE - self.usb_device.read(iframe, 1) called to prevent timeout errors on usb
            # when sending data
            # repeat loop for current sensor node for the delay time
            if time.time() - end_time >= 0:
                end_time = time.time() + SENSOR_SERVER_SEND_DELAY
                if self.usb_device.send(sensor_node_command_frame):
                    pass
                    #print(f"TX: {sensor_node_command_frame}")
            '''
            # TODO - increment sensor_node_count once full data packet from current sensor node 
            # is received
            # sensor_node_count += 1

            if sensor_node_count == sensor_node_len:
                sensor_node_count = 0  