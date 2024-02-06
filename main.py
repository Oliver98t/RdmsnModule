from Sensor_Server import SensorServer, sensorNode, BMP180, MPU6050


CAN_BAUDRATE = 20000

# test data structure for sensor nodes
# TO DO - will generatoed automatically from configuration phase 
def create_sensor_nodes():
    n1_bmp180 = BMP180()
    n1_mpu6050 = MPU6050()
    node_1_sensors = [n1_bmp180, n1_mpu6050]
    node_1 = sensorNode(sensors=node_1_sensors, name="Node_1")

    n2_bmp180 = BMP180()
    n2_mpu6050 = MPU6050()
    node_2_sensors = [n2_bmp180, n2_mpu6050]
    node_2 = sensorNode(sensors=node_2_sensors, name="Node_2") 
                            

    nodes = [
        (0x20, node_1),
        (0x30, node_2)
    ]

    return nodes

sensor_nodes = create_sensor_nodes()
server1 = SensorServer(sensor_nodes, CAN_BAUDRATE)

def main():
    server1.start_data_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        del server1
    
    