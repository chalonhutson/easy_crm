from datetime import datetime

from model import connect_to_db, db, User_info, Contacts, Contacts_phone_numbers, Contacts_emails, Contacts_social_medias, Contacts_addresses, Contacts_notes, Meetings, Meetings_notes

from werkzeug.security import check_password_hash

# from flask_login import LoginManager, UserMixin



def get_user_by_id(user_id):
    try:
        query = User_info.query.filter(User_info.id == user_id).one()
        return query
    except:
        return False


def get_user_by_email(email):

    try:
        user = User_info.query.filter(User_info.email==email).one()
        return user
    except:
        return False


def attempt_login(email, password):
    
    user = get_user_by_email(email)

    if user:
        if check_password_hash(user.password, password):
            return user
        else:
            return False
    else:
        return False

def attempt_registration(first_name, last_name, email, password):
    new_user = User_info(first_name = first_name, last_name = last_name, email = email, password = password)
    db.session.add(new_user)
    db.session.commit()
    success = attempt_login(email, password)
    if success:
        print(f"New Registration || {new_user}")
        return success
    else:
        return False


def return_count_contacts(user_id):
    count = Contacts.query.filter(Contacts.user_info_id == user_id).count()
    return count

def return_count_meetings(user_id):
    count = Meetings.query.filter(Meetings.user_info_id == user_id).count()
    return count




def get_meeting_by_id(meeting_id):
    try:
        meeting = Meetings.query.get(meeting_id)
        return meeting
    except:
        return False


def add_contact(user_id, fname, lname, title, company, bio):

    if len(fname) < 25 and len(lname) < 25 and len(title) < 50 and len(company) < 50 and len(bio) < 2000:
        new_contact = Contacts(user_info_id = user_id, first_name = fname, last_name = lname, job_title = title, company = company, bio = bio)
        db.session.add(new_contact)
        db.session.commit()
        print(f"Contact added || {new_contact}")
        return True
    else:
        return False


def add_meeting(user_id, form):
    
    user_id = user_id
    if form["contact"] == "None" or None:
        contact_id = None
    else:
        contact_id = form["contact"]
    if form["title"]:
        title = form["title"]
    else:
        title = None
    if form["method"]:
        method = form["method"]
    else:
        method = None
    if form["place"]:
        place = form["place"]
    else:
        place = None
    if form["datetime"]:
        datetime = form["datetime"]
    else:
        datetime = None
    meeting = Meetings(user_info_id = user_id, contact_id = contact_id, meeting_title = title, meeting_method = method, meeting_place = place, meeting_datetime = datetime)

    try:
        print(f"Meeting added || {meeting}")
        db.session.add(meeting)
        db.session.commit()
        return meeting
    except:
        return False


def add_email(user_id, contact_id, email):

    #Checks if the user who owns the contact for whom we are trying to add the email, is the actual contact owner. If they aren't a match, the function returns true, and avoids commiting a new email to the database.
    get_contact = Contacts.query.filter(Contacts.contact_id == contact_id).one()
    is_correct_user = get_contact.user_info_id == user_id
    if is_correct_user == False:
        return False

    if len(email) < 99 and type(email) is str:
        new_email = Contacts_emails(contact_id = contact_id, email = email)
        db.session.add(new_email)
        db.session.commit()
        print(f"Email added || {new_email}")
        return True
    else:
        return False


def add_phone(user_id, contact_id, phone):

    #Same as add_email function. Checks to ensure the user has the rights to add to this contact.
    get_contact = Contacts.query.filter(Contacts.contact_id == contact_id).one()
    is_correct_user = get_contact.user_info_id == user_id
    if is_correct_user == False:
        return False

    if len(phone) == 10 and type(phone) is str:
        new_phone = Contacts_phone_numbers(contact_id = contact_id, phone_number = phone)
        db.session.add(new_phone)
        db.session.commit()
        print(f"Phone added || {new_phone}")
        return True
    else:
        return False


def add_address(user_id, contact_id, address):
    get_contact = Contacts.query.filter(Contacts.contact_id == contact_id).one()
    is_correct_user = get_contact.user_info_id == user_id
    if is_correct_user == False:
        return False
    print(address)

    validation_1 = len(address["address_1"]) <= 150
    validation_2 = len(address["city"]) <= 50
    validation_3 = len(address["county"]) <= 50
    validation_4 = len(address["state"]) <= 50
    validation_5 = len(address["country"]) <= 50
    validation_6 = len(address["zip"]) <= 9

    if validation_1 and validation_2 and  validation_3 and validation_4 and validation_5 and validation_6:
        new_address = Contacts_addresses(contact_id = contact_id, street_address_1 = address["address_1"], street_address_2 = address["address_2"], city = address["city"], county = address["county"], state = address["state"], country = address["country"], zip = address["zip"])
        try:
            db.session.add(new_address)
            db.session.commit()
            print(f"Address added || {new_address}")
            return True
        except:
            return False
    else:
        return False


