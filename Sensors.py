'''

Author - Oliver Tattersfield

Organisation: University Of Nottingham

Classes for desciribing real world sensors and byte order for expected data

'''
# sensor codes
MPU6050_CODE="0x1"
BMP180_CODE="0x2"
DS3231_CODE="0x3"

MEASUREMENT_FIELD_INDEX = 0
MEASUREMENT_VALUE_INDEX = 1

# abstract sensor class
class sensor:
    def __init__(self):
        self.sensor_id = None
        self.name = ""
        self.byte_order = ""
        self.measurements = []
        self.measurements_num = None

# data classes for real world sensors
class BMP180(sensor):
    def __init__(self):
        super().__init__()
        self.sensor_id = "0x02"
        self.name = "BMP180"
        self.byte_order = "fi"
        self.measurements = [
            ["temperature" , 0],
            ["pressure" , 0],
            ["timestamp", None]
        ]
        self.measurements_num = len(self.measurements)
       
class MPU6050(sensor):
    def __init__(self):
        super().__init__()
        self.sensor_id = "0x01"
        self.name = "MPU6050"
        self.byte_order = "hhhhhhf"
        self.measurements = [
            ["Ax" , 0],
            ["Ay" , 0],
            ["Az" , 0],
            ["Gx" , 0],
            ["Gy" , 0],
            ["Gz" , 0],
            ["temperature" , 0],
            ["timestamp", None]
        ]
        self.measurements_num = len(self.measurements)

class DS3231(sensor):
    def __init__(self):
        super().__init__()
        self.sensor_id = "0x03"
        self.name = "DS3231"
        self.byte_order = "fxxxx" # when padding and byte string for unpacking data includes endianess char, x represents 1 byte
        self.measurements = [
            ["temperature" , 0],
            ["timestamp", None]
        ]
        self.measurements_num = len(self.measurements)

def get_sensor(code):
    if code == MPU6050_CODE:
        return MPU6050()
    elif code == BMP180_CODE:
        return BMP180()
    elif code == DS3231_CODE:
        return DS3231()
    else:
        return 0

if __name__ == "__main__":
    measurements = {
            "Ax" : 0,
            "Ay" : 0,
            "Az" : 0,
            "timestamp": None
        }
    