INSERT INTO user_info (first_name, last_name, email, password)
VALUES
('Frodo', 'Baggins', 'myburden@email.com', 'pbkdf2:sha256:260000$Cd165fpj3npLMdNW$0013a81442a9fd95785b0a55ae46a0c8acd6d6b56013669ea65745290e423615'),
('Samwise', 'Gamgee', 'gardener@email.com', 'pbkdf2:sha256:260000$5JpU4zj0T06QJIpB$23a14b87f02e2e354a1287f0c860340a5032915fe7002f7dd24041fd64ca3c95'),
('Gandalf', 'the White', 'mithrandir@email.com', 'pbkdf2:sha256:260000$adRxHi5Y7ynp66wW$8174ea9f16e7cb4c9a5a320c10b07ca6e67fe54f3d2b0e8c1451b47c26a27cd0')
('C', 'H', 'ch@em.co', 'pbkdf2:sha256:260000$8gl4nLAWfwR4M1HA$4ac39021f6243b81a60989d0ea9d6f51ea8dd3865aea6bebbae4ac4a98f50ec3');


INSERT INTO contacts (user_info_id, first_name, last_name, job_title, company, bio)
VALUES 
(1, 'Samwise', 'Gamgee', 'Gardener', 'The Fellowship', 'He is the main character, not me.'),
(1, 'Bilbo', 'Baggins', 'Celebrity', 'Thorin Oakenshield Inc.', 'He is writing a book. Don''t ask him about it though or he will talk your ear off about it.'),
(1, 'Tom', 'Bombadil', 'Possibly God', NULL, 'I am forgetting about him so I might not include him in my book.'),
(2, 'Frodo', 'Baggins', 'Ringbearer', 'The Fellowship', 'Kinda ambiguous to make easier to identify with him.'),
(2, 'Gollum', 'Smeogol', 'Stinker', 'Bad guys', 'There''s not left in him but lies and deceit.'),
(2, 'Faramir', 'Son of Denethor', 'Captain of the Rangers of Ithilien', 'Gondor', 'All I have to do is tell an epic speech and he will be good with us..'),
(3, 'Aragorn', 'Son of Arathorn', 'Ranger', 'Dunedain', 'This guy might be important.'),
(3, 'Legolas', 'Woodland Realm', 'Sniper', 'Elves', 'This guy is still mad that his girlfriend fell in love with a dwarf like 60 years ago. I mean get over it buddy.'),
(3, 'Gimli', 'Son of Gloin', 'Machine Gunner', 'Dwarves', 'Don''t even think about tossing this guy.');


INSERT INTO contacts_phone_numbers (contact_id, phone_number)
VALUES
(1, '1234567890'),
(2, '1111111111'),
(3, '0000000000'),
(4, '6548973210'),
(5, '4382090169'),
(5, '7798318284'),
(6, '0663161812'),
(7, '5816449688'),
(8, '0375090528'),
(9, '5243021176');


INSERT INTO contacts_emails (contact_id, email)
VALUES
(1, 'illcarryitforyou@email.com'),
(2, 'butterscrapedoverbred@email.com'),
(3, 'imightbeadeity@email.com'),
(4, 'myburdentobear@email.com'),
(5, 'myprecious@email.com'),
(5, 'itsmybirthday@email.com'),
(6, 'notboromir@email.com'),
(7, 'striderboi69@email.com'),
(8, 'mybow@email.com'),
(9, 'donttossmebro@email.com');


INSERT INTO contacts_social_medias (contact_id, social_media, social_media_address)
VALUES
(1, 'Twitter', '@thegreatstories'),
(2, 'Insta', '@nopartybusiness'),
(5, 'tiktok', '@ontheprecious'),
(5, 'tiktok', '@ilikefishing'),
(7, 'Facebook', 'legolassy');


INSERT INTO contacts_addresses (contact_id, street_address_1, street_address_2, city, county, state, country, zip)
VALUES
(2, '123 Hole in the Ground', 'Under the Hill', 'Hobbiton', 'Westfarthing', 'The Shire', 'Middle Earth', '12345'),
(4, '501 Buckland Road', NULL, 'Matamata 3472', NULL, NULL, 'New Zealand', NULL);


INSERT INTO contacts_notes (contact_id, note)
VALUES
(1, 'Oh my Eru Iluvatar! I can''t seem to get rid of this guy!'),
(1, 'He''s being such a jerk to my new friend smeogol. Come on Sam wtf?'),
(1, 'Okay he was right about Gollum after all.'),
(1, 'He asked me to be a ringbearer at his wedding. Jerk move, Sam. Jerk move.'),
(2, 'Haven''t seen him for 17 years since Gandalf left. However, it doesn''t seem important enough to include in my book I''ll just make it seem like it was a few weeks or something.'),
(3, 'This dude is weird.'),
(4, 'He''s my BEEEEEESSSSSSSTTTTTT FRRIIIIIIEEEENNNNDDDDDDDD.....'),
(4, 'He didn''t want me to join him on his trip, so I threatened to drown myself so he was forced to take me along. My therapist said things like that are unhealthy and lead toward horrible codependent relationships, but I dont care.'),
(4, 'I asked him to be the ringbearer for my wedding... lolz'),
(5, 'Legit heard him saying his plan to murder us out loud. Frodo didn''t believe me. I guess I''ll keep Gollum around for a while longer and not throw him off a cliff.'),
(5, 'Threw a giant boulder at this dudes head and he is still moving!'),
(6, 'This guys not cool'),
(6, 'I just gave a speech. I tried to talk loud enough so Faramir could hear it.'),
(6, 'Okay this guy is cool now.'),
(7, 'For realz I''ve told him to get a haircut so many times.'),
(7, 'This guy is gonna be a good king...... Actually wait, I never asked him about his tax policy...... whoops, I probably should have vetted him better.'),
(8, 'Just found Justin Bieber out in the woods and asked him to join this Council of Elrond thing going on.'),
(8, 'Okay its not actually Justin Bieber.. Its Legolas. Disappointing.'),
(8, 'So Gimli is a little racist against Elves....... I mean its a whole other species so I assume its cool.');


INSERT INTO meetings (contact_id, user_info_id, meeting_title, meeting_method, meeting_place, meeting_datetime)
VALUES
(2, 1, 'Birthday Bash', 'Party', 'That huge field down the street.', '3001-09-22 00:00:00'),
(7, 3, 'Meet Aragorn and the Hobbits', 'In Person', 'Prancing Pony, Bree', '3018-09-29 20:00:00'),
(7, 3, 'Meet Aragorn and the Hobbits', 'In Person', 'Prancing Pony, Bree', '3018-09-29 20:00:00'),
(NULL, 2, 'Take the Ring to Mount Doom Alone', 'In Person', 'Mordor', '3019-03-13 23:00:00');

INSERT INTO meetings_notes (meeting_id, note)
VALUES
(1, 'No visitors, well-wishers, or distant relations!'),
(2, 'Oh crap, I''m stuck at Orthanc..... not sure I can make it. Better send Aragorn a text..... Oh wait Saruman stole my phone.. that jerk.'),
(3, 'Look at me. I am the ringbearer now.');