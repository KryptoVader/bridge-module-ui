import sqlite3
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path(os.path.join("data", "locations.db"))

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()

    def get_states(self):
        self.cur.execute("SELECT DISTINCT State FROM locations ORDER BY State")
        return [row[0] for row in self.cur.fetchall()]

    def get_districts(self, state):
        self.cur.execute(
            "SELECT District FROM locations WHERE State=? ORDER BY District",
            (state,)
        )
        return [row[0] for row in self.cur.fetchall()]

    def get_location_data(self, district):
        self.cur.execute(
            "SELECT Wind, SeismicZone, SeismicFactor, TempMax, TempMin FROM locations WHERE District=?",
            (district,)
        )
        return self.cur.fetchone()
