from random import randint
from pyluach.dates import HebrewDate
import svgwrite
import gi
gi.require_version('Gtk', '3.0')  # nopep8
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')  # nopep8
from gi.repository import AppIndicator3 as appindicator
import time
from datetime import datetime
from suntime import Sun, SunTimeException
import pytz
import os
import signal


APP_INDICATOR_ID = 'hebrew_date'


class MyIndicator:
    def __init__(self):
        self.indicator = appindicator.Indicator.new(
            APP_INDICATOR_ID,
            "...",
            appindicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.sun_times = SunTimes()
        self.set_icon()
        self.indicator.set_attention_icon_full("...", "desc")
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        gtk.main()

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem(label='רענון תאריך')
        item_quit.connect('activate', self.set_icon)
        item_full_date = gtk.MenuItem(label=HebrewDate.today().hebrew_date_string())
        menu.append(item_quit)
        menu.append(item_full_date)
        menu.show_all()
        return menu

    def set_icon(self, *args, **keywords):
        heb_day = (HebrewDate.today() + 1 if self.sun_times.is_after_sunset() else HebrewDate.today()).hebrew_day()
        icon_path = self.gen_icon_path(heb_day)
        dwg = svgwrite.Drawing(
            filename=icon_path,
            size=("36px", "24px"),
            profile="tiny"
        )
        dwg.add(dwg.text(
            heb_day,
            font_size="20px",
            font_family="SystemUI",
            insert=("4px", "18px"),
            fill="white",
        ))
        dwg.save()
        time.sleep(5)
        self.indicator.set_icon_full(icon_path, "Hebrew Date")

    def gen_icon_path(self, day):
        return os.path.abspath(f"heb_date_icon_{day}.svg")


class SunTimes:
    IL_LON = 35.217018
    IL_LAT = 31.771959
    IL_TZ = pytz.timezone("Asia/Jerusalem")

    def __init__(self) -> None:
        self.sun = Sun(self.IL_LAT, self.IL_LON)

    def is_after_sunset(self):
        today_sunset = self.sun.get_sunset_time().astimezone(self.IL_TZ)
        now = datetime.now(tz=self.IL_TZ)
        return now >= today_sunset


def main():
    MyIndicator()


main()
