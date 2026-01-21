import flet as ft

class BaseApp:

    def __init__(self, phone):
        self.phone = phone  # referencja do Nokii

    def build(self, width, height):
        return ft.Text("Empty app")

    def on_key(self, key):
        pass

    def on_call(self):
        pass

    def on_back(self):
        self.phone.show_menu()

    def on_arrow(self,arrow):
        pass