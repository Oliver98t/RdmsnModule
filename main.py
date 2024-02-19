from Sensor_Server import SensorServer, sensorNode, BMP180, MPU6050


CAN_BAUDRATE = 20000

'''
# test data structure for sensor nodes
# TO DO - will generatoed automatically from configuration phase 
def create_sensor_nodes():
    n1_bmp180 = BMP180()
    n1_mpu6050 = MPU6050()
    node_1_sensors = [n1_bmp180, n1_mpu6050]
    node_1 = sensorNode(sensors=node_1_sensors, name="Node_1", CAN_ID=0x20)

    n2_bmp180 = BMP180()
    n2_mpu6050 = MPU6050()
    node_2_sensors = [n2_bmp180, n2_mpu6050]
    node_2 = sensorNode(sensors=node_2_sensors, name="Node_2", CAN_ID=0x30) 
                            

    nodes = [node_1, node_2]

    return nodes

sensor_nodes = create_sensor_nodes()
'''

server = SensorServer(CAN_BAUDRATE)

def main():
    server.configure_sensor_nodes()
    print(server.sensor_nodes)
    while True:
        server.get_sensor_node_data()
    '''
    while True:
        sensor_nodes = server1.get_sensor_node_data()
        for sensor in sensor_nodes[0].sensors:
            print(f"\n{sensor.name}: {sensor.measurements}\n")
        
        for sensor_node in sensor_nodes:
            print(sensor_node.name)
            for sensor in sensor_node.sensors:
                print(f"{sensor.name}: {sensor.measurements}")
            print("\n")
        #'''
        

if __name__ == "__main__":
    try:
        main()
        del server
    except KeyboardInterrupt:
        del server
    
    