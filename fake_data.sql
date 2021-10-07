INSERT INTO user_info (first_name, last_name, email, password)
VALUES
('Frodo', 'Baggins', 'myburden@email.com', 'icantdothissam'),
('Samwise', 'Gamgee', 'gardener@email.com', 'illcarryitforyou'),
('Gandalf', 'the White', 'mithrandir@email.com', 'flyyoufools');


INSERT INTO contacts (user_info_id, first_name, last_name, job_title, company, bio)
VALUES 
(2, 'Frodo', 'Baggins', 'Ringbearer', 'The Fellowship', 'Kinda ambiguous to make easier to identify with him.');