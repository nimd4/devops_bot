CREATE TABLE replication_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action TEXT,
    details TEXT
);

INSERT INTO replication_logs(action, details)
VALUES
('START', 'Replication initialized');

CREATE TABLE test_table(
    id SERIAL PRIMARY KEY,
    message TEXT
);

INSERT INTO test_table(message)
VALUES
('Hello PostgreSQL');
