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
    
    def start_ui(self):
        self.gui = ui.Gui()
        self.news = news.news()
        choice = self.gui.ask_main_menu()
        if choice == '1':
            self.gui.draw_news_windows()
            # self.gui.display_top_news_articles()
        elif choice == '2':
            self.gui.draw_news_windows()
        elif choice == '5':
             # quit
            self.gui.quit_ui()
            exit(0)
        if self.gui.running and self.gui.help_win:
            key = None
            while key != 'm':
                key = self.gui.ask_quit()
                if key == 'q':
                    self.gui.quit_ui()
                    exit(0)
        self.gui.clear()
        self.start_ui()

faulthandler.enable()

if __name__ == "__main__":
    client = Client()
    try:
        client.start_ui()
    except Exception as e:
        if hasattr(client, 'gui') and client.gui is not None:
            client.gui.quit_ui()
        raise e
    