"""
NASCAR Driver Summary Board

Adapted from the NHL team_summary board. The scroll structure and side-panel
layout are preserved — the data layer and draw content need to be wired in
when driver summary data is available.

HOW THE NHL VERSION WORKED (use as a guide):
  - data.pref_teams held a list of preferred team IDs from config
  - For each team it loaded: team record (W-L-OT, GP, points), previous game
    result (opponent, W/L, score), and next game info (date, time, opponent)
  - The left side showed a team logo via LogoRenderer
  - The right side (37px wide) scrolled through the stats panel
  - draw_team_summary() built a tall image that scrolled upward

NASCAR TODO:
  1. Add driver standings data to data.py (see standings.py TODO for the API shape).
     You'll want each preferred driver's: position, points, wins, recent finish,
     next race info.

  2. Decide what "preferred drivers" means in config — probably a list of car
     numbers or driver IDs in config.json under preferences, similar to how
     preferred_teams worked in NHL. Add self.preferred_drivers to scoreboard_config.py.

  3. Add a driver photo or car number graphic in place of the team logo, or skip
     the logo panel and use the full width for stats.

  4. Wire up the DriverSummary board in boards.py and add "driver_summary" to
     the desired states in config.json.

DISPLAY IDEAS (37px right panel, scrolling):
  Row  0-6:  Driver name / car number header (series color bg)
  Row  7-13: "STANDINGS"  label
  Row 14-20: Position + points  (e.g. "P3  512pts")
  Row 21-27: Wins this season   (e.g. "3 WINS")
  Row 28-34: Playoff status     (e.g. "PLAYOFFS" in green or "BUBBLE" in yellow)
  Row 35-41: "LAST RACE" label
  Row 42-48: Finish position + track abbreviation
  Row 49-55: "NEXT RACE" label
  Row 56-62: Date + track
"""

from PIL import Image, ImageDraw
from utils import get_file
import debug


class DriverSummary:
    """
    NASCAR driver summary board. Shows season stats, recent finish, and
    next race for each preferred driver.

    Data source (TODO): data.driver_summaries — a dict keyed by driver_id/car_number,
    each value containing standings position, points, wins, last race, next race.
    """

    def __init__(self, data, matrix, sleepEvent):
        self.data = data
        self.matrix = matrix
        self.font = data.config.layout.font
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()

    def render(self):
        self.matrix.clear()

        # TODO: replace with a check against data.preferred_drivers once that exists
        # preferred_drivers = self.data.config.preferred_drivers  # e.g. ["24", "9"]
        # if not preferred_drivers:
        #     debug.error("DriverSummary: no preferred drivers configured")
        #     self.sleepEvent.wait(5)
        #     return

        # TODO: for each preferred driver, build and scroll the summary image.
        # The NHL version looped over preferred_teams and scrolled each one:
        #
        # for driver_id in preferred_drivers:
        #     driver_data = self.data.driver_summaries.get(driver_id)
        #     if not driver_data:
        #         continue
        #
        #     im_height = 67   # same as NHL — adjust based on how many rows you need
        #     i = 0
        #
        #     image = draw_driver_summary(self.data, driver_data, im_height)
        #
        #     # NHL used a logo on the left + a scrolling stats panel on the right.
        #     # For NASCAR, you could draw the car number large on the left, or use
        #     # the full 64px width for stats.
        #     self.matrix.clear()
        #     self.matrix.draw_image((0, 0), image)
        #     self.matrix.render()
        #     self.sleepEvent.wait(5)
        #
        #     while i > -(im_height - self.matrix.height) and not self.sleepEvent.is_set():
        #         i -= 1
        #         self.matrix.clear()
        #         self.matrix.draw_image((0, i), image)
        #         self.matrix.render()
        #         self.sleepEvent.wait(0.3)
        #
        #     self.sleepEvent.wait(5)

        debug.info("DriverSummary board: not yet implemented")
        self.sleepEvent.wait(5)


def draw_driver_summary(data, driver_data, im_height):
    """
    Draw a scrollable stats panel for a single driver.

    driver_data dict (TODO — define shape in nascar_api/info.py):
      {
          "car_number":  "24",
          "driver_name": "William Byron",
          "series_id":   1,
          "position":    3,
          "points":      512,
          "wins":        3,
          "in_playoffs": True,
          "last_race":   {"track": "CMS", "finish": 4},
          "next_race":   {"track": "Pocono", "date": "Jun 22"}
      }

    HOW THE NHL VERSION WORKED (draw_team_summary):
      - Built a 37px wide image (right panel only, left was the logo)
      - Used bg_color/txt_color from team_colors for section header rectangles
      - Sections: RECORD (GP, points, W-L-OT), LAST GAME (opponent, W/L, score),
        NEXT GAME (date, time, opponent)
      - Each section had a colored header bar and white text rows below it

    NASCAR ADAPTATION NOTES:
      - Replace bg_color/txt_color with series_colors for the driver's series
      - Replace RECORD section with STANDINGS (position, points, wins)
      - Replace LAST GAME with LAST RACE (track abbreviation, finish position)
      - Replace NEXT GAME with NEXT RACE (track, date)
      - Consider using full 64px width since there's no logo panel to work around
      - Add a playoff indicator row (green "PLAYOFFS" or yellow "BUBBLE" etc.)
    """
    layout = data.config.layout

    # TODO: get series colors for header bars
    # series_id = driver_data.get("series_id", 1)
    # bg = data.config.series_colors.color("{}.bg".format(series_id))
    # txt = data.config.series_colors.color("{}.text".format(series_id))
    # bg_color = (bg["r"], bg["g"], bg["b"])
    # txt_color = (txt["r"], txt["g"], txt["b"])

    image = Image.new('RGB', (37, im_height))
    draw = ImageDraw.Draw(image)

    # TODO: draw driver name / car number header
    # draw.rectangle([0, -1, 36, 6], fill=bg_color)
    # draw.text((1, 0), "#{} {}".format(driver_data["car_number"],
    #           driver_data["driver_name"].split()[-1]),
    #           fill=txt_color, font=layout.font)

    # TODO: draw STANDINGS section
    # draw.rectangle([0, 14, 36, 20], fill=bg_color)
    # draw.text((1, 14), "STANDINGS", fill=txt_color, font=layout.font)
    # draw.text((0, 21), "P{}  {}pts".format(driver_data["position"],
    #           driver_data["points"]), fill=(255, 255, 255), font=layout.font)
    # draw.text((0, 27), "{} WINS".format(driver_data["wins"]),
    #           fill=(255, 255, 255), font=layout.font)

    # TODO: draw playoff status
    # if driver_data.get("in_playoffs"):
    #     draw.text((0, 33), "PLAYOFFS", fill=(50, 255, 50), font=layout.font)

    # TODO: draw LAST RACE section
    # draw.rectangle([0, 42, 36, 48], fill=bg_color)
    # draw.text((1, 42), "LAST RACE", fill=txt_color, font=layout.font)
    # last = driver_data.get("last_race")
    # if last:
    #     draw.text((0, 49), "P{} {}".format(last["finish"], last["track"]),
    #               fill=(255, 255, 255), font=layout.font)

    # TODO: draw NEXT RACE section
    # draw.rectangle([0, 56, 36, 62], fill=bg_color)
    # draw.text((1, 56), "NEXT RACE", fill=txt_color, font=layout.font)
    # next_r = driver_data.get("next_race")
    # if next_r:
    #     draw.text((0, 63), next_r["track"], fill=(255, 255, 255), font=layout.font)

    return image
