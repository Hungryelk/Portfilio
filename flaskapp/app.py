# Copyright © 2023, Indiana University
# BSD 3-Clause License
from flask import Flask, render_template, request, redirect, url_for
from flaskapp import database
import html





app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#PEOPLE
#Calls the get_people function from the database and renders the template
@app.route('/')
@app.route('/people')
@app.route('/people/')
def people():
    people = database.get_people()
    return render_template("people.html", people = people)
    
#Adds people to the database using the add_person function
@app.route('/people/add', methods=["GET", "POST"])
def add_people():
    if request.method == "POST":
        #if an error occurs it will show a blank form
        error=check_people(request.form['Name'],request.form['address'],request.form['email'],request.form['date_of_birth'],request.form['phone'],request.form['role'])
        if error:
            return render_template('people_form.html')
        #If there are no errors it runs the add_person
        #the html.escape to imiting SQL Injection attacks
        database.add_person(request.form['Name'],html.escape(request.form['address']),html.escape(request.form['email']),html.escape(request.form['date_of_birth']),html.escape(request.form['phone']),html.escape(request.form['role']))
        return redirect(url_for('people'))
    else:
        return render_template("people_form.html")
#VENUE
@app.route('/venues/add', methods=["GET", "POST"])
def add_venue():
    # Grabs the information from the form and adds it the venue table in maria db
    if request.method == "POST":
            database.add_venue(request.form['Name'],request.form['address'],request.form['phone'],request.form['Fee'],request.form['attendees'])
            return redirect(url_for('venue'))
    else:
        return render_template("venue_form.html")
#takes the data from the database and displays it
@app.route("/venue/")
def venue():
    venue = database.get_venues()
    return render_template("venues.html", venue = venue)

# EVENTS

#adds a new event to the existing events database
@app.route('/events/add', methods=["GET", "POST"])
def add_events():
    List_venues = database.get_venues()
    list_people = database.get_people()
    list_events = database.get_events()
    if request.method == "POST":
        #error check calling the check event function which takes in the form to data and makes a list of errors in it
        error = check_event(request.form['Name'],request.form['date'],request.form['start_time'],request.form['end_time'],request.form['venue'],request.form['invitation'],request.form['max_attendes'],request.form['party_planner'],request.form['host'],request.form['rental_items'],request.form['notes'],request.form['image_path'])
        #if an error is found then the form resets and displays and empty version of it
        if error:
            return render_template('event_form.html', event = None, List_venues =  List_venues, list_events = list_events, list_people = list_people)
        #Adds the checked form data to the database
        database.add_event(request.form['Name'],html.escape(request.form['date']),html.escape(request.form['start_time']),html.escape(request.form['end_time']),request.form['venue'],html.escape(request.form['invitation']),html.escape(request.form['max_attendes']),html.escape(request.form['party_planner']),html.escape(request.form['host']),html.escape(request.form['rental_items']),html.escape(request.form['notes']),html.escape(request.form['image_path']))
        return redirect(url_for("events"))
    else:
        return render_template('event_form.html', event = None, List_venues = List_venues, list_events = list_events, list_people = list_people)
#takes events data from the database then displays
@app.route('/events')
def events():
    events = database.get_events()
    return render_template("events.html", events = events)
# if an events id is given then using the event id you display the event html page and the informtion linked to the event id
@app.route('/events/<events_id>')
def event(events_id=None):
    if events_id:
        event=database.get_event(events_id)
        host=database.get_host(events_id)
        planner = database.get_planner(events_id)
        venue = database.get_venue_name(events_id)
        attendees = database.get_attendees(events_id)
        list_people = database.get_people()
        return render_template("event.html", event = event, host = host, planner = planner, venue = venue, attendees = attendees, people = list_people) 


