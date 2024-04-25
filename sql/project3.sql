CREATE TABLE event (
    event_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    planner INT,
    FOREIGN KEY (planner) REFERENCES people(people_id),
    name VARCHAR(50),
    invitation VARCHAR(100),
    rental_items VARCHAR(50),
    venue VARCHAR(50),
    start_time TIME,
    image_path VARCHAR(100),
    maximum_attendees INT,
    note VARCHAR(255),
    end_time TIME,
    event_date DATE,
    host INT,
    FOREIGN KEY (host) REFERENCES people(people_id)
);


INSERT INTO event (planner, name, invitation, rental_items, venue, start_time, image_path, maximum_attendees, note, end_time, event_date, host) 
VALUES 
    (1, 'Equinox Gala', 'Join the Gala', 'Stall', 'Moose Lodge Hall', '23:00', 'images/birthday-party.png', 12, 'N/A', '02:00', '2003-12-25', 1),
    (2, 'Pat''s Graduation Party', 'GRADUATION!', 'Lights', 'Fountain Square Mall Ballroom', '21:00', 'images/dinner-party.png', 12, 'N/A', '02:00', '2024-11-24', 2),
    (3, 'Benny Got a Job', 'FIRST JOB!', 'bounce house', 'Bryan Park Pool', '22:00', 'images/graduation-event.png', 15, 'N/A', '05:00', '2023-10-20', 3),
    (4, 'Granny''s 100th Birthday', 'BIG 100!', 'Camera', 'IMU', '17:00', 'images/outdoor-party.png', 30, 'N/A', '20:30', '2030-09-10', 4),
    (5, 'Celebrate the Veterans', 'HELP US HONOR THE PEOPLE WHO SERVE US', 'PA SYSTEM', 'John Deer park', '18:00', 'images/sports-event.png', 35, 'N/A', '22:00', '2030-09-11', 5),
    (6, 'Ron''s Christmas Party', 'COME OVER AND HAVE FUN', 'DISCO', 'Ron''s house', '20:00', 'images/music-concert.png', 10, 'N/A', '00:00', '2030-09-12', 6);


CREATE TABLE ATTENDING (
    event_id INT NOT NULL,
    attendee_id INT NOT NULL,
    FOREIGN KEY(event_id) REFERENCES event(event_id),
    FOREIGN KEY(attendee_id) REFERENCES people(people_id)
);
CREATE TABLE people (
    people_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    address VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(50),
    date_of_birth DATE
);
ALTER TABLE people
ADD COLUMN role VARCHAR(50);



INSERT INTO people (Name, address, phone, email, date_of_birth, role) VALUES 
    ('Harry', '420 South Jordan street', '(607) 562-1374', 'slidup@uuluu.net', '1991-08-05', 'Staffer'),
    ('John', '430 South Eaglosn street', '(745) 841-2337', 'claudot@hobbyfreedom.com', '1996-05-27', 'Customer'),
    ('Henry', 'East Hunter ROAD', '(884) 218-5754', 'chuusits@hishamm12.shop', '1993-10-17', 'Customer'),
    ('Arjun', 'Meyer Road', '(353) 645-6765', 'guru4@bukutututul.xyz', '1991-05-26', 'Customer'),
    ('Son', 'East Coast Road', '(952) 908-4580', 'grishutovsvos@bigzobs.com', '1995-08-29', 'Staffer'),
    ('Steve', 'John Road', '(932) 995-8563', 'gmunky@visblackbox.com', '2001-01-14', 'Staffer');



CREATE TABLE venue (
venue_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Name VARCHAR(50),
address VARCHAR(100),
phone VARCHAR(15),
Fee INT,
attendees INT
);

INSERT INTO venue (Name, address, phone, Fee, attendees) VALUES 
    ('Moose Lodge Hall', '403 South Jordan street', '(209) 899-3006', 500, 100),
    ('Fountain Square Mall Ballroom', '430 South Eaglosn street', '(269) 450-5320', 350, 30),
    ('Bryan Park Pool', 'East Hunter ROAD', '(871) 285-9108', 200, 20),
    ('IMU', 'Meyer Road', '(458) 997-6976', 100, 20),
    ('John Deer park', 'East Coast Road', '(844) 889-6249', 90, 100),
    ('Ron''s house', 'John Road', '(501) 627-8222', 10, 30);


INSERT INTO ATTENDING (event_id, attendee_id) VALUES
    (1,2),
    (2,3),
    (4,5),
    (4,4),
    (5,2),
    (5,4);