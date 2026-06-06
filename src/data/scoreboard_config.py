from utils import get_file
from data.layout import Layout
from data.colors import Color
from config.main import Config  
# TODO: Re-enable once NASCAR config.json and config.schema.json are finalized
# from nhl_setup.validate_json import validateConf
import json
import os
import sys
import debug

class ScoreboardConfig:
    def __init__(self, filename_base, args, size):
        json = self.__get_config(filename_base)

        self.testing_mode = False

        # Misc config options
        self.debug = json["debug"]
        self.loglevel = json["loglevel"]
        self.live_mode = json["live_mode"]

        # Preferences
        self.end_of_day = json["preferences"]["end_of_day"]
        self.time_format = self.__get_time_format(json["preferences"]["time_format"])
        self.location = json["preferences"]["location"]

        self.live_game_refresh_rate = json["preferences"]["live_game_refresh_rate"]

        # NASCAR — which series to display (1=Cup, 2=Xfinity, 3=Truck). Empty list = all series.
        self.preferred_series = json["preferences"].get("preferred_series", [])

        #Screen Saver entries
        self.screensaver_enabled = json["sbio"]["screensaver"]["enabled"]
        self.screensaver_animations = json["sbio"]["screensaver"]["animations"]
        self.screensaver_start = json["sbio"]["screensaver"]["start"]
        self.screensaver_stop = json["sbio"]["screensaver"]["stop"]
        self.screensaver_data_updates = json["sbio"]["screensaver"]["data_updates"]
        self.screensaver_motionsensor = json["sbio"]["screensaver"]["motionsensor"]
        self.screensaver_ms_pin = json["sbio"]["screensaver"]["pin"]
        self.screensaver_ms_delay = json["sbio"]["screensaver"]["delay"]

        # Dimmer preferences
        self.dimmer_enabled = json["sbio"]["dimmer"]["enabled"]
        self.dimmer_source = json["sbio"]["dimmer"]["source"]
        self.dimmer_daytime = json["sbio"]["dimmer"]["daytime"]
        self.dimmer_nighttime = json["sbio"]["dimmer"]["nighttime"]
        self.dimmer_offset = json["sbio"]["dimmer"]["offset"]
        self.dimmer_frequency = json["sbio"]["dimmer"]["frequency"]
        self.dimmer_light_level_lux = json["sbio"]["dimmer"]["light_level_lux"]
        self.dimmer_mode = json["sbio"]["dimmer"]["mode"]
        self.dimmer_sunset_brightness = json["sbio"]["dimmer"]["sunset_brightness"]
        self.dimmer_sunrise_brightness = json["sbio"]["dimmer"]["sunrise_brightness"]

        # Pushbutton preferences
        self.pushbutton_enabled = json["sbio"]["pushbutton"]["enabled"]
        self.pushbutton_bonnet = json["sbio"]["pushbutton"]["bonnet"]
        self.pushbutton_pin = json["sbio"]["pushbutton"]["pin"]
        # Reboot duration should be a medium time press (ie greater than 2 seconds)
        self.pushbutton_reboot_duration = json["sbio"]["pushbutton"]["reboot_duration"]
        # Override process is used to trigger a different process other than the default.  reboot uses /sbin/reboot poweroff uses /sbin/poweroff
        self.pushbutton_reboot_override_process = json["sbio"]["pushbutton"]["reboot_override_process"]
        self.pushbutton_display_reboot = json["sbio"]["pushbutton"]["display_reboot"]
        # Poweroff duration should be a long press (greater than 5 or 6 seconds).  This is ties to the hold_time property of a button
        self.pushbutton_poweroff_duration = json["sbio"]["pushbutton"]["poweroff_duration"]
        self.pushbutton_poweroff_override_process = json["sbio"]["pushbutton"]["poweroff_override_process"]
        self.pushbutton_display_halt = json["sbio"]["pushbutton"]["display_halt"]
        self.pushbutton_state_triggered1 = json["sbio"]["pushbutton"]["state_triggered1"]
        self.pushbutton_state_triggered1_process = json["sbio"]["pushbutton"]["state_triggered1_process"]

        # Weather board preferences
        self.weather_enabled = json["boards"]["weather"]["enabled"]
        self.weather_view = json["boards"]["weather"]["view"]
        self.weather_units = json["boards"]["weather"]["units"]
        self.weather_duration = json["boards"]["weather"]["duration"]
        self.weather_data_feed = json["boards"]["weather"]["data_feed"]
        self.weather_owm_apikey = json["boards"]["weather"]["owm_apikey"]
        self.weather_update_freq = json["boards"]["weather"]["update_freq"]
        # Show curr temp, humidity on clock
        self.weather_show_on_clock = json["boards"]["weather"]["show_on_clock"]
        # Forecast settings
        self.weather_forecast_enabled = json["boards"]["weather"]["forecast_enabled"]
        #Number of days up to 3 for forecast
        self.weather_forecast_days = json["boards"]["weather"]["forecast_days"]
        #How frequent, in hours, to update the forecast
        self.weather_forecast_update = json["boards"]["weather"]["forecast_update"]

        #Weather Alerts Preferences
        self.wxalert_alert_feed = json["boards"]["wxalert"]["alert_feed"]
        #Allow the weather thread to interrupt the current flow of the display loop and show an alert if it shows up
        #Similar to how a pushbutton interrupts the flow
        self.wxalert_show_alerts = json["boards"]["wxalert"]["show_alerts"]  
        #Show expire time instead of effective time of NWS alerts
        self.wxalert_nws_show_expire = json["boards"]["wxalert"]["nws_show_expire"]
        # Display on top and bottom bar the severity (for US) and type
        self.wxalert_alert_title = json["boards"]["wxalert"]["alert_title"]
        # Display static alert or scrolling
        self.wxalert_scroll_alert = json["boards"]["wxalert"]["scroll_alert"]
        # How long to display static alert in seconds
        self.wxalert_alert_duration = json["boards"]["wxalert"]["alert_duration"]
        # Show any alerts on clock
        self.wxalert_show_on_clock = json["boards"]["wxalert"]["show_on_clock"]
        self.wxalert_update_freq = json["boards"]["wxalert"]["update_freq"]



        # States — board lists for each race day phase
        self.boards_off_day = json["states"]["off_day"]
        self.boards_scheduled = json["states"]["scheduled"]
        self.boards_pre_race = json["states"]["pre_race"]
        self.boards_post_race = json["states"]["post_race"]

        # Schedule board
        self.schedule_upcoming_days = json["boards"]["schedule"].get("upcoming_days", 14)

        # Clock
        self.clock_board_duration = json["boards"]["clock"]["duration"]
        self.clock_hide_indicators = json["boards"]["clock"]["hide_indicator"]
        self.clock_team_colors =  json["boards"]["clock"]["preferred_team_colors"]
        self.clock_clock_rgb =  json["boards"]["clock"]["clock_rgb"]
        self.clock_date_rgb =  json["boards"]["clock"]["date_rgb"]
        self.clock_flash_seconds =  json["boards"]["clock"]["flash_seconds"]

        # Fonts
        self.layout = Layout()

        # load colors
        self.series_colors = Color(self.__get_config(
            "colors/series"
        ))

        self.config = Config(size)

        if args.testing_mode:
            self.testing_mode = True
            

    def read_json(self, filename):
        # Find and return a json file

        j = {}
        msg = ""
        path = get_file("config/{}".format(filename))
        if os.path.isfile(path):
            try:
                j = json.load(open(path))
                msg = "json loaded OK"
            except json.decoder.JSONDecodeError as e:
                msg = "Unable to load json: {0}".format(e)
                j = {}
        return j, msg

    def __get_config(self, base_filename, error=None):
        # Look and return config.json file

        filename = "{}.json".format(base_filename)

        (reference_config, error) = self.read_json(filename)
        if not reference_config:
            if (error):
                debug.error(error)
            else:
                debug.error("Invalid {} config file. Make sure {} exists in config/".format(base_filename, base_filename))
            sys.exit(1)


        # TODO: Re-enable config validation once NASCAR config.json and config.schema.json are finalized.
        # Update the schema path and messaging below before uncommenting.
        # if base_filename == "config":
        #     debug.error("INFO: Validating config.json.....")
        #     conffile = "config/config.json"
        #     schemafile = "config/config.schema.json"
        #     confpath = get_file(conffile)
        #     schemapath = get_file(schemafile)
        #     (valid, msg) = validateConf(confpath, schemapath)
        #     if valid:
        #         debug.error("INFO: config.json passes validation")
        #     else:
        #         debug.warning("WARN: config.json fails validation: error: [{0}]".format(msg))
        #         debug.warning("WARN: Rerun the nhl_setup app to create a valid config.json")
        #         sys.exit(1)

        return reference_config

    def __get_time_format(self, config):
        # Set the time format to 12h.
        time_format = "%I:%M"

        # Check if the time format is different in the config. if so, change it.
        if config == "24h":
            time_format = "%H:%M"

        return time_format

