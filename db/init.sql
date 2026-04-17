-- db/init.sql
-- Run this against your local MySQL server before starting the backend.

CREATE DATABASE IF NOT EXISTS hcp_crm;
USE hcp_crm;

CREATE TABLE IF NOT EXISTS hcps (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    specialty   VARCHAR(100),
    territory   VARCHAR(100),
    email       VARCHAR(255),
    phone       VARCHAR(50),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interactions (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    hcp_id                  INT,
    rep_id                  INT NOT NULL DEFAULT 1,
    interaction_type        ENUM('Meeting','Call','Email','Conference') DEFAULT 'Meeting',
    interaction_date        DATE NOT NULL,
    interaction_time        TIME,
    attendees               TEXT,
    topics_discussed        TEXT,
    materials_shared        TEXT,
    samples_distributed     TEXT,
    sentiment               ENUM('Positive','Neutral','Negative') DEFAULT 'Neutral',
    outcomes                TEXT,
    follow_up_actions       TEXT,
    ai_summary              TEXT,
    ai_suggested_followups  TEXT,
    raw_chat_input          TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (hcp_id) REFERENCES hcps(id) ON DELETE SET NULL
);

-- Seed some sample HCPs for testing
INSERT INTO hcps (name, specialty, territory, email, phone) VALUES
('Dr. Priya Sharma',    'Oncology',        'Mumbai North',   'p.sharma@hospital.com',  '+91-98765-43210'),
('Dr. Arjun Mehta',     'Cardiology',      'Delhi Central',  'a.mehta@clinic.in',      '+91-87654-32109'),
('Dr. Kavitha Rao',     'Neurology',       'Bangalore East', 'k.rao@neuro.org',        '+91-76543-21098'),
('Dr. Rahul Patel',     'Endocrinology',   'Ahmedabad',      'r.patel@diabetes.in',    '+91-65432-10987'),
('Dr. Sunita Verma',    'Pulmonology',     'Chennai South',  's.verma@lung.com',       '+91-54321-09876'),
('Dr. Vikram Nair',     'Hematology',      'Hyderabad',      'v.nair@blood.org',       '+91-43210-98765'),
('Dr. Ananya Das',      'Rheumatology',    'Kolkata',        'a.das@rheum.in',         '+91-32109-87654'),
('Dr. Suresh Kumar',    'Gastroenterology','Pune',           's.kumar@gastro.com',     '+91-21098-76543');