@app.route('/events/<event_id>/edit', methods=["GET", "POST"])
def events_edit(event_id=None):
    event = database.get_event(event_id)
    List_venues = database.get_venues()
    list_people = database.get_people()
    host=database.get_host(event_id)
    planner=database.get_planner(event_id)
    venue = database.get_venue_name(event_id)
    if request.method == "POST":
        #checks if the changes made to the exisitng edit are still in bounds of acceptable
        error = check_event(request.form['Name'],request.form['date'],request.form['start_time'],request.form['end_time'],request.form['venue'],request.form['invitation'],request.form['max_attendes'],request.form['party_planner'],request.form['host'],request.form['rental_items'],request.form['notes'],request.form['image_path'])
        if error:
            return render_template('event_form.html', event = event)
        #adds it back to the database
        database.update_event(event_id,request.form['Name'],html.escape(request.form['date']),html.escape(request.form['start_time']),html.escape(request.form['end_time']),request.form['venue'],html.escape(request.form['invitation']),html.escape(request.form['max_attendes']),html.escape(request.form['party_planner']),html.escape(request.form['host']),html.escape(request.form['rental_items']),html.escape(request.form['notes']),html.escape(request.form['image_path']))
        #returns back to the event page that you just edited
        if event_id:
            return redirect(url_for("event", events_id = event_id, event = event, host_val = host, planner = planner, venue = venue, List_venues = List_venues, list_people = list_people))
            # return render_template("event.html", event = event, host = host, planner = planner, venue = venue, List_venues = List_venues, list_people = list_people) 
    else:
        return render_template("event_form.html", events_id = event_id, event=event,  List_venues = List_venues, list_people = list_people, host_val = host, planner_val = planner )
#Takes from the form using the action and then adds it the databse and then spits out the updated attendee id
@app.route('/events/<event_id>/attendees/add', methods=["GET", "POST"])
def add_attendee(event_id=None):
    if request.method == "POST":
        attendee_id = request.form["Attendee_add"] 
        database.add_attendee_event(event_id, attendee_id)
        return redirect(url_for("event", events_id=event_id, attendee_id = attendee_id))
#DELTE ATTENDEE TAKES IN A PERSON_ID AND AN EVENT_ID and relays that into the remove attendee event
@app.route('/events/<event_id>/attendees/<person_id>/delete')
def delete_attendee(event_id=None,person_id=None):
    database.remove_attendee_event(event_id, person_id)
    return redirect(url_for("event", events_id=event_id, person_id = person_id))
   




#Takes input of the form data and check if it's valid by checking if it exists and if the len fits into the database lenghts
def check_people(name,address,email,date_of_birth,phone,role):
    errors = []
    if not name:
        errors.append("")
    elif len(name) >= 50:
        errors.append("")
    if not address:
        errors.append("")
    elif len(address) >= 100:
        errors.append("")
    if not email:
        errors.append("")
    elif len(email) >= 50:
        errors.append("")
    if not date_of_birth:
        errors.append("")
    if not phone:
        errors.append("")
    elif len(phone) >= 15:
        errors.append("")
    if not role:
        errors.append("")
    elif len(role) >= 50:
        errors.append("")
    if errors:
        return "\n".join(errors)
    else:
        return None



#Takes input of the form data and check if it's valid by checking if it exists and if the len fits into the database lenghts
def check_event(name, date, start_time, end_time, venue, invitation, max_attendees, party_planner, host, rental_items, notes, image_path):
    errors = []
    if not name:
        errors.append("")
    elif len(name) >= 50:
        errors.append("")
    if not date:
        errors.append("")
    if not start_time:
        errors.append("")
    if not end_time:
        errors.append("")
    if not venue:
        errors.append("")
    elif len(venue) >= 50:
        errors.append("")
    if not invitation:
        errors.append("")
    elif len(invitation) >= 100:
        errors.append("")
    if not max_attendees:
        errors.append("")
    if not party_planner:
        errors.append("")
    elif len(party_planner) >= 11:
        errors.append("")
    if not host:
        errors.append("")
    elif len(host) > 11:
        errors.append("")
    if not rental_items:
        errors.append("")
    if len(notes) > 500:
        errors.append("")
    if not image_path:
        errors.append("")
    if errors:
        return "\n".join(errors)
    else:
        return None





