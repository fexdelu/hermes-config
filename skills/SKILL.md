# Skill: Clima

## Descripción
Proporciona información del clima usando OpenWeatherMap API.

## Trigger
El usuario pide el clima de una ciudad con "/clima [ciudad]".

## Acción
1. Obtener la ciudad del mensaje
2. Llamar a OpenWeatherMap API con la ciudad
3. Formatear la respuesta en español
4. Devolver temperatura, sensación térmica, humedad, descripción y viento

## API
- Endpoint: https://api.openweathermap.org/data/2.5/weather
- Parámetros: q={ciudad}, appid={API_KEY}, units=metric
- API Key: e574fbca70dc23400aafb07f4fb263a8

## Respuesta formato
🌤️ Clima para {ciudad}:
• Temperatura: {temp}°C
• Sensación térmica: {feels_like}°C
• Humedad: {humidity}%
• Descripción: {description}
• Viento: {wind} m/s