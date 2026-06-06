"""
A Board is simply a display object with specific parameters made to be shown on screen.
    TODO: Make the board system customizable so that all the user needs to do is paste a board file and modify the
        config file to add the custom board.
"""
import debug
from boards.clock import Clock
from boards.pbdisplay import pbDisplay
from boards.wxWeather import wxWeather
from boards.wxAlert import wxAlert
from boards.christmas import Christmas
from boards.seasoncountdown import SeasonCountdown
from boards.wxForecast import wxForecast
from boards.screensaver import screenSaver
from boards.schedule import Schedule
from boards.results import Results
from time import sleep

import traceback

class Boards:
    def __init__(self):
        pass

    # Board handler for PushButton
    def _pb_board(self, data, matrix, sleepEvent):

        board = getattr(self, data.config.pushbutton_state_triggered1)
        board(data, matrix, sleepEvent)

    # Board handler for Weather Alert
    def _wx_alert(self, data, matrix, sleepEvent):

        board = getattr(self, "wxalert")
        board(data, matrix, sleepEvent)

    # Board handler for screensaver
    def _screensaver(self, data, matrix, sleepEvent):

        board = getattr(self, "screensaver")
        board(data, matrix, sleepEvent)

    # Board handler for Off day / No race state
    def _no_race(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_off_day[bord_index])
            data.curr_board = data.config.boards_off_day[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding off_day -> " + data.config.boards_off_day[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in off day loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in off day loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False

            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_off_day) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _scheduled(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_scheduled[bord_index])
            data.curr_board = data.config.boards_scheduled[bord_index]
            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding scheduled -> " + data.config.boards_scheduled[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in scheduled loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in scheduled loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False

            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_scheduled) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _intermission(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_intermission[bord_index])
            data.curr_board = data.config.boards_intermission[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding intermission -> " + data.config.boards_intermission[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in intermission....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            ## Don't Display the Screensaver Board in "live game mode"
            # if data.screensaver:
            #     if not data.pb_trigger:
            #         debug.info('Screensaver triggered in intermission loop....')
            #         #Display the board from the config
            #         board = getattr(self,"screensaver")
            #         data.curr_board = "screensaver"
            #         data.prev_board = data.config.boards_off_day[bord_index]
            #         bord_index -= 1
            #     else:
            #         data.pb_trigger = False
        
            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_intermission) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def _post_game(self, data, matrix, sleepEvent):
        bord_index = 0
        while True:
            board = getattr(self, data.config.boards_post_game[bord_index])
            data.curr_board = data.config.boards_post_game[bord_index]

            if data.pb_trigger:
                debug.info('PushButton triggered....will display ' + data.config.pushbutton_state_triggered1 + ' board ' + "Overriding post_game -> " + data.config.boards_post_game[bord_index])
                if not data.screensaver:
                    data.pb_trigger = False
                board = getattr(self,data.config.pushbutton_state_triggered1)
                data.curr_board = data.config.pushbutton_state_triggered1
                bord_index -= 1

            # Display the Weather Alert board
            if data.wx_alert_interrupt:
                debug.info('Weather Alert triggered in post game loop....will display weather alert board')
                data.wx_alert_interrupt = False
                #Display the board from the config
                board = getattr(self,"wxalert")
                data.curr_board = "wxalert"
                bord_index -= 1

            # Display the Screensaver Board
            if data.screensaver:
                if not data.pb_trigger:
                    debug.info('Screensaver triggered in post game loop....')
                    #Display the board from the config
                    board = getattr(self,"screensaver")
                    data.curr_board = "screensaver"
                    data.prev_board = data.config.boards_off_day[bord_index]
                    bord_index -= 1
                else:
                    data.pb_trigger = False


            board(data, matrix, sleepEvent)

            if bord_index >= (len(data.config.boards_post_game) - 1):
                return
            else:
                if not data.pb_trigger or not data.wx_alert_interrupt or not data.screensaver:
                    bord_index += 1

    def fallback(self, data, matrix, sleepEvent):
        Clock(data, matrix, sleepEvent)

    # -------------------------------------------------------------------------
    # NASCAR boards
    # -------------------------------------------------------------------------

    def schedule(self, data, matrix, sleepEvent):
        """Upcoming race schedule board."""
        Schedule(data, matrix, sleepEvent).render()

    def results(self, data, matrix, sleepEvent):
        """Live running order / race results board."""
        Results(data, matrix, sleepEvent).render()

    # -------------------------------------------------------------------------
    # Utility boards
    # -------------------------------------------------------------------------

    def clock(self, data, matrix, sleepEvent):
        Clock(data, matrix, sleepEvent)

    def pbdisplay(self, data, matrix, sleepEvent):
        pbDisplay(data, matrix, sleepEvent)

    def weather(self, data, matrix, sleepEvent):
        wxWeather(data, matrix, sleepEvent)

    def wxalert(self, data, matrix, sleepEvent):
        wxAlert(data, matrix, sleepEvent)

    def wxforecast(self, data, matrix, sleepEvent):
        wxForecast(data, matrix, sleepEvent)

    def screensaver(self, data, matrix, sleepEvent):
        screenSaver(data, matrix, sleepEvent)

    def christmas(self, data, matrix, sleepEvent):
        Christmas(data, matrix, sleepEvent).draw()

    def seasoncountdown(self, data, matrix, sleepEvent):
        SeasonCountdown(data, matrix, sleepEvent).draw()
