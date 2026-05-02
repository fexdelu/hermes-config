"""clima plugin — /clima slash command for weather lookups in Spanish."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)

_API_KEY: str = ""
_ALLOWED_USER_ID: str = "7494833586"


def _get_api_key() -> str:
    """Resolve the OpenWeatherMap API key from env or .env file."""
    global _API_KEY
    if _API_KEY:
        return _API_KEY
    key = os.getenv("WEATHER_API_KEY") or os.getenv("OPENWEATHERMAP_API_KEY", "")
    if key:
        _API_KEY = key
    return _API_KEY


def _fetch_weather(city: str) -> dict[str, Any]:
    """Call OpenWeatherMap API synchronously (used from sync handler)."""
    api_key = _get_api_key()
    if not api_key:
        return {"error": "WEATHER_API_KEY not configured. Add it to ~/.hermes/.env"}

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric&lang=es"
    )
    try:
        req = Request(url, headers={"User-Agent": "Hermes-clima/1.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 404:
            return {"error": f"Ciudad '{city}' no encontrada."}
        if e.code == 401:
            return {"error": "API key inválida. Verifica WEATHER_API_KEY en ~/.hermes/.env"}
        return {"error": f"Error HTTP {e.code}: {e.reason}"}
    except URLError as e:
        return {"error": f"Error de conexión: {e.reason}"}
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}


def _format_weather(data: dict[str, Any]) -> str:
    """Format OpenWeatherMap response into a Spanish weather report."""
    if "error" in data:
        return f"❌ {data['error']}"

    try:
        name = data["name"]
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]

        temp = main["temp"]
        feels_like = main["feels_like"]
        humidity = main["humidity"]
        description = weather["description"].capitalize()
        wind_speed = wind["speed"]

        return (
            f"🌤️ Clima para {name}:\n"
            f"• Temperatura: {temp}°C\n"
            f"• Sensación térmica: {feels_like}°C\n"
            f"• Humedad: {humidity}%\n"
            f"• Descripción: {description}\n"
            f"• Viento: {wind_speed} m/s"
        )
    except (KeyError, IndexError) as e:
        return f"❌ Error procesando datos del clima: {e}"


def _handle_clima(raw_args: str) -> Optional[str]:
    """Handle /clima slash command.

    Args:
        raw_args: The text after /clima, e.g. "Buenos Aires"

    Returns:
        Formatted weather string or error message.
    """
    city = raw_args.strip()
    if not city:
        return "Uso: /clima <ciudad>\nEjemplo: /clima Buenos Aires"

    data = _fetch_weather(city)
    return _format_weather(data)


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    """Register the /clima slash command with the Hermes plugin system."""
    # Pre-load API key so it's available at registration time
    _get_api_key()

    ctx.register_command(
        "clima",
        handler=_handle_clima,
        description="Obtener el clima de una ciudad (en español)",
        args_hint="<ciudad>",
    )
    logger.info("clima plugin registered — /clima command available")