# OLD FUNCTIONS
#CREATES A LIST OF people FROM THE CSV
# def list_people():
#         people = pet=database.get_pet(int(pet_id))
    # with open('people.csv', encoding='UTF-8-sig') as csvfile:
    #     contents = csv.DictReader(csvfile)
    #     all_people = []
    #     for row in contents:
    #         all_people.append(row)
        # return all_people

#  all_events = events_list()
    # event = None
    # for i in all_events:
    #     if i['Name'] == event_id:
    #         event = i
    #         break
    #takes the updated infomration from the forms into a new dict
    # if request.method == "POST":
    #     edit_event = {}
    #     edit_event["Name"] = request.form['Name']
    #     edit_event["date"] = request.form['date']
    #     edit_event["Venue"] = request.form['venue']
    #     edit_event["start_time"] = request.form['start_time']
    #     edit_event["end_time"] = request.form['end_time']
    #     edit_event["invitation"] = request.form['invitation']
    #     edit_event["path"] = request.form['image_path']
    #     edit_event["attendees"] = request.form['max_attendes']
    #     edit_event["planner"] = request.form['party_planner']
    #     edit_event["rental_items"] = request.form['rental_items']
    #     edit_event["Notes"] = request.form['notes']
        # print(edit_event)
        # #enumerates over the infomation it find the exact index.
        # for j,i in enumerate(all_events):
        #     if event_id == i["Name"]:
        #         all_events[j] = edit_event
        # #adds the updated all_events to the csv
        # with open("events.csv", "w") as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=Keys)
        #     writer.writeheader()
        #     for row in all_events:
        #         writer.writerow(row)
#   # all_events = events_list()
    # for i in all_events:
    #     if i['Name'] == events_id:
    #         return render_template("event.html", event=i)
#Keys created for the use of file name in events
# Keys ={
#     "Name",
#     "date",
#     "Venue",
#     "start_time",
#     "end_time",
#     "invitation",
#     "path",
#     "attendees",
#     "planner",
#     "rental_items",
#     "Notes",
# }
#edits the events
# event_id=None 


# new_event.append(request.form['date'])
    #     new_event.append(request.form['venue'])
    #     new_event.append(request.form['start_time'])
    #     new_event.append(request.form['end_time'])
    #     new_event.append(request.form['invitation'])
    #     new_event.append(request.form['image_path'])
    #     new_event.append(request.form['max_attendes'])
    #     new_event.append(request.form['party_planner'])
    #     new_event.append(request.form['rental_items'])
    #     new_event.append(request.form['notes'])
    #     #creates a new line so it doesn't print at the bottom
    #     print(new_event)
    #     with open('events.csv', mode="a") as csv_file:
    #         writer_object = writer(csv_file)
    #         writer_object.writerow(new_event)
    #         return redirect(url_for('events'))

    # def venue_list():
#     with open('venues.csv', encoding='UTF-8-sig') as csvfile:
#         contents = csv.DictReader(csvfile)
#         all_venues = []
#         for row in contents:
#             all_venues.append(row)
#         return all_venues

# new_venue = []
        # new_venue.append(request.form['Name'])
        # new_venue.append(request.form['address'])
        # new_venue.append(request.form['phone'])
        # new_venue.append(request.form['Fee'])
        # new_venue.append(request.form['attendees'])
        # with open('venues.csv', mode="a", newline="") as csv_file:
        #     writer_object = writer(csv_file)
        #     writer_object.writerow(new_venue)

        # new_person = []
        # new_person.append(request.form['Name'])
        # new_person.append(request.form['address'])
        # new_person.append(request.form['phone'])
        # new_person.append(request.form['email'])
        # new_person.append(request.form['date_of_birth'])
        # with open('people.csv', mode="a",newline="") as csv_file:
        #     writer_object = writer(csv_file)
        #     writer_object.writerow(new_person)