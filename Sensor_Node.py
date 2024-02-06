'''

Author - Oliver Tattersfield

Organisation: University Of Nottingham

Class for describing sensor node on the RDMSN

'''

from Sensors import BMP180, MPU6050
from struct import unpack

# start and finish packets to define start/finish of incomcing buffer over CAN
START_PACKET = b'\xff\x00\x00\x00\x00\x00\x00\x00'
END_PACKET = b'\xaa\x00\x00\x00\x00\x00\x00\x00'

# buffer status codes
INCORRECT_BUFFER = 0
CORRECT_BUFFER = 1

# define endianess of current platform
BIG_ENDIAN = '<'
LITTLE_ENDIAN = '>'

# functions to convert bytes to readable values over CAN bus
class sensorNode:
    def __init__(self, sensors, name: str):
        self.name = name
        self.sensors = sensors
        self.sensor_buffer = bytes()
        self.byte_order = ""
        self.packets_flag = False
        for sensor in self.sensors:
            self.byte_order += sensor.byte_order
       
    def convert_bytes(self):
        try: 
            measurements = unpack(f'{BIG_ENDIAN}{self.byte_order}', self.sensor_buffer)
            previous_sensor_slice = 0
            print(self.name)
            for sensor in self.sensors:
                current_sensor_slice = sensor.measurements_num
                current_measurements = measurements[previous_sensor_slice:previous_sensor_slice+current_sensor_slice]
                
                for index, measurement_key in enumerate(sensor.measurements):
                    sensor.measurements[measurement_key] = current_measurements[index]
                
                print( sensor.measurements )
                previous_sensor_slice = current_sensor_slice
            print("\n\n")
            return CORRECT_BUFFER
        except: # incorrect buffer case
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
    x = '0x20'
    print(x.encode())
    measurements = {
    "temperature" : 10,
    "pressure" : 40
    }

    for i,m in enumerate(measurements):
        print(i)
        print(m)