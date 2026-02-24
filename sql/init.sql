CREATE TABLE departments (
    department_id   SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    location        VARCHAR(100)
);

CREATE TABLE jobs (
    job_id          SERIAL PRIMARY KEY,
    title           VARCHAR(100) NOT NULL,
    min_salary      NUMERIC(10,2),
    max_salary      NUMERIC(10,2)
);

CREATE TABLE employees (
    employee_id     SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    phone           VARCHAR(20)
);

CREATE TABLE job_history (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT NOT NULL REFERENCES employees(employee_id),
    job_id              INT NOT NULL REFERENCES jobs(job_id),
    department_id       INT NOT NULL REFERENCES departments(department_id),
    manager_id          INT REFERENCES employees(employee_id),
    hire_date           DATE NOT NULL,
    termination_date    DATE,
    salary              NUMERIC(10,2),
    reason              VARCHAR(100)
);

-- -------------------------------------------------------
-- Seed data
-- -------------------------------------------------------

INSERT INTO departments (name, location) VALUES
    ('Engineering',        'New York'),
    ('Product',            'San Francisco'),
    ('Human Resources',    'Chicago'),
    ('Finance',            'New York'),
    ('Marketing',          'Los Angeles'),
    ('Sales',              'Austin');

INSERT INTO jobs (title, min_salary, max_salary) VALUES
    ('Software Engineer I',       60000,  90000),
    ('Software Engineer II',      90000, 130000),
    ('Senior Software Engineer', 130000, 175000),
    ('Engineering Manager',      150000, 210000),
    ('Product Manager',          110000, 160000),
    ('HR Specialist',             55000,  80000),
    ('HR Manager',                80000, 120000),
    ('Financial Analyst',         70000, 105000),
    ('CFO',                      200000, 300000),
    ('Marketing Specialist',      55000,  85000),
    ('Sales Representative',      50000,  80000),
    ('Sales Manager',             90000, 140000);

INSERT INTO employees (first_name, last_name, email, phone) VALUES
    ('Diana',   'Flores',   'diana.flores@company.com',   '212-555-0101'),  -- 1
    ('Marcus',  'Webb',     'marcus.webb@company.com',    '415-555-0102'),  -- 2
    ('Sandra',  'Kim',      'sandra.kim@company.com',     '312-555-0103'),  -- 3
    ('Robert',  'Okafor',   'robert.okafor@company.com',  '212-555-0104'),  -- 4
    ('Laura',   'Chen',     'laura.chen@company.com',     '323-555-0105'),  -- 5
    ('James',   'Patel',    'james.patel@company.com',    '512-555-0106'),  -- 6
    ('Alice',   'Nguyen',   'alice.nguyen@company.com',   '212-555-0201'),  -- 7
    ('Brian',   'Torres',   'brian.torres@company.com',   '212-555-0202'),  -- 8
    ('Chloe',   'Martin',   'chloe.martin@company.com',   '212-555-0203'),  -- 9
    ('David',   'Russo',    'david.russo@company.com',    '212-555-0204'),  -- 10
    ('Eva',     'Schmidt',  'eva.schmidt@company.com',    '415-555-0205'),  -- 11
    ('Frank',   'Osei',     'frank.osei@company.com',     '415-555-0206'),  -- 12
    ('Grace',   'Li',       'grace.li@company.com',       '312-555-0207'),  -- 13
    ('Henry',   'Diaz',     'henry.diaz@company.com',     '212-555-0208'),  -- 14
    ('Isla',    'Brown',    'isla.brown@company.com',     '323-555-0209'),  -- 15
    ('Jason',   'Park',     'jason.park@company.com',     '512-555-0210'),  -- 16
    ('Karen',   'Wilson',   'karen.wilson@company.com',   '512-555-0211'),  -- 17
    ('Leo',     'Adams',    'leo.adams@company.com',      '212-555-0212');  -- 18

-- Job history: hire_date = role start, termination_date = role end (NULL = current)
INSERT INTO job_history (employee_id, job_id, department_id, manager_id, hire_date, termination_date, salary, reason) VALUES
    -- Diana (1): SE II -> Engineering Manager
    (1,  2, 1, NULL, '2015-03-01', '2018-02-28', 120000, 'hired'),
    (1,  4, 1, NULL, '2018-03-01', NULL,         195000, 'promotion'),

    -- Marcus (2): Product Manager
    (2,  5, 2, NULL, '2016-07-15', NULL,         145000, 'hired'),

    -- Sandra (3): HR Manager
    (3,  7, 3, NULL, '2014-01-20', NULL,         110000, 'hired'),

    -- Robert (4): CFO
    (4,  9, 4, NULL, '2013-06-10', NULL,         260000, 'hired'),

    -- Laura (5): Marketing Specialist
    (5,  10, 5, NULL, '2017-09-05', NULL,         78000, 'hired'),

    -- James (6): Sales Manager
    (6,  12, 6, NULL, '2016-11-30', NULL,        125000, 'hired'),

    -- Alice (7): SE I -> SE II
    (7,  1, 1, 1, '2019-04-12', '2021-04-11',  78000, 'hired'),
    (7,  2, 1, 1, '2021-04-12', NULL,          115000, 'promotion'),

    -- Brian (8): SE I
    (8,  1, 1, 1, '2020-08-03', NULL,           78000, 'hired'),

    -- Chloe (9): SE I
    (9,  1, 1, 1, '2021-02-17', NULL,           72000, 'hired'),

    -- David (10): SE I -> SE II -> Senior SE
    (10, 1, 1, 1, '2018-11-25', '2020-06-30',  68000, 'hired'),
    (10, 2, 1, 1, '2020-07-01', '2022-07-31', 110000, 'promotion'),
    (10, 3, 1, 1, '2022-08-01', NULL,          158000, 'promotion'),

    -- Eva (11): Product Manager
    (11, 5, 2, 2, '2020-05-19', NULL,          118000, 'hired'),

    -- Frank (12): Product Manager
    (12, 5, 2, 2, '2022-01-10', NULL,          112000, 'hired'),

    -- Grace (13): HR Specialist
    (13, 6, 3, 3, '2019-07-22', NULL,           68000, 'hired'),

    -- Henry (14): Financial Analyst
    (14, 8, 4, 4, '2021-09-14', NULL,           92000, 'hired'),

    -- Isla (15): Marketing Specialist
    (15, 10, 5, 5, '2020-03-30', NULL,          62000, 'hired'),

    -- Jason (16): Marketing Specialist -> Sales Rep (transfer)
    (16, 10, 5, 5, '2018-06-01', '2020-12-31', 58000, 'hired'),
    (16, 11, 6, 6, '2021-01-01', NULL,          65000, 'transfer'),

    -- Karen (17): Sales Rep
    (17, 11, 6, 6, '2019-10-07', NULL,          68000, 'hired'),

    -- Leo (18): SE I
    (18, 1, 1, 1, '2023-03-15', NULL,           70000, 'hired');
