import requests
import news
import ui
import os
import sys
import faulthandler


class Client:

    def __init__(self):
        self.gui = None
        self.news = None
    
    def startNews(self):
        self.gui = ui.Gui()
        self.news = news.news()
        # self.gui.draw_status_bar()
        choice = self.gui.ask_main_menu()
        if choice == '1':
            self.gui.draw_news_windows()
        elif choice == '5':
             # quit
            self.gui.quit_ui()
            exit(0)
        self.gui.clear()
        self.startNews()

faulthandler.enable()

if __name__ == "__main__":
    client = Client()
    try:
        client.startNews()
    except Exception as e:
        if hasattr(client, 'gui') and client.gui is not None:
            client.gui.quit_ui()
        raise e
    