from sqlalchemy import text 
from app.config.db_connect import engine



def table_entries():
	table_entries = text('''INSERT INTO admission_type(admission_type)
	VALUES ('Yearly'),
		('Semester'),
		('Course');

		
	INSERT INTO department (department_name)
	VALUES ('FSc Programms'),
		('Medical Courses'),
		('Short Courses');

	INSERT INTO course (name, department_id)
	VALUES
	('DIT I Year', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('MS Office', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('Special Excel', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('Graphic Design', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('Video Editing', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('CCTV', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('CCNA', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),
	('Web Development', (SELECT department_id FROM department WHERE department_name = 'Short Courses')),

	('Health', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Pathology', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Pharmacy', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Dental', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Anesthesia', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Surgical', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),
	('Radiology', (SELECT department_id FROM department WHERE department_name = 'Medical Courses')),

	('DIT II Year', (SELECT department_id FROM department WHERE department_name = 'FSc Programms')),
	('Pre Engineering', (SELECT department_id FROM department WHERE department_name = 'FSc Programms')),
	('Pre Medical', (SELECT department_id FROM department WHERE department_name = 'FSc Programms')),
	('Computer Science', (SELECT department_id FROM department WHERE department_name = 'FSc Programms'));


	INSERT INTO shift(shift_name)
	VALUES ('Morning'),
		('Evening'),
		('Both');


	INSERT INTO salary_type(salary_type_name)
	VALUES ('Salary'),
			('Bonous'),
			('Advance');


	INSERT INTO payment_type(payment_type_name)
	VALUES ('Fee'),
		('Addmission Fee'),	   	
		('Promotion Fee'),
		('Miscelenious Fee'),
		('Examination Fee'),
		('Registration Fee'),
		('Compart Fee'),
		('UFM Fee'),
		('Grace Fee'),
		('Hospital Fee'),
		('Sports Fee'),
		('DMC Fee'),
		('Diploma Fee'),
		('Certificate Fee');


	INSERT INTO salary_type (salary_type_name)
	VALUES ('Yearly'),
		('Semester'),
		('Course');
		

	INSERT INTO session (session_id, session) 
	VALUES (24, '2024'), (25, '2025'), 
		(26, '2026'), (27, '2027'), 
		(28, '2028'), (29, '2029'), 
		(30, '2030');


	INSERT INTO month (month)
	VALUES ('Jan'),
		('Feb'),
		('March'),
		('April'),
		('May'),
		('Jun'),	   
		('July'),		   
		('Aug'),
		('Sept'),
		('Oct'),
		('Nov'),
		('Dec');
		


	INSERT INTO day (day)
	VALUES ('1'), ('2'), ('3'),
		('4'), ('5'), ('6'),	   
		('7'), ('8'), ('9'),
		('10'), ('11'), ('12'),
		('13'), ('14'), ('15'),
		('16'), ('17'), ('18'),
		('19'), ('20'), ('21'),
		('22'), ('23'), ('24'),
		('15'), ('26'), ('27'),
		('28'), ('29'), ('30'), ('31');
		''')




	with engine.connect() as conn:
		conn.execute(table_entries)
		conn.commit()


# INSERT INTO course (name, department_id)
# VALUES ('DIT I Year', 3),
# 	('MS Office', 3),
# 	('Special Excel', 3),
# 	('Graphic Design', 3),
# 	('Video Editing', 3),
# 	('CCTV', 3),
# 	('CCNA', 3),
# 	('Web Development', 3),
	
# 	('Health', 2),
# 	('Pathology', 2),
# 	('Pharmacy', 2),
# 	('Dental', 2),
# 	('Anesthesia', 2),
# 	('Surgical', 2),
# 	('Radiology', 2),

# 	('DIT II Year', 1),
# 	('Pre Engineering', 1),
# 	('Pre Medical', 1),
# 	('Computer Science', 1);
