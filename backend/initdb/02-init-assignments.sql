-- Create assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    rm_user_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    company_ticker TEXT,
    FOREIGN KEY (rm_user_id) REFERENCES users(user_id)
);

-- Insert RM company assignments
INSERT INTO assignments (rm_user_id, company_name, company_ticker) VALUES
('u1001', 'Broadcom', 'AVGO'),
('u1001', 'AMD', 'AMD'),
('u1002', 'Micron', 'MU'),
('u1002', 'Nvidia', 'NVDA'),
('u1002', 'Intel', 'INTC'),
('u1003', 'Bharti Airtel', 'BHARTIARTL.NS'),
('u1003', 'Reliance Jio', 'RELIANCE.NS'),
('u1004', 'Verizon', 'VZ'),
('u1004', 'AT&T', 'T'),
('u1004', 'Vodafone Group', 'VOD'),
('u1005', 'Maersk', 'MAERSK-B.CO'),
('u1005', 'Hapag-Lloyd', 'HLAG.DE'),
('u1006', 'NYK Line', '9101.T'),
('u1006', 'Mitsui OSK Lines', '9104.T'),
('u1006', 'ZIM Integrated', 'ZIM'),
('u1007', 'Delta Airlines', 'DAL'),
('u1007', 'United Airlines', 'UAL'),
('u1008', 'Lufthansa', 'LHA.DE'),
('u1008', 'Air France–KLM', 'AF.PA'),
('u1008', 'Emirates', NULL);
