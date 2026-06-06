"""
NASCAR Points Standings Board

Adapted from the NHL standings board. The scroll/render structure is preserved —
only the data layer needs to be wired in when the NASCAR standings API is integrated.

HOW THE NHL VERSION WORKED (use as a guide):
  - data.standings held a standings object populated from the NHL API
  - Standings were grouped by conference or division, selected via config
  - draw_standing() iterated a list of team records, drawing one row per team
    with team colors, abbreviation, W-L-OT record, and points

NASCAR TODO:
  1. Add a standings URL to nascar_api/data.py:
       CAR_STANDINGS_URL = CAR_BASE_URL + "cacher/{year}/{series}/standings.json"

  2. Add a get_standings(year, series) function to nascar_api/data.py that calls
     that URL and returns the parsed JSON.

  3. Add a standings_info(year, series) function to nascar_api/info.py that builds
     a list of dicts like:
       {
           "position": 1,
           "car_number": "24",
           "driver_name": "William Byron",
           "points": 512,
           "wins": 3,
           "in_playoffs": True
       }

  4. In data.py, add self.standings = {} and populate it in refresh_daily() by calling
     nascar_api.info.standings_info(self.year, series_id) for each preferred series.

  5. Wire up the Standings board in boards.py and add "standings" to the desired
     states in config.json.

DISPLAY IDEAS:
  - Header row: series name colored with series_colors bg
  - Each row: position | car number | driver last name | points
  - Highlight playoff drivers (inPlayoffs == True) with a different row color
  - Scroll through full field or top N drivers (configurable)
"""

from PIL import Image, ImageDraw
import debug


class Standings:
    """
    NASCAR points standings board. Scrolls through the championship standings
    for one or more series.

    Data source (TODO): data.standings — a dict keyed by series_id, each value
    being a list of driver standing dicts (see nascar_api/info.py TODO above).
    """

    def __init__(self, data, matrix, sleepEvent):
        self.data = data
        self.matrix = matrix
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()

    def render(self):
        # TODO: replace this guard with a check against data.standings once it exists
        if not hasattr(self.data, 'standings') or not self.data.standings:
            debug.error("Standings board: no standings data available")
            self.sleepEvent.wait(5)
            return

        # TODO: iterate over data.config.preferred_series (or all series in data.standings)
        # For each series, call draw_standings() and scroll the result, similar to how
        # the NHL version iterated over conferences/divisions.
        #
        # Example structure to implement:
        #
        # for series_id, records in self.data.standings.items():
        #     im_height = (len(records) + 1) * 7
        #     image = draw_standings(self.data, series_id, records, im_height, self.matrix.width)
        #     i = 0
        #     self.matrix.draw_image((0, i), image)
        #     self.matrix.render()
        #     self.sleepEvent.wait(5)
        #     while i > -(im_height - self.matrix.height) and not self.sleepEvent.is_set():
        #         i -= 1
        #         self.matrix.draw_image((0, i), image)
        #         self.matrix.render()
        #         self.sleepEvent.wait(0.2)
        #     self.sleepEvent.wait(5)

        debug.info("Standings board: not yet implemented")
        self.sleepEvent.wait(5)


def draw_standings(data, series_id, records, img_height, width):
    """
    Draw a scrollable standings image for one series.

    series_id: int or str (1=Cup, 2=Xfinity, 3=Truck)
    records:   list of driver standing dicts (see TODO in module docstring)

    HOW THE NHL VERSION WORKED (draw_standing):
      - Drew a header row with the conference/division name
      - For each team: colored bg rectangle using team_colors, abbreviation,
        W-L-OT record, and points right-aligned
      - Row height was 7px throughout

    NASCAR ADAPTATION NOTES:
      - Use series_colors for the header bg instead of team_colors
      - Each row: position number, car number, driver last name, points
      - Consider a small colored dot or different row bg for playoff drivers
      - Points can be right-aligned like NHL did with the points column
      - Car number column width ~10px, name ~30px, points right-aligned
    """
    layout = data.config.layout
    image = Image.new('RGB', (width, img_height))
    draw = ImageDraw.Draw(image)

    row_height = 7
    row_pos = 0

    # TODO: draw header using series_colors
    # series_bg = data.config.series_colors.color("{}.bg".format(series_id))
    # series_txt = data.config.series_colors.color("{}.text".format(series_id))
    # series_names = {1: "CUP", 2: "NXS", 3: "TRUCKS"}
    # draw.rectangle([0, 0, width - 1, row_height - 1],
    #                fill=(series_bg["r"], series_bg["g"], series_bg["b"]))
    # draw.text((1, 0), series_names.get(int(series_id), "NASCAR"),
    #           fill=(series_txt["r"], series_txt["g"], series_txt["b"]), font=layout.font)
    row_pos += row_height

    # TODO: draw each driver row
    # for driver in records:
    #     pos     = str(driver["position"])
    #     car_no  = str(driver["car_number"])
    #     name    = driver["driver_name"].split()[-1]  # last name only
    #     points  = str(driver["points"])
    #     in_playoffs = driver.get("in_playoffs", False)
    #
    #     row_bg = (0, 60, 0) if in_playoffs else ((0, 0, 0) if row_pos % 14 == 7 else (20, 20, 20))
    #     draw.rectangle([0, row_pos, width - 1, row_pos + row_height - 1], fill=row_bg)
    #     draw.text((1,  row_pos), pos,    fill=(255, 255, 255), font=layout.font)
    #     draw.text((9,  row_pos), car_no, fill=(255, 255, 0),   font=layout.font)
    #     draw.text((18, row_pos), name,   fill=(255, 255, 255), font=layout.font)
    #     draw.text((54, row_pos), points, fill=(255, 255, 255), font=layout.font)
    #     row_pos += row_height

    return image
