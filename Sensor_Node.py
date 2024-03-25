'''

Author - Oliver Tattersfield

Organisation: University Of Nottingham

Class for describing sensor node on the RDMSN

'''

from Sensors import BMP180, MPU6050
from struct import unpack, pack
from datetime import datetime


# start and finish packets to define start/finish of incomcing buffer over CAN
START_PACKET = b'\xff\x00\x00\x00\x00\x00\x00\x00'
END_PACKET = b'\xaa\x00\x00\x00\x00\x00\x00\x00'

# buffer status codes
INCORRECT_BUFFER = 0
CORRECT_BUFFER = 1

# define endianess of current platform
BIG_ENDIAN = '>'
LITTLE_ENDIAN = '<'

# sensor macros
TIME_STAMP_INDEX = -1
TIME_STAMP_VALUE_INDEX = -1
MEASUREMENT_VALUE_INDEX = 1



# functions to convert bytes to readable values over CAN bus
class sensorNode:
    def __init__(self, sensors, can_id):
        self.name = f"Node_{can_id}"
        self.can_id = can_id
        self.sensors = sensors
        self.sensor_buffer = bytes()
        self.byte_order = ""
        self.packets_flag = False
        # attributes for writing to csv files
        self.csv_field_flag = False
        self.csv_fields = [] 
        self.csv_measurements = []
        for sensor in self.sensors:
            self.byte_order += sensor.byte_order

    def convert_bytes(self):
        try:
            measurements = unpack(f'{LITTLE_ENDIAN}{self.byte_order}', self.sensor_buffer)
            previous_sensor_slice = 0
            single_value = False        

            for sensor in self.sensors:
                # -1 from total sensor measurements to exclude timestamp 
                current_sensor_slice = sensor.measurements_num - 1
                
                if current_sensor_slice == 1:
                    current_measurements = tuple([measurements[previous_sensor_slice]])
                    previous_sensor_slice = current_sensor_slice
                    single_value = True
                else:
                    current_measurements = measurements[previous_sensor_slice:previous_sensor_slice+current_sensor_slice]
                    if single_value == True:
                        previous_sensor_slice = current_sensor_slice+1
                        single_value = False
                    else:
                        previous_sensor_slice = current_sensor_slice

                for measurement_index, current_measurement in enumerate(current_measurements):
                    sensor.measurements[measurement_index][MEASUREMENT_VALUE_INDEX] = round(current_measurement, ndigits=3)
                          
                sensor.measurements[TIME_STAMP_INDEX][TIME_STAMP_VALUE_INDEX] = str(datetime.now())
            return CORRECT_BUFFER
        except:
            return INCORRECT_BUFFER
        
    def reset_sensor_buffer(self):
        self.sensor_buffer = bytes()

    def increment_sensor_buffer(self, add_buffer):
        self.sensor_buffer += add_buffer

    def get_sensor_buffer(self):
        return self.sensor_buffer

    def reset_byte_order(self):
        self.byte_order = ""
        

# test class functions
if __name__ == '__main__':
    
    print(str(datetime.now()))
    

    



