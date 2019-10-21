from dicttoxml import dicttoxml
from database_creation import Message, db


def filter_messages(filter_parameters: dict):
    filtered_messages = db.session.query(Message)
    json_size = 0

    if 'title' in filter_parameters['filter']:
        json_size += 1
        filtered_messages = filtered_messages.filter(Message.title == filter_parameters['filter']['title'])
    if 'date' in filter_parameters['filter']:
        json_size += 1
        filtered_messages = filtered_messages.filter(Message.date == convert_date(filter_parameters['filter']['date']))
    if 'from' in filter_parameters['filter']:
        json_size += 1
        filtered_messages = filtered_messages.filter(Message.sender == filter_parameters['filter']['from'])
    if 'to' in filter_parameters['filter']:
        json_size += 1
        filtered_messages = filtered_messages.filter(Message.recipient == filter_parameters['filter']['to'])

    if json_size == len(filter_parameters['filter']):
        return filtered_messages
    else:
        return None


def convert_to_xml(message_from_database: Message) -> bytes:
    message_dict = {'Message': {}}
    message_dict['Message']['Header'] = {}
    message_dict['Message']['Header']['To'] = message_from_database.recipient
    message_dict['Message']['Header']['From'] = message_from_database.sender
    message_dict['Message']['Header']['Timestamp'] = message_from_database.date + "T" + message_from_database.time
    message_dict['Message']['Title'] = message_from_database.title
    message_dict['Message']['Body'] = message_from_database.message

    return dicttoxml(message_dict, root=False, attr_type=False)


def send_message_to_db(message_in_dict: dict):
    if 'Message' in message_in_dict and 'Header' in message_in_dict['Message'] \
            and 'To' in message_in_dict['Message']['Header'] and 'From' in message_in_dict['Message']['Header'] \
            and 'Timestamp' in message_in_dict['Message']['Header'] and 'Title' in message_in_dict['Message'] \
            and 'Body' in message_in_dict['Message']:
        try:
            current_id = db.session.query(Message)[-1].id + 1
        except:
            current_id = 1

        message_in_dict = Message(id=current_id, recipient=message_in_dict['Message']['Header']['To'],
                                  sender=message_in_dict['Message']['Header']['From'],
                                  date=message_in_dict['Message']['Header']['Timestamp'][:10],
                                  time=message_in_dict['Message']['Header']['Timestamp'][11:],
                                  title=message_in_dict['Message']['Title'],
                                  message=message_in_dict['Message']['Body'])
        db.session.add(message_in_dict)
        db.session.commit()

        return "Пустое сообщение"
    else:
        return None


def convert_date(date: str) -> str:
    if date[2] == '.' and date[5] == '.':
        date = date.split('.')
        date = list(reversed(date))
        date = '-'.join(date)
    else:
        date = "invalid date format"

    return date
