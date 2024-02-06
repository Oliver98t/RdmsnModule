'''

Author - Oliver Tattersfield

Organisation: University Of Nottingham

Classes for desciribing real world sensors and byte order for expected data

'''

# abstract sensor class
class sensor:
    def __init__(self):
        self.name = ""
        self.byte_order = ""
        self.measurements = dict()
        self.measurements_num = None

# data classes for real world sensors
class BMP180(sensor):
    def __init__(self):
        super().__init__()
        self.name = "BMP180"
        self.byte_order = "II"
        self.measurements = {
            "temperature" : 0,
            "pressure" : 0
        }
        self.measurements_num = len(self.measurements)
       
class MPU6050(sensor):
    def __init__(self):
        super().__init__()
        self.name = "MPU6050"
        self.byte_order = "ddd"
        self.measurements = {
            "Ax" : 0,
            "Ay" : 0,
            "Az" : 0
        }
        self.measurements_num = len(self.measurements)
        
