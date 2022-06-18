import time
import json
import threading
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.uix.progressbar import ProgressBar
from db_management.db_repo import DbRepo
from db_management.db_config import local_session, config
from db_management.db_data_object import DbDataObject
from db_management.db_rabbit_producer import DbRabbitProducer
from db_management.refresh_db import refresh_db


class myThread(threading.Thread):

    def __init__(self, progress_bar):
        threading.Thread.__init__(self)
        self.progress_bar = progress_bar

    def run(self):
        while self.progress_bar.value < 100:
            time.sleep(1 / 25)
            self.progress_bar.value += 1
        print('Data Imported')


class MyWidget(Widget):
    progress_bar = ObjectProperty()
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    rabbit_producer = DbRabbitProducer('DataToGenerate')
    repo = DbRepo(local_session)

    def __init__(self, **kwa):
        super(MyWidget, self).__init__(**kwa)
        self.progress_bar = ProgressBar()
        self.popup = Popup(title='Importing' if self.ids.rbutton2.state == 'normal' else 'Refreshing DB',
                           content=self.progress_bar)
        self.popup.bind(on_open=self.puopen)

    def pop(self):
        if self.ids.rbutton2.state == 'down': self.reset_db()
        try:
            data_object = DbDataObject(customers=int(self.customers.text),
                                       airlines=int(self.airline_companies.text),
                                       flights_per_company=int(self.flights_per_company.text),
                                       tickets_per_customer=int(self.tickets_per_customer.text))
            data_object.validate()
            self.rabbit_producer.publish(json.dumps(data_object.__dict__()))
            print("Airline Companies:", self.airline_companies.text,
                  ", Customers:", self.customers.text,
                  ", Flights Per Company:", self.flights_per_company.text,
                  ", Tickets Per Customer:", self.tickets_per_customer.text)
        except:
            return "Invalid Input"
        self.progress_bar.value = 0
        self.popup.open()

    def puopen(self, instance):
        t1 = myThread(self.progress_bar)
        t1.start()

    def switchstate1(self):
        self.ids.rbutton1.state = 'down'
        self.ids.rbutton2.state = 'normal'

    def switchstate2(self):
        self.ids.rbutton2.state = 'down'
        self.ids.rbutton1.state = 'normal'


Builder.load_file(config['db']['kv_file'])


class MyApp(App):
    def build(self): return MyWidget()


if __name__ in ("__main__"):
    MyApp().run()
