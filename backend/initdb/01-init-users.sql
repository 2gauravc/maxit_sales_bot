-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,    -- 'Team Lead' or 'RM'
    base_location TEXT NOT NULL
);

-- Insert Team Leads
INSERT INTO users (user_id, name, email, role, base_location) VALUES
('tl2001', 'Laura Schneider', 'laura.schneider@maxit.dev', 'Team Lead', 'Berlin'),
('tl2002', 'Rajeev Nair', 'rajeev.nair@maxit.dev', 'Team Lead', 'Mumbai'),
('tl2003', 'Chen Lei', 'chen.lei@maxit.dev', 'Team Lead', 'Hong Kong'),
('tl2004', 'Amanda Blake', 'amanda.blake@maxit.dev', 'Team Lead', 'New York');

-- Insert Relationship Managers
INSERT INTO users (user_id, name, email, role, base_location) VALUES
('u1001', 'Ankit Mehra', 'ankit.mehra@maxit.dev', 'RM', 'Munich'),
('u1002', 'Wei Ling', 'wei.ling@maxit.dev', 'RM', 'Shanghai'),
('u1003', 'Sofia Martinez', 'sofia.martinez@maxit.dev', 'RM', 'Madrid'),
('u1004', 'Tomoko Saito', 'tomoko.saito@maxit.dev', 'RM', 'Tokyo'),
('u1005', 'Fatima Al-Farsi', 'fatima.alfarsi@maxit.dev', 'RM', 'Dubai'),
('u1006', 'Lucas Dubois', 'lucas.dubois@maxit.dev', 'RM', 'Paris'),
('u1007', 'Rakesh Sharma', 'rakesh.sharma@maxit.dev', 'RM', 'San Francisco'),
('u1008', 'Elena Petrova', 'elena.petrova@maxit.dev', 'RM', 'Amsterdam');
