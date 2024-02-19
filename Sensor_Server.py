'''

    Author - Oliver Tattersfield

    Organisation: University Of Nottingham

Class for desciribing sensor server object that interacts with Innomaker USB-CAN converter to 
extract data from the configurable CAN network

'''

from Sensor_Node import sensorNode, START_PACKET, END_PACKET
from Sensors import sensor, BMP180, MPU6050, get_sensor

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
SENSOR_SERVER_CONFIG_SCAN_TIME = 1 # in seconds

SENSOR_SERVER_RECEIVE_STATE = 0
SENSOR_SERVER_RECEIVE_STATE = 0
SENSOR_SERVER_SEND_DELAY = 0.5 # in sceonds

# sensor node command state packets/bytes
SENSOR_NODE_WAIT_COMMAND=[171, 0, 0, 0, 0, 0, 0, 0]
SENSOR_NODE_TRANSMIT_PACKET = b"\xff\xff\xff\xff\xff\xff\xff\xff"
SENSOR_NODE_RECEIVE_STATE_PACKET = b"\xaa\xff\xaa\xff\xaa\xff\xaa\xff"



class SensorServer:
    def __init__(self, baudrate):
        self.sensor_nodes = [] # dictionary of the sensor nodes 
        self.baudrate = baudrate # data rate of CAN network
        self.timeout = GS_USB_TIMEOUT # usb timeout time in milliseconds
        self.sensor_node_command_packet = [0,0,0,0,0,0,0,0]
        # create USB connection from server to the USB-CAN converter
        usb_devices = GsUsb.scan() # find connected usb devices
        if len(usb_devices) == 0:
            print("Cannot find gs_usb device\n")

        # first device is the connected USB2CAN converter
        self.usb_device = usb_devices[0]
        print(f"Baud rate: {self.baudrate} bit/s\n")
        
        # configure baud rate for USB-CAN converter
        if self.usb_device.set_bitrate(self.baudrate) == False:
            print("Baud NOT rate set for usb device\n")
        else:
            print("Baud rate set for usb device\n")
        self.usb_device.start(GS_CAN_MODE_NORMAL)

    def __del__(self):
        self.usb_device.stop() # drop usb connection upon deletion of object

    def configure_sensor_nodes(self):
        
        end_time = time.time()
        can_id_filter = []
        # sensor configuration loop
        #-------------------------------------------------------------------------------------------
        while True:
            iframe = GsUsbFrame()
            if self.usb_device.read(iframe, 1):  
                if iframe.echo_id == GS_USB_NONE_ECHO_ID:
                    current_sensor_node_id = hex(iframe.can_id)
                    
                    if current_sensor_node_id not in can_id_filter:
                        current_sensor_node_sensors = []
                        
                        for sensor_code in iframe.data:
                            current_sensor = get_sensor(hex(sensor_code))
                            if current_sensor != 0:
                                current_sensor_node_sensors.append( current_sensor )
                        
                        can_id_filter.append( current_sensor_node_id )
                        current_sensor_node = sensorNode( sensors=current_sensor_node_sensors, can_id=current_sensor_node_id )
                        self.sensor_nodes.append( current_sensor_node )
            

            if time.time() - end_time >= SENSOR_SERVER_CONFIG_SCAN_TIME:
                end_time = time.time() + 1
                
                for sensor_node in self.sensor_nodes:
                    print(sensor_node.name)
                    for sensor in sensor_node.sensors:
                        print(sensor.name)
                    print("\n")

                self.sensor_node_command_packet = SENSOR_NODE_WAIT_COMMAND
                sensor_node_command_frame = GsUsbFrame( can_id=SENSOR_SERVER_CAN_ID, 
                                        data=self.sensor_node_command_packet   )
                self.usb_device.send(sensor_node_command_frame)
                print("Configuration scan complete.")
                break
        #-------------------------------------------------------------------------------------------



    def get_sensor_node_data(self):
        sensor_node_len =  len(self.sensor_nodes)
        sensor_node_count = 0

        # loop until data from all sensor nodes retrieved
        while True:

            current_sensor_node = self.sensor_nodes[sensor_node_count]
            current_sensor_node_id = current_sensor_node.can_id
            
            # send out transmission frame for current sensor node
            self.sensor_node_command_packet[0] = current_sensor_node_id
            sensor_node_command_frame = GsUsbFrame( can_id=SENSOR_SERVER_CAN_ID, 
                                                    data=self.sensor_node_command_packet   )
            
            

            break
            '''
            # unpack bytes for current sensor node
            # -------------------------------------------------------------------------
            iframe = GsUsbFrame()
            if self.usb_device.read(iframe, 1):
                if iframe.echo_id == GS_USB_NONE_ECHO_ID:
                    current_packet = bytes(iframe.data)
                    print(iframe)
                    if iframe.can_id == current_sensor_node_id: # filter out CAN packets  
                        if current_packet == SENSOR_NODE_RECEIVE_STATE_PACKET: # transmit state
                            self.usb_device.send(sensor_node_command_frame) # tell current node to send data

                        # begin creating sensor buffer for current sensor node if start packet receievd
                        if current_packet == START_PACKET:
                            current_sensor_node.packets_flag = True
                        if current_sensor_node.packets_flag == True:
                            if current_packet == END_PACKET: # stop recording sensor buffer
                                current_sensor_node.convert_bytes()
                                current_sensor_node.packets_flag = False # reset sensor buffer and flags
                                current_sensor_node.reset_sensor_buffer()
                                sensor_node_count += 1
                            elif current_packet != START_PACKET:
                                current_sensor_node.increment_sensor_buffer( current_packet )
            # --------------------------------------------------------------------------
            
            # finish loop when data from all sensor nodes read
            if sensor_node_count == sensor_node_len-1:
                break
        
        return self.sensor_nodes
        '''
