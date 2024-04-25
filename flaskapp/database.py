from pymysql import connect
from pymysql.cursors import DictCursor

from flaskapp.config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE

# Make sure you have data in your tables. You should have used auto increment for
# primary keys, so all primary keys should start with 1


def get_connection():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DATABASE,
        cursorclass=DictCursor,
    )

def get_events():
    """Returns a list of dictionaries representing all of the event data"""
    sql = "SELECT * FROM event"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    return result
    
    
    

def get_event(event_id):
    """Takes an event_id, returns a single dictionary containing the data for the event with that id"""
    sql = "SELECT * FROM event WHERE event_id = %s"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id))
            result = cursor.fetchone() 
    return result
    
def add_event(name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, note, image_path):
    """Takes as input all of the data for an event. Inserts a new event into the event table"""
    sql = "INSERT INTO event (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, note, image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    connect = get_connection()
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, note, image_path))
            connect.commit()

  

def update_event(event_id, name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,note,image_path):
    """Takes a event_id and data for a event. Updates the event table with new data for the event with event_id as it's primary key"""
    sql =  "UPDATE event SET name = %s, event_date= %s, start_time = %s, end_time = %s, venue = %s, invitation = %s, maximum_attendees = %s, planner = %s, host = %s, rental_items = %s, note = %s, image_path = %s   WHERE event_id = %s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,note,image_path, event_id))
            connect.commit() 

def get_people():
    """Returns a list of dictionaries representing all of the person data"""
    sql = "SELECT * FROM people"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall() 
    return result

def add_person(name,address,email,date_of_birth,phone,role):
    """Takes as input all of the data for a person and adds a new person to the person table"""
    sql = "INSERT INTO people (name,address,email,date_of_birth,phone,role) VALUES (%s, %s, %s, %s, %s, %s);"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (name,address,email,date_of_birth,phone,role))
            connect.commit()

def delete_person(people_id):
    """Takes a person_id and deletes the person with that person_id from the person table"""
    sql = "DELETE FROM people WHERE people_id=%s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (people_id))
            connect.commit()

def get_attendees(event_id):
    """Returns a list of dictionaries representing all of the data for people attending a particular event"""
    sql = "SELECT * FROM people as p JOIN ATTENDING as a ON a.attendee_id = p.people_id JOIN event as e ON e.event_id = a.event_id WHERE a.event_id = %s"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id))
            result = cursor.fetchall() 
    return result

def add_attendee_event(event_id, attendee_id):
    """Takes as input a event_id and a attendee_id and inserts the appropriate data into the database that indicates the attendee with attendee_id as a primary key is attending the event with the event_id as a primary key"""
    sql = "INSERT INTO ATTENDING (event_id, attendee_id) VALUES (%s, %s);"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id, attendee_id))
            connect.commit()

def remove_attendee_event(event_id, attendee_id):
    """Takes as input a event_id and a attendee_id and deletes the data in the database that indicates that the attendee with attendee_id as a primary key
    is attending the event with event_id as a primary key."""
    sql = "DELETE FROM ATTENDING WHERE event_id=%s AND attendee_id=%s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id,attendee_id))
            connect.commit()
def get_host(event_id):
    """Takes an event_id and returns a dictionary of the data for the host of the event with
    event_id as its primary key"""
    sql = "SELECT * FROM people WHERE people_id = (SELECT host FROM event AS e WHERE e.event_id=%s);"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id))
            result = cursor.fetchone()
    return result


def set_host(person_id, event_id):
    """Sets the person with primary key person_id as the host of the event with event_id as its primary key"""
    sql = "UPDATE event SET host=%s WHERE event_id=%s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (person_id, event_id))
            connect.commit()

def get_planner(event_id):
    """Takes a event_id and returns a dictionary of the data for the planner of the event with
    event_id as its primary key"""
    sql = "SELECT * FROM people WHERE people_id = (SELECT planner FROM event AS e WHERE event_id=%s);"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id))
            result = cursor.fetchone()
    return result

def set_planner(person_id, event_id):
    """Sets the person with primary key person_id as the planner of the event with event_id as its primary key"""
    sql = "UPDATE event SET planner=%s WHERE event_id=%s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (person_id, event_id))
            connect.commit()


def get_venues():
    """Returns a list of dictionaries representing all of the venues data"""
    sql = "SELECT * FROM venue"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall() 
    return result

def add_venue(name,address,phone,fee,attendees):
    """Takes as input all of the data for a venue. Inserts a new venue into the event table"""
    sql = "INSERT INTO venue (name,address,phone,fee,attendees) VALUES (%s, %s, %s, %s, %s);"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (name,address,phone,fee,attendees))
            connect.commit()

def get_venue_name(event_id):
    """Returns venue using event_id"""
    sql = "SELECT venue.name  FROM event JOIN venue ON event.venue = venue.name WHERE event.event_id = %s;"
    connect = get_connection() 
    with connect:
        with connect.cursor() as cursor:
            cursor.execute(sql, (event_id))
            result = cursor.fetchone()
    return result


if __name__ == "__main__":

    print(f"All events: {get_events()}")
    print(f"Event info for event_id 1: {get_event(1)}")
    print(f"All people: {get_people()}")
    print(f"All attendees attending the event with event_id 1: {get_attendees(1)}")
    print(add_event('LIAM"S Christmas Party', 'COME OVER AND HAVE FUN', 'DISCO', 'Ron''s house', '20:00', 'images/music-concert.png', 10, 'N/A', '00:00', '2030-09-12', 6))
    
