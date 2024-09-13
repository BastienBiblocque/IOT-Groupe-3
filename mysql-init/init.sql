CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(255) NOT NULL,
    temperature FLOAT NOT NULL,
    measure_timestamp TIMESTAMP NOT NULL,
    sending_timestamp TIMESTAMP DEFAULT NULL
);