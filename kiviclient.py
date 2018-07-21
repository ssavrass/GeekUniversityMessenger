# -*- coding: utf-8 -*-

import kivy
import time

kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder
from kivy.clock import Clock

from database import SqliteDB, Message, User
from graphicchat import GraphicChat
from authenticate import client_authenticate



Builder.load_string('''

#: import ListAdapter kivy.adapters.listadapter.ListAdapter
#: import ListItemButton kivy.uix.listview.ListItemButton


<ListItemButton>:
    selected_color: 0, 0, 1, 1
    deselected_color: 0, 0, 1, 1

<ChatBox>:
    orientation: "vertical"
    message_input: message
    message_list: message_list_view
    contact_list: contact_list_view
    padding: 3
    spacing: 3
    BoxLayout:
        orientation: "horizontal"
        Label:
            text: "Chat"
            font_size: 16
            size_hint: [.1,.1]
            pos_hint: {'top':1}
            canvas.before:
                Color:
                    rgba: 1, 0, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size 
        

        Label:
            text: "Contacts"
            font_size: 16
            size_hint: [.1,.1]
            pos_hint: {'top':1}
            canvas.before:
                Color:
                    rgba: 0, 0, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size 
            


    BoxLayout:
        orientation: "horizontal"
        BoxLayout:
            pos_hint: {'x': 0, 'center_y': 1}
            size_hint: [1,1.6]
            ListView:
                
                id: message_list_view
                font_size: 16
                adapter:
                    ListAdapter(data=["Hey"], cls=ListItemButton)

        
        BoxLayout:
            pos_hint: {'x': 0, 'center_y': 1.4}

            ListView:
               
                id: contact_list_view
                adapter:
                    ListAdapter(data=["Sergey"], cls=ListItemButton)
        
    BoxLayout:
        orientation: "horizontal"
            
        BoxLayout:
            size_hint_y: None
            height: "40dp"
        
            TextInput:
                id: message
                hint_text: "Type message..."
                # pos: root.x + 10, (root.height / 4)
                size: 300,50
                color: .10,.9,1,2

            # Label:
            #     id: label
            #     text: ""
            #     # pos: root.x + 410, 525
            #     color: 244, 65, 223,1

        BoxLayout:
            size_hint_y: None
            height: "40dp"    

            Button:
                text: "Send Message"
                font_size: 14
                pos: root.x + 320, (root.height / 4)
                size: 100,50
                on_press: root.send_message()
            
''')


class ChatBox(BoxLayout):
    
    def __init__(self, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.db = SqliteDB()
        self.chat = GraphicChat()
        client_authenticate(self.chat._sock, b'secretkey')
        self.populate()
        


    message_input = ObjectProperty()
    time_input = ObjectProperty()
    message_list = ObjectProperty()
    contact_list = ObjectProperty()

    def send_message(self):
        timestamp = time.ctime()
        message = self.message_input.text
        messagetime = message + " " + timestamp
        self.db.add_message("2", "3", message, timestamp)
        self.chat.send(message)
        self.message_list.adapter.data.extend([messagetime])
        self.message_list._trigger_reset_populate()

    def populate(self):

        messages = self.db.get_all_messages(2, 3)
        contacts = self.db.get_all_contacts()
        
        for itm in messages:
            messagetime = itm.message + " " + itm.timestamp
            self.message_list.adapter.data.extend([messagetime])

        for itm in contacts:
            contact = itm.fullname
            self.contact_list.adapter.data.extend([contact])
            
        self.message_list._trigger_reset_populate()
        self.contact_list._trigger_reset_populate()




class ClientApp(App):
    # This returns the content we want in the windo

    def build(self):

        
        return ChatBox();



clientapp = ClientApp()
clientapp.run()