# NASA Natural Events Tracker

The app works as an indicator to track the natural events happening in the world. 
On the browse page, you can filter the days, status and category and also shows the date and time and coordinates of the events. 
The app has clickable links where when you click the link, showing its magnitude when available and a link to the official source webpage.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate #Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run
```

The app will be available at `http://127.0.0.1:5000/` when started with `flask run` (or `http://127.0.0.1:5001/` if run directly with `python app.py`, since port 5001 is used there to avoid a conflict with macOS AirPlay Receiver). 

## Project Structure 

NASA Natural Events Tracker/
    app.py
    models.py
    templates/
        base.html
        browse.html
        event_detail.html
    requirements.txt
    .gitignore
    README.md

## OOP Design

`NaturalEvent` represents a single event fetched from the EONET API, storing its title, category, status, coordinates, date, and source. 
It has the methods `is_active` to simply check the status via boolean and `summery` to return a single line description combining category, title and status. The event's ID is stored as a private attribute and exposed through a read-only property, so that some other code does not overwrote it after creation as well as python itself blocking that kind of accidently mistake at the moment it happens.

`WatchedEvent` inherits from `NaturalEvent` using `super().__init__()`, 
adding a personal note and an alert flag. Its `toggle_alert()` method 
which turns the boolean and retuen the new value.

`EventFetcher` is the only class that calls the `requests` library so that Flask routes never call it directly. It provides `fetch_events()` to to return a list of `NaturalEvent` objects and `fetch_event()` to return one `NaturalEvent`.

## Known Limitations

- Groups C, D, and E are not implemented in this project. This 
  was an intentional scope reduction to focus on Groups A, B, and F.
- Group C (Watch List CRUD): there is no personal watch list, users cannot save, remove, or add notes to events.
- Group D (Search, Filter, and Sort) and Group E (Statistics) both 
  depend on a saved watch list existing, so without Group C, there 
  is nothing to filter, sort, or calculate statistics about.
- `WatchedEvent` exists in `models.py` as a class (satisfying the 
  OOP requirement) but isn't used by any route, since there's no 
  watch list feature for it to support.

## AI Assistance Disclosure

Parts of this project were developed with AI assistance (Claude), used to explain concepts, review code, and help debug issues. 
I reviewed and understood all code in this submission and can explain any part of it during the viva.




