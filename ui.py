import curses
import curses.panel
import curses.textpad
import re
from urllib.parse import urlparse
import os

# Minimal terminal size
MIN_LINES = 48
MIN_COLS = 150


class Gui:

    def __init__(self):
        self.MENU_Y = 0
        self.MENU_X = 0
        self.MENU_H = 24
        self.MENU_W = 0  
        self.DATA_Y = 1
        self.DATA_X = 0
        self.DATA_H = 29
        self.DATA_W = 32
        self.PLAYERS_Y = 1
        self.PLAYERS_X = self.DATA_X + self.DATA_W + 2
        self.PLAYERS_H = 21
        self.PLAYERS_W = 66
        self.DATA_Y = 1
        self.DATA_X = 0
        self.DATA_H = 29
        self.DATA_W = 32
        self.LOG_Y = self.DATA_Y + self.DATA_H + 2
        self.LOG_X = 0
        self.LOG_H = 12
        self.LOG_W = self.DATA_W + self.PLAYERS_W + 2
        self.menu_win = None 
        self.data_win = None
        self.log_win = None
        self.cursor_x = 0
        self.cursor_y = 0
        self.stdscr = curses.initscr()
        curses.start_color()
        # Basic color set
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        # check for minimal screen size
        screen_y, screen_x = self.stdscr.getmaxyx()
        if screen_y < MIN_LINES or screen_x < MIN_COLS:
            # Try resizing terminal
            curses.resize_term(MIN_LINES, MIN_COLS)
            if not curses.is_term_resized(MIN_LINES, MIN_COLS):
                self.quit_ui()
                print ("Unable to change your terminal size. Your terminal must be at least", \
                        MIN_LINES, "lines and", MIN_COLS, "columns and it actually has", \
                        screen_y, "lines and", screen_x, "columns.")
                quit(1)
        # Screen is up
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        # - /screen init ----

    def clear(self):
        self.stdscr.erase()
        if self.data_win:
            self.data_win.erase()
        if self.menu_win:
            self.menu_win.erase()
        curses.doupdate() 

    def draw_news_windows(self):
        if self.menu_win:
            self.menu_win.erase()
        self.draw_log_win()
        # self.draw_banner()
        curses.panel.update_panels()
        curses.doupdate()

    def draw_log_win(self):
        """Draw log window"""
        self.stdscr.addstr(self.LOG_Y - 1, self.LOG_X + 1, "Log", curses.A_BOLD)
        self.log_win = curses.newwin(self.LOG_H, self.LOG_W, self.LOG_Y, self.LOG_X)
        self.log_win.box()
        self.log_pan = curses.panel.new_panel(self.log_win)


    def ask_action(self):
        """Return the inputed value"""
        k = self.menu_win.getkey()
        return k
        
    def draw_banner(self):
            self.menu_win.clear()
            self.menu_win.box()
            self.menu_pan = curses.panel.new_panel(self.menu_win)
            title1="           _           _    _____         _                 _             _"           
            title2="          (_)         (_)  |_   _|       | |               | |           (_)          "
            title3=" _ __ ___  _ _ __ ___  _ _ __| | ___  ___| |__  _ __   ___ | | ___   __ _ _  ___  ___ "
            title4="| '_ ` _ \| | '_ ` _ \| | '__| |/ _ \/ __| '_ \| '_ \ / _ \| |/ _ \ / _` | |/ _ \/ __|"
            title5="| | | | | | | | | | | | | |  | |  __/ (__| | | | | | | (_) | | (_) | (_| | |  __/\__ \""
            title6="|_| |_| |_|_|_| |_| |_|_|_|  \_/\___|\___|_| |_|_| |_|\___/|_|\___/ \__, |_|\___||___/"
            title7="                                                                     __/ |            "
            title8="                                                                    |___/            " 
            # Centering calculations
            screen_y, screen_x = self.stdscr.getmaxyx()
            offset = int((screen_x // 2) - (len(title5) // 2) - len(title5) % 2)
            self.menu_win.addstr(1, offset, title1, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(2, offset, title2, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(3, offset, title3, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(4, offset, title4, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(5, offset, title5, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(6, offset, title6, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(7, offset, title7, curses.A_BOLD + curses.color_pair(4))
            self.menu_win.addstr(8, offset, title8, curses.A_BOLD + curses.color_pair(4))

    def ask_main_menu(self):
            """Display main menu window and ask for choice"""
            screen_y, screen_x = self.stdscr.getmaxyx()
            offset = screen_x // 2 - 25
            choice = "0"
            options = ["1", "2", "3", "4", "5"]
            self.menu_win = curses.newwin(self.MENU_H, self.MENU_W, self.MENU_Y, self.MENU_X)
            self.draw_banner()
            self.menu_win.addstr(9, offset + 8, "Please, choose an option:", curses.A_BOLD)
            self.menu_win.addstr(11, offset + 10, "1", curses.A_BOLD)
            self.menu_win.addstr(11, offset + 12, "- Get Top Articles (Global) ")
            self.menu_win.addstr(13, offset + 10, "2", curses.A_BOLD)
            self.menu_win.addstr(13, offset + 12, "- Get Top Articles United States")
            self.menu_win.addstr(15, offset + 10, "3", curses.A_BOLD)
            self.menu_win.addstr(15, offset + 12, "- Get 100 Articles URL")
            self.menu_win.addstr(17, offset + 10, "4", curses.A_BOLD)
            self.menu_win.addstr(17, offset + 12, "- Load game from URL")
            self.menu_win.addstr(19, offset + 10, "5", curses.A_BOLD)
            self.menu_win.addstr(19, offset + 12, "- Quit")
            while choice not in options:
                choice = self.ask_action()
            return choice

    def quit_ui(self):
        """Quit the UI and restore terminal state"""
        self.stdscr.clear()
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.curs_set(1)
        curses.endwin()
        self.running = False