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


def get_contact_by_id(contact_id):
    try:
        query = Contacts.query.filter(Contacts.contact_id == contact_id).one()
        return query
    except:
        return False

def get_meeting_by_id(meeting_id):
    try:
        query = Meetings.query.filter(Meetings.meeting_id == meeting_id).one()
        return query
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

    validation_1 = len(social["social"]) <= 50
    validation_1 = len(social["social_address"]) <= 200

    if validation_1 and validation_2:
        new_social = Contacts_social_medias(contact_id = contact_id, social_medial = social["social"], social_media_address = social["social_address"])
        try:
            db.session.add(new_social)
            db.session.commit()
            print(f"Social added || {new_social}")
            return True
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



def get_emails_for_contact(contact_id):
    query = Contacts_emails.query.filter(Contacts_emails.contact_id == contact_id)

    return query

def get_addresses_for_contact(contact_id):
    addresses = Contacts_addresses.query.filter(Contacts_addresses.contact_id == contact_id).all()
    if len(addresses) == 0:
        addresses = None
    return addresses

def get_socials_for_contact(contact_id):
    socials = Contacts_social_medias.query.filter(Contacts_social_medias.contact_id == contact_id).all()
    if len(socials) == 0:
        socials = None
    return socials
    

def get_emails_as_list(email_object):
    emails = []
    for email in email_object:
        emails.append(email.email)
    return emails


def get_phones_for_contact(contact_id):
    query = Contacts_phone_numbers.query.filter(Contacts_phone_numbers.contact_id == contact_id)

    return query

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

        # This code sends only the first email to display on the All Contacts page.
        emails = []
        email_object = get_emails_for_contact(contact_id)
        for email in email_object:
            if len(emails) < 1:
                emails.append(email.email)
                break
        
        if len(emails) > 0:
            contact_email = emails[0]
        else:
            contact_email = None
        
        # This code sends only the first phone number to display on the All Contacts page.
        phones = []
        phone_object = get_phones_for_contact(contact_id)
        for phone in phone_object:
            phones.append(phone.phone_number)
            break
        
        if len(phones) > 0:
            contact_phone = get_readable_phone_number(phones[0])
        else:
            contact_phone = None

        if contact.first_name:
            first_name = contact.first_name
        else:
            first_name = None
        if contact.last_name:
            last_name = contact.last_name
        else:
            last_name = None
        if contact.job_title:
            job_title = contact.job_title
        else:
            job_title = None
        if contact.company:
            company = contact.company
        else:
            company = None

        contact = {"contact_id": contact_id, "first_name": first_name, "last_name": last_name, "email": contact_email, "phone": contact_phone, "job_title": job_title, "company": company}

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

def get_all_notes_contact(contact_id):
    notes = Contacts_notes.query.filter(Contacts_notes.contact_id == contact_id).all()
    if len(notes) == 0:
        notes = None
    return notes
  



def delete_social(user_id, social_id):
    print(user_id, social_id)








# Runs the script in interactive mode
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to Easy CRM database.")