def add_social(user_id, contact_id, social):
    get_contact = Contacts.query.filter(Contacts.contact_id == contact_id).one()
    is_correct_user = get_contact.user_info_id == user_id
    if is_correct_user == False:
        return False
    validation_1 = len(social["social_media"]) <= 50
    validation_2 = len(social["social_media_address"]) <= 200

    if validation_1 and validation_2:
        new_social = Contacts_social_medias(contact_id = contact_id, social_media = social["social_media"], social_media_address = social["social_media_address"])
        try:
            db.session.add(new_social)
            db.session.commit()
            print(f"Social added || {new_social}")
            return True
        except:
            return False
    else:
        return False

def add_note_meeting(user_id, meeting_id, note):
    try:
        meeting = Meetings.query.get(meeting_id)
    except:
        return False
    if meeting.user_info_id != user_id:
        return False
    print(note["note"])
    if len(note["note"]) <= 5000:
        new_note = Meetings_notes(meeting_id = meeting_id, note = note["note"])
        try:
            db.session.add(new_note)
            db.session.commit()
            print(f"Meeting note added || {new_note}")
            return new_note
        except:
            return False
    else:
        return False



def add_note_contact(user_id, contact_id, note):
    try:
        contact = Contacts.query.get(contact_id)
    except:
        return False
    if contact.user_info_id != user_id:
        return False
    print(note["note"])
    if len(note["note"]) <= 5000:
        new_note = Contacts_notes(contact_id = contact_id, note = note["note"])
        try:
            db.session.add(new_note)
            db.session.commit()
            print(f"Contact note added || {new_note}")
            return new_note
        except:
            return False
    else:
        return False






def find_contact_by_fname(user_id, name):
    name = name.lower()
    q = Contacts.query.filter(func.lower(Contacts.first_name) == name)
    qcount = q.count()

    if qcount == 0:
        return "No results."
    if qcount == 1:
        qresult = q.first()
        full_name = f"{qr.first_name} {qr.last_name}"
        return full_name
    if qcount > 1:
        qresult = q.all()
        return qresult


######## Begin Get Contact Info ############
######## Begin Get Contact Info ############
######## Begin Get Contact Info ############

def get_contact_by_id(contact_id):
    try:
        contact = Contacts.query.filter(Contacts.contact_id == contact_id).one()
        return contact
    except:
        return None

def get_name_for_contact(contact_id):
    contact = Contacts.query.get(contact_id)
    if not contact.first_name and not contact.last_name:
        return None
    return f"{contact.first_name} {contact.last_name}"

def get_phones_for_contact(contact_id):
    phones = Contacts_phone_numbers.query.filter(Contacts_phone_numbers.contact_id == contact_id).all()
    if len(phones) == 0:
        return None
    return phones

def get_first_phone_contact(contact_id):
    phone= Contacts_phone_numbers.query.filter(Contacts_phone_numbers.contact_id == contact_id).first()
    if not phone:
        return None
    return phone

def get_emails_for_contact(contact_id):
    emails = Contacts_emails.query.filter(Contacts_emails.contact_id == contact_id).all()
    if len(emails) == 0:
        return None
    return emails

def get_first_email_contact(contact_id):
    email = Contacts_emails.query.filter(Contacts_emails.contact_id == contact_id).first()
    if not email:
        return None
    return email

def get_addresses_for_contact(contact_id):
    addresses = Contacts_addresses.query.filter(Contacts_addresses.contact_id == contact_id).all()
    if len(addresses) == 0:
        return None
    return addresses

def get_socials_for_contact(contact_id):
    socials = Contacts_social_medias.query.filter(Contacts_social_medias.contact_id == contact_id).all()
    if len(socials) == 0:
        return None
    return socials

def get_all_notes_contact(contact_id):
    notes = Contacts_notes.query.filter(Contacts_notes.contact_id == contact_id).all()
    if len(notes) == 0:
        return None
    return notes

def get_all_for_contact(contact_id):
    contact = get_contact_by_id(contact_id)
    phones = get_phones_for_contact(contact_id)
    emails = get_emails_for_contact(contact_id)
    addresses = get_addresses_for_contact(contact_id)
    socials = get_socials_for_contact(contact_id)
    notes = get_all_notes_contact(contact_id)
    return contact, phones, emails, addresses, socials, notes

######## End Get Contact Info ############
######## End Get Contact Info ############
######## End Get Contact Info ############



def get_emails_as_list(email_object):
    emails = []
    for email in email_object:
        emails.append(email.email)
    return emails



def get_readable_phone_number(phone):
    new_phone = f"({phone[0:3]}) {phone[3:6]}-{phone[6:]}"
    return new_phone

def get_readable_date_time(datetime):
    date = datetime.strftime("%B %d, %Y")
    time = datetime.strftime("%I:%M")
    return date, time

def get_phones_as_list(phone_object):
    phones = []
    for phone in phone_object:
        phones.append(get_readable_phone_number(phone.phone_number))
    return phones

def get_all_contacts_by_user(user_id, alphabetical):
    if alphabetical == True:
        contacts = Contacts.query.filter(Contacts.user_info_id == user_id).order_by(Contacts.first_name).all()
    else:
        contacts = Contacts.query.filter(Contacts.user_info_id == user_id).all()
    return contacts

def get_all_contacts_page(user_id, per_page, page_offset):
    page_offset = page_offset * per_page
    query = Contacts.query.filter(Contacts.user_info_id == user_id).limit(per_page).offset(page_offset)

    contacts = []

    for contact in query:
        contact_id = contact.contact_id
        name = get_name_for_contact(contact_id)
        phone = get_first_phone_contact(contact_id)
        email = get_first_email_contact(contact_id)
        job_title = contact.job_title
        company = contact.company
        contact = {"contact_id": contact_id, "name": name, "email": email, "phone": phone, "job_title": job_title, "company": company}

        contacts.append(contact)

    return contacts


def get_all_meetings_page(user_id, per_page, page_offset):
    page_offset = page_offset * per_page
    query = Meetings.query.filter(Meetings.user_info_id == user_id).limit(per_page).offset(page_offset)

    meetings = []

    for meeting in query:
        meeting_id = meeting.meeting_id
        if meeting.contact_id:
            meeting_contact = get_contact_by_id(meeting.contact_id)
        else:
            meeting_contact = None
        if meeting.meeting_title:
            meeting_title = meeting.meeting_title
        else:
            meeting_title = None
        if meeting.meeting_method:
            meeting_method = meeting.meeting_method
        else:
            meeting_method = None
        if meeting.meeting_place:
            meeting_place = meeting.meeting_place
        else:
            meeting_place = None
        if meeting.meeting_datetime:
            meeting_date, meeting_time = get_readable_date_time(meeting.meeting_datetime)
        else:
            meeting_date = None
            meeting_time = None

        meeting = {"meeting_id": meeting_id, "meeting_contact": meeting_contact, "meeting_title": meeting_title, "meeting_method": meeting_method, "meeting_place": meeting_place, "meeting_date": meeting_date, "meeting_time": meeting_time}

        meetings.append(meeting)

    return meetings




def get_all_notes_meeting(meeting_id):
    notes = Meetings_notes.query.filter(Meetings_notes.meeting_id == meeting_id).all()
    if len(notes) == 0:
        notes = None
    return notes


  
def get_contact_by_address(addresses_id):
    try:
        address = Contacts_addresses.query.get(addresses_id)
        contact_id = address.contact_id
        return contact_id
    except:
        return False

def get_contact_by_social(social_id):
    try:
        social = Contacts_social_medias.query.get(social_id)
        contact_id = social.contact_id
        return contact_id
    except:
        return False

def get_contact_by_phone(phone_id):
    try:
        phone = Contacts_phone_numbers.query.get(phone_id)
        contact_id = phone.contact_id
        return contact_id
    except:
        return False

def get_contact_by_email(email_id):
    try:
        email = Contacts_emails.query.get(email_id)
        contact_id = email.contact_id
        return contact_id
    except:
        return False

def get_note_meeting_by_id(note_id):
    note = Meetings_notes.query.get(note_id)
    return note

def get_note_contact_by_id(note_id):
    note = Contacts_notes.query.get(note_id)
    return note


def delete_address(user_id, address_id):
    address = Contacts_addresses.query.get(address_id)
    contact_owner = Contacts.query.get(address.contact_id)
    if user_id == contact_owner.user_info_id:
        try:
            db.session.delete(address)
            db.session.commit()
            return True
        except:
            return False
    else:
        return False

def delete_social(user_id, social_id):
    social = Contacts_social_medias.query.get(social_id)
    contact_owner = Contacts.query.get(social.contact_id)
    if user_id == contact_owner.user_info_id:
        try:
            db.session.delete(social)
            db.session.commit()
            return True
        except:
            return False
    else:
        return False
        
def delete_phone(user_id, phone_id):
    phone = Contacts_phone_numbers.query.get(phone_id)
    contact_owner = Contacts.query.get(phone.contact_id)
    if user_id == contact_owner.user_info_id:
        try:
            db.session.delete(phone)
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def delete_email(user_id, email_id):
    email = Contacts_emails.query.get(email_id)
    contact_owner = Contacts.query.get(email.contact_id)
    if user_id == contact_owner.user_info_id:
        try:
            db.session.delete(email)
            db.session.commit()
            return True
        except:
            return False
    else:
        return False

def delete_note_meeting(user_id, note_id):
    note = Meetings_notes.query.get(note_id)
    if not note:
        return False
    meeting = Meetings.query.get(note.meeting_id)
    if user_id == meeting.user_info_id:
        try:
            db.session.delete(note)
            db.session.commit()
            return True
        except:
            print("Couldn't delete meeting from database.")
            return False
    else:
        return False


def delete_note_contact(user_id, note_id):
    note = Contacts_notes.query.get(note_id)
    if not note:
        return False
    contact = Contacts.query.get(note.contact_id)
    if user_id == contact.user_info_id:
        try:
            db.session.delete(note)
            db.session.commit()
            return True
        except:
            print("Couldn't delete contact from database.")
            return False
    else:
        return False







# Runs the script in interactive mode
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to Easy CRM database.")