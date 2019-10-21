from flask import request
import xmltodict
from flask_classy import FlaskView, route
import os
import lxml.etree

from secondary import send_message_to_db, convert_to_xml, filter_messages
from database_creation import Message, db


class ApiView(FlaskView):
    @route('/findMessages', methods=["POST"])
    def find_messages(self):
        if db.session.query(Message).count() > 0:
            json_request = request.get_json()
            filtered_messages = filter_messages(json_request)

            if filtered_messages is not None:
                messages_in_xml = convert_to_xml(filtered_messages[0])
                convert_to_pretty_xml = str(messages_in_xml.decode('utf-8'))

                for filtered_message in filtered_messages[1:]:
                    messages_in_xml = convert_to_xml(filtered_message)
                    convert_to_pretty_xml += str(messages_in_xml.decode('utf-8'))

                convert_to_pretty_xml = lxml.etree.fromstring('<Messages>' + convert_to_pretty_xml + '</Messages>')

                return lxml.etree.tostring(convert_to_pretty_xml, pretty_print=True, encoding='UTF-8',
                                           method='xml', xml_declaration=True)
            else:
                return "Some of JSON keys are wrong"
        else:
            return "There are no messages in the database"

    @route('sendMessage', methods=['POST'])
    def send_message_from_file(self):
        try:
            message_in_dict = xmltodict.parse(request.data)
        except:
            return "file does not contain xml"

        if send_message_to_db(message_in_dict) is None:
            return "invalid XML format"
        else:
            return ""

    @route('sendMessage/<path:file_path>', methods=['GET'])
    def send_message(self, file_path):
        if not os.path.exists(file_path.replace('/', '\\')):
            return "File with that name does not exist!"

        message_from_file = open(file_path.replace('/', '\\'), encoding='utf-8')

        try:
            message_in_dict = xmltodict.parse(message_from_file.read())
        except:
            return "file does not contain xml"

        if send_message_to_db(message_in_dict) is None:
            return "invalid XML format"
        else:
            return ""

    @route('getMessage', methods=['GET'])
    def get_message(self) -> bytes:
        if db.session.query(Message).count() > 0:
            message_in_xml = convert_to_xml(db.session.query(Message)[0])
        else:
            return "There are no messages in the database"

        convert_to_pretty_xml = lxml.etree.fromstring(str(message_in_xml.decode('utf-8')))

        db.session.delete(db.session.query(Message)[0])
        db.session.commit()

        return lxml.etree.tostring(convert_to_pretty_xml, pretty_print=True, encoding='UTF-8',
                                   method='xml', xml_declaration=True)
