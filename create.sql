CREATE TABLE user_info (
	user_info_id SERIAL PRIMARY KEY NOT NULL,
	first_name varchar(25) NOT NULL,
	last_name varchar(25) NOT NULL,
	email varchar(99) NOT NULL UNIQUE,
	password varchar NOT NULL
);

CREATE TABLE contacts (
	contact_id serial PRIMARY KEY NOT NULL,
	user_info_id integer NOT NULL,
	first_name varchar(25),
	last_name varchar(25),
	job_title varchar(50),
	company varchar(50),
	bio varchar(2000),
	FOREIGN KEY(user_info_id) REFERENCES user_info(user_info_id)
	);

CREATE TABLE contacts_phone_numbers (
	contact_phone_number_id serial PRIMARY KEY NOT NULL,
	contact_id integer NOT NULL,
	phone_number varchar(10) NOT NULL,
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE contacts_emails (
	contact_email_id serial PRIMARY KEY NOT NULL,
	contact_id integer NOT NULL,
	email varchar(99) NOT NULL,
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE contacts_social_medias (
	contact_social_media_id serial PRIMARY KEY NOT NULL,
	contact_id integer NOT NULL,
	social_media varchar(50) NOT NULL,
	social_media_address varchar(200) NOT NULL,
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE contacts_addresses (
	contact_address_id serial PRIMARY KEY NOT NULL,
	contact_id integer NOT NULL,
	street_address_1 varchar(150),
	street_address_2 varchar(150),
	city varchar(50),
	county varchar(50),
	state varchar(50),
	country varchar(50),
	zip varchar(9),
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE contacts_notes (
	contact_note_id serial PRIMARY KEY NOT NULL,
	contact_id integer NOT NULL,
	note varchar(5000) NOT NULL,
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE meetings (
	meeting_id serial PRIMARY KEY NOT NULL,
	user_info_id integer NOT NULL,
	contact_id integer,
	meeting_title varchar(150),
	meeting_method varchar(50),
	meeting_place varchar(100),
	meeting_datetime timestamp,
	FOREIGN KEY(user_info_id) REFERENCES user_info(user_info_id),
	FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
	);

CREATE TABLE meetings_notes (
	meeting_note_id serial PRIMARY KEY NOT NULL,
	meeting_id integer NOT NULL,
	note varchar(5000) NOT NULL,
	FOREIGN KEY(meeting_id) REFERENCES meetings(meeting_id)
	);