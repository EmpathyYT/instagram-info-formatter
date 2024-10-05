import os
from datetime import datetime
from urllib.parse import uses_relative

from bs4 import BeautifulSoup
import json
import copy
from langdetect import detect

from utils.organizer import Organizer


class HtmlGenerator:
    def __init__(self, jsonpath):
        self.soup = BeautifulSoup()
        self.data = json.load(open(jsonpath))
        self.users = []
        self.home_page_template = 'design/base_homepage.html'
        self.message_page_template_path = 'design/base_user_page.html'
        self.drop_down_html = ""
        self.runner()

    def generate_dropdown(self):
        with open(self.message_page_template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            dropdown_menu = soup.find('ul', {'class': 'dropdown-menu'})
            for key in self.users:
                new_li = soup.new_tag('li')
                new_a = soup.new_tag('a', href=f"Generated Messages/Messages/{self.users.index(key)}.html", **{'class': 'dropdown-item'})
                new_a.string = key
                new_li.append(new_a)
                dropdown_menu.append(new_li)

            self.drop_down_html = dropdown_menu

    def generate_home_page(self):
        with open(self.home_page_template, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            user_list = soup.find('div', {'class': 'list-group'})
            for key in self.users:
                new_a = soup.new_tag('a', href=f'Messages/{self.users.index(key)}.html',
                                     **{'class': 'list-group-item list-group-item-action'})
                new_a.string = key
                user_list.append(new_a)

            new_html_file_path = 'Generated Messages/HomePage.html'
            with open(new_html_file_path, 'w', encoding='utf-8') as new_html:
                new_html.write(str(soup))

    def message_populater(self):
        with open(self.message_page_template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            for user in self.users:

                soup = copy.copy(BeautifulSoup(html_content, 'html.parser'))
                soup.find('h1').string = user
                message_template = soup.find('div', {'class': 'message'})
                messages_list = soup.find('div', {'id': 'messages-holder'})
                for message in self.user_messages_getter(user):
                    try:
                        copied_message_template = copy.copy(message_template)
                        reaction = "null"
                        if 'reactions' in message:
                            reaction = message.get('reactions')[0].get("reaction")
                        time_sent = datetime.fromtimestamp(message.get('timestamp_ms') / 1000)
                        message_sender = copied_message_template.find('h5')
                        message_sender.string = Organizer.language_checker(message.get('sender_name'))
                        message_content = copied_message_template.find('p')
                        message_content.string = Organizer.language_checker(message.get('content'))
                        copied_message_template['onclick'] = f"showMessageDetails('{time_sent.strftime('%Y-%m-%d %H:%M:%S %Z%z')}', '{reaction}')"
                        messages_list.append(copied_message_template)
                    except:
                        pass

                print('Generating HTML for ', user)
                new_html_file_path = f'Generated Messages/Messages/{self.users.index(user)}.html'
                os.makedirs(os.path.dirname(new_html_file_path), exist_ok=True)
                with open(new_html_file_path, 'w', encoding='utf-8') as new_html:
                    new_html.write(str(soup))

            message_template.decompose()

    def user_messages_getter(self, user):
        user_messages = self.data[user]
        return user_messages[::-1]

    def user_populater(self):
        for user in self.data.keys():
            self.users.append(user)
        self.users.remove('total_users')


    def runner(self):
        os.makedirs('Generated Messages', exist_ok=True)
        self.user_populater()
        #self.generate_dropdown()
        self.generate_home_page()
        self.message_populater()
