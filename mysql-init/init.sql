CREATE TABLE IF NOT EXISTS sensor_data (
    sensor_id VARCHAR(255) NOT NULL,
    temperature FLOAT NOT NULL,
    measure_timestamp TIMESTAMP NOT NULL,
    sending_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
