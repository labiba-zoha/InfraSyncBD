-- InfraSync BD Selenium test accounts
-- Run this only if preflight.py says one or more seeded logins are missing/wrong.
USE infrasync_bd;

-- Roles must already exist from schema/seeds.
INSERT INTO users (role_id, full_name, email, phone, password_hash, account_status)
VALUES
((SELECT role_id FROM roles WHERE role_name='super_admin'), 'System Administrator', 'admin@infrasync.gov.bd', '01799999999', 'admin123', 'active'),
((SELECT role_id FROM roles WHERE role_name='department_officer'), 'Eng. Salman', 'salman@rhd.gov.bd', '01733333331', 'admin123', 'active'),
((SELECT role_id FROM roles WHERE role_name='contractor'), 'Tariq Construction', 'tariq@builder.com', '01722222221', 'admin123', 'active'),
((SELECT role_id FROM roles WHERE role_name='citizen'), 'Rahim Uddin', 'rahim@citizen.com', '01711111111', 'admin123', 'active')
ON DUPLICATE KEY UPDATE
  role_id = VALUES(role_id),
  password_hash = VALUES(password_hash),
  account_status = 'active';
