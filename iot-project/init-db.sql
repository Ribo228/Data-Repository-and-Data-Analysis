CREATE TABLE smart (
id SERIAL PRIMARY KEY,
device_id VARCHAR(255),
date_time TIMESTAMP DEFAULT current_timestamp,
data jsonb
);

CREATE INDEX date_time_indx ON smart (date_time);
