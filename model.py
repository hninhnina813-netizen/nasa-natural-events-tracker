import requests


class NaturalEvent:
    def __init__(self,eonet_id, title, category, status, latitude, longitude, event_date, magnitude, mag_unit, source_url):
        self.__eonet_id = eonet_id
        self.title = title
        self.category = category
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.event_date = event_date
        self.magnitude = magnitude
        self.mag_unit = mag_unit
        self.source_url = source_url

    def is_active(self):
        return self.status == "open" #open if true and otherwise close

    def summary(self):
        return f"[{self.category}] {self.title} ({self.status})"

    @property 
    def eonet_id(self):
        return self.__eonet_id
    
class WatchedEvent(NaturalEvent):
    def __init__(self, eonet_id, title, category, status, latitude, longitude, event_date, magnitude, mag_unit, source_url, note="", alert_active=False):

        super().__init__(eonet_id, title, category, status, latitude, longitude, event_date, magnitude, mag_unit, source_url)

        self.note = note
        self.alert_active = alert_active

    def is_alert_active(self):
        return self.alert_active

    def toggle_alert(self):
        self.alert_active = not self.alert_active
        return self.alert_active

    def summary(self):
        text = super().summary()
        if self.note:
            text += f" - Note: {self.note}"

        text += f" | Alert:{'Active' if self.alert_active else 'Inactive'}"

        return text

class EventFetcher:

    BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"

    def _create_event(self, event_data):
        geometry = event_data.get("geometry", [])

        latitude = None
        longitude = None
        magnitude = None
        mag_unit = None
        event_date = None

        if geometry:
            latest_geometry = geometry[0]
            magnitude = latest_geometry.get("magnitudeValue")
            mag_unit = latest_geometry.get("magnitudeUnit")
            event_date = latest_geometry.get("date")
            coordinates = latest_geometry.get("coordinates")

            if coordinates and len(coordinates) >= 2:
                longitude = coordinates[0]
                latitude = coordinates[1]

        categories = event_data.get("categories", [])

        category = None

        if categories:
            category = categories[0].get("title")

        status = "closed" if event_data.get("closed") else "open"

        sources = event_data.get("sources", [])

        source_url = None

        if sources:
            source_url = sources[0].get("url")

        return NaturalEvent(
            eonet_id=event_data.get("id"),
            title=event_data.get("title"),
            category=category,
            status=status,
            latitude=latitude,
            longitude=longitude,
            event_date=event_date,
            magnitude=magnitude,
            mag_unit=mag_unit,
            source_url=source_url
        )

    def fetch_events(self, status="open", category=None, days=30, limit=50):
        params = {
            "status": status,
            "days": days,
            "limit": limit
        }

        if category:
            params["category"] = category

        response = requests.get(
            f"{self.BASE_URL}/events",
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        events = []

        for event_data in data.get("events", []):
            event = self._create_event(event_data)
            events.append(event)

        return events

    def fetch_event(self, eonet_id):
        response = requests.get(
            f"{self.BASE_URL}/events/{eonet_id}",
            timeout=10
        )

        response.raise_for_status()

        event_data = response.json()

        return self._create_event(event_data)

if __name__ == "__main__":
    event = NaturalEvent(
        eonet_id="EONET_12345",
        title="Wildfire in California",
        category="Wildfire",
        status="open",
        latitude=36.7783,
        longitude=-119.4179,
        event_date="2023-08-15",
        magnitude=5.0,
        mag_unit="Richter",
        source_url="https://example.com/wildfire"
    )
    print(event.summary())
    print("Is the event active?", event.is_active())

    print("\n--- WatchedEvent Example ---\n")
    watch_event = WatchedEvent(
        "EONET_12345", "Wildfire in California", "Wildfire", "open",
        36.7783, -119.4179, "2023-08-15", 5.0, "Richter",
        "https://example.com/wildfire",
        note="This is a critical event.", alert_active=True
    )
    print(watch_event.summary())
    print("Toggling alert...")
    watch_event.toggle_alert()
    print(watch_event.summary())

    print("\n--- EventFetcher Example ---\n")
    fetcher = EventFetcher()
    events = fetcher.fetch_events(status="open", category=None, days=30, limit=5)
    print(f"Number of events: {len(events)}")
    for e in events:
        print(e.summary())
        print(f"Location: ({e.longitude}, {e.latitude})")
        print(f"Magnitude: {e.magnitude} {e.mag_unit}")
        print("---")