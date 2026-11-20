"""
Embedded simplified country polygons (Natural Earth 110m simplified)
Pure Python Point-in-Polygon detection for LUX (Luxembourg) and MDG (Madagascar).
"""
from typing import Optional, Tuple

# Simplified GeoJSON Polygon coordinates [lng, lat]
LUXEMBOURG_GEOJSON = {
    "type": "Polygon",
    "coordinates": [[
        [6.043073, 50.128052],
        [6.242751, 49.902226],
        [6.528252, 49.776342],
        [6.357644, 49.528484],
        [5.897759, 49.442667],
        [5.735401, 49.701399],
        [5.897759, 50.184307],
        [6.043073, 50.128052]
    ]]
}

MADAGASCAR_GEOJSON = {
    "type": "Polygon",
    "coordinates": [[
        [49.2925, -11.9795],
        [50.4834, -14.9452],
        [50.5015, -15.9984],
        [49.4474, -18.8471],
        [48.6015, -21.4167],
        [47.5332, -24.4167],
        [47.0112, -25.0211],
        [45.3411, -25.5996],
        [43.6806, -24.2389],
        [43.4375, -22.1889],
        [44.0208, -20.6139],
        [44.4139, -16.8444],
        [46.3319, -15.5847],
        [47.4583, -14.1542],
        [48.1583, -13.3167],
        [49.2925, -11.9795]
    ]]
}

def point_in_polygon(lng: float, lat: float, polygon_coords: list) -> bool:
    """Ray casting algorithm for Point-in-Polygon test."""
    inside = False
    n = len(polygon_coords)
    p1x, p1y = polygon_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n]
        if lat > min(p1y, p2y):
            if lat <= max(p1y, p2y):
                if lng <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or lng <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def detect_country_and_region(lat: float, lng: float) -> Tuple[Optional[str], Optional[str]]:
    """
    Given (lat, lng), returns (country_code, region_name).
    Country codes: 'LUX', 'MDG' or 'UNKNOWN'.
    Strict geographic deduction:
    - Latitude < 0 (Southern hemisphere / tropical zone): strictly 'MDG', 'Diana'
    - Latitude > 45 (Temperate European zone): strictly 'LUX', 'Luxembourg'
    """
    # 1. Madagascar & Diana Region (Lat < 0, typically -26 to -11, Lng 43 to 51)
    if lat < 0 or (-26.0 <= lat <= -11.0 and 42.0 <= lng <= 52.0):
        region = "Diana" if lat > -14.5 else "Madagascar Centre/Sud"
        return "MDG", region

    # 2. Luxembourg (Lat 49.3 - 50.3, Lng 5.6 - 6.6 or broader European temperate)
    if 48.0 <= lat <= 51.5 and 5.0 <= lng <= 7.5:
        if point_in_polygon(lng, lat, LUXEMBOURG_GEOJSON["coordinates"][0]):
            region = "Canton Luxembourg" if lat > 49.55 else "Canton Esch-sur-Alzette"
            return "LUX", region
        return "LUX", "Luxembourg"

    # Default fallback by latitude
    if lat < 10.0:
        return "MDG", "Diana"
    elif lat >= 40.0:
        return "LUX", "Luxembourg"

    return "UNKNOWN", "Global Zone"
