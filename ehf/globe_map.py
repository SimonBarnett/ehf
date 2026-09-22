"""Static Earth map (Leaflet + OpenStreetMap) — no API keys."""

from __future__ import annotations

import html
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ehf.game import Campaign


def _marker_payload(campaign: Campaign) -> list[dict]:
    from ehf.theatres import is_theatre_unlocked

    markers: list[dict] = []
    deployed_ids = {d.theatre_id for d in campaign.deployments}
    for theatre in campaign.globe_theatres:
        status = "deployed" if theatre.id in deployed_ids else (
            "unlocked" if is_theatre_unlocked(theatre, campaign) else "locked"
        )
        markers.append(
            {
                "id": theatre.id,
                "name": theatre.name,
                "lat": theatre.latitude,
                "lon": theatre.longitude,
                "tier": theatre.difficulty_tier,
                "region": theatre.region,
                "status": status,
            }
        )
    for town, assets in _town_assets(campaign):
        if not assets:
            continue
        markers.append(
            {
                "id": f"assets_{town}",
                "name": f"{town} assets",
                "lat": assets[0].latitude,
                "lon": assets[0].longitude,
                "tier": 0,
                "region": "asset",
                "status": "base",
            }
        )
    return markers


def _town_assets(campaign: Campaign):
    for town in campaign.world.towns:
        assets = campaign.world.towns[town]["assets"]
        if assets:
            yield town.value, assets


def render_globe_html(campaign: Campaign, title: str = "EHF globe — god-mode deploy") -> str:
    markers_json = json.dumps(_marker_payload(campaign))
    deployments_json = json.dumps(
        [
            {
                "theatre": d.theatre_name,
                "kind": d.kind,
                "count": d.count,
                "day": d.day,
                "lat": d.latitude,
                "lon": d.longitude,
                "tier": d.difficulty_tier,
            }
            for d in campaign.deployments
        ]
    )
    safe_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{safe_title}</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body, #map {{ height: 100%; margin: 0; }}
    #panel {{
      position: absolute; top: 10px; right: 10px; z-index: 1000;
      background: rgba(255,255,255,0.92); padding: 10px 12px; max-width: 320px;
      font: 13px/1.4 system-ui, sans-serif; border-radius: 6px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }}
    .tier-1 {{ filter: hue-rotate(90deg); }}
    .tier-high {{ filter: hue-rotate(-30deg); }}
  </style>
</head>
<body>
  <div id="panel">
    <strong>EHF globe</strong> (Leaflet / OpenStreetMap)<br/>
    God-mode deployments into escalating theatres.<br/>
    <span id="deploy-summary"></span>
  </div>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const markers = {markers_json};
    const deployments = {deployments_json};
    const map = L.map('map').setView([20, 10], 2);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
    const colors = {{
      base: '#2563eb',
      unlocked: '#16a34a',
      locked: '#9ca3af',
      deployed: '#dc2626',
    }};
    for (const m of markers) {{
      const c = colors[m.status] || '#333';
      L.circleMarker([m.lat, m.lon], {{
        radius: m.tier >= 2 ? 8 : 5,
        color: c,
        fillColor: c,
        fillOpacity: 0.85,
        weight: 1,
      }}).bindPopup(
        `<b>${{m.name}}</b><br/>tier ${{m.tier}} · ${{m.status}}<br/>${{m.lat}}, ${{m.lon}}`
      ).addTo(map);
    }}
    for (const d of deployments) {{
      L.marker([d.lat, d.lon]).bindPopup(
        `<b>Deploy: ${{d.theatre}}</b><br/>${{d.kind}} × ${{d.count}}<br/>${{d.day}}`
      ).addTo(map);
    }}
    document.getElementById('deploy-summary').textContent =
      deployments.length
        ? deployments.length + ' deployment(s) on map'
        : 'No deployments yet — UK training first, then README theatres.';
  </script>
</body>
</html>
"""
