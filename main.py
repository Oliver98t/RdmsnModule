from Sensor_Server import SensorServer, sensorNode, BMP180, MPU6050
from time import sleep

CAN_BAUDRATE = 20000
server = SensorServer(CAN_BAUDRATE)

def main():
    
    server.configure_sensor_nodes()
    
    while True:
        sensor_nodes = server.get_sensor_node_data()
            
        for  sensor_node_id, sensor_node in sensor_nodes.items():
            print("----------------------------------------------------------")
            print(sensor_node.name)
            for sensor in sensor_node.sensors:
                print(f"\n{sensor.name}: {sensor.measurements}\n")
                
            print("----------------------------------------------------------")
        

    
    
    
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        server.close()
        
    
    