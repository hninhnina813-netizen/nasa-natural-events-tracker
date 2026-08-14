from flask import Flask, render_template, request
import sqlite3
from model import EventFetcher

app = Flask(__name__)

DATABASE = "events.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watched_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eonet_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            category TEXT,
            status TEXT,
            longitude REAL,
            latitude REAL,
            event_date TEXT,
            magnitude REAL,
            mag_unit TEXT,
            source_url TEXT,
            note TEXT DEFAULT '',
            alert_active INTEGER DEFAULT 0,
            saved_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL UNIQUE,
            label TEXT NOT NULL
        )
        """
    )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT,
            searched_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
        """)

    conn.commit()
    conn.close()

@app.route("/")
def index():
        return "Welcome to the Natural Events Tracker"

@app.route("/browse")
def browse():
    fetcher = EventFetcher()
    selected_status = request.args.get("status", "open")
    selected_days = request.args.get("days", "30")
    selected_category = request.args.get("category", None)
    events = fetcher.fetch_events(
        status=selected_status,
        category=selected_category,
        days=int(selected_days),
        limit=50,
    )
    return render_template(
          "browse.html", 
          events=events,
          selected_status=selected_status,
          selected_days=selected_days,
          selected_category=selected_category
          )

@app.route("/event/<eonet_id>")
def event_detail(eonet_id):
      fetcher = EventFetcher()
      event = fetcher.fetch_event(eonet_id)
      return render_template("event_detail.html", event=event)

init_db()

if __name__ == "__main__":
       app.run(debug=True, port=5001)

    