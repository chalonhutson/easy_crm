from model import connect_to_db, User_info, Contacts, Contacts_phone_numbers, Contacts_emails, Contacts_social_medias, Contacts_addresses, Contacts_notes, Meetings, Meetings_notes


def add_contact(user_id, fname, lname, title, company, bio):
    new_c = Contacts(first_name = fname, last_name = lname, job_title = title, company = company, bio = bio)
    db.session.add(new_c)
    db.session.commit()


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


def get_phones_for_contact(contact_id):
    query = Contacts_phone_numbers.query.filter(Contacts_phone_numbers.contact_id == contact_id)

    return query


def get_all_contacts_page(user_id, per_page, page_offset):
    page_offset = page_offset * per_page
    query = Contacts.query.filter(Contacts.user_info_id == user_id).limit(per_page).offset(page_offset)

    contacts = []

    for contact in query:
        contact_id = contact.contact_id
        emails = []
        email_object = get_emails_for_contact(contact_id)
        for email in email_object:
            if len(emails) < 1:
                emails.append(email.email)
        
        if len(emails) > 0:
            cemail = emails[0]
        else:
            cemail = None
        
        phones = []
        phone_object = get_phones_for_contact(contact_id)
        for phone in phone_object:
            # if len(phones) < 1:
            phones.append(phone.phone_number)
            break
        
        if len(phones) > 0:
            cphone = phones[0]
        else:
            cphone = None

        fname = contact.first_name
        lname = contact.last_name

        contact = {"first_name": fname, "last_name": lname, "email": cemail, "phone": cphone}

        contacts.append(contact)

    return contacts


# Runs the script in interactive mode
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to Easy CRM database.")

    # if query.count() >= per_page:
    #     for i in query:
    #         print(i.first_name)
    # elif query.count() > 0:
    #     for i in query:
    #         print(i.first_name)
    #         print("End of contacts.")
    # else:
    #     print("No more contacts.")