'''INSERT INTO admission_type(admission_type)
VALUES ('Yearly'),
	   ('Semester'),
	   ('Course');

	   
INSERT INTO department (department_name)
VALUES ('FSc'),
       ('Medical Courses'),
       ('Short Courses');

INSERT INTO course (name, department_id)
VALUES ('DIT I Year', 3),
       ('MS Office', 3),
       ('Special Excel', 3),
	   ('Graphic Design', 3),
	   ('Video Editing', 3),
	   ('CCTV', 3),
       ('CCNA', 3),
       ('Web Development', 3),
	   
       ('Health', 2),
       ('Pathology', 2),
       ('Pharmacy', 2),
       ('Dental', 2),
       ('Anesthesia', 2),
       ('Surgical', 2),
       ('Radiology', 2),

       ('DIT II Year', 1),
       ('Pre Engineering', 1),
       ('Pre Medical', 1),
       ('Computer Science', 1);


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
	   ('Course');'''