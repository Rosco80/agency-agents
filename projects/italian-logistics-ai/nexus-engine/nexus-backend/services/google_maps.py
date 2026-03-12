import googlemaps
from config import settings

class GoogleMapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    def optimize_route(self, origin, destination, waypoints):
        """
        Calculates the optimal sequence for a set of waypoints.
        For Phase 1, we use the Directions API with optimize_waypoints=True.
        The Google Maps Route Optimization API (Fleet Routing) is more complex,
        so we start with this for the MVP to get to "Optimal Sequences" fast.
        """
        if not settings.GOOGLE_MAPS_API_KEY:
            return {"error": "API Key missing"}

        try:
            result = self.client.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                optimize_waypoints=True,
                mode="driving",
                region="it"
            )
            return result
        except Exception as e:
            return {"error": str(e)}

google_maps_service = GoogleMapsService()
