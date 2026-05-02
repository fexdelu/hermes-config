# Hermes Agent Configuration

Configuración personal de Hermes Agent incluyendo plugins, skills y dotfiles.

## Estructura

```
hermes-config/
├── plugins/          # Plugins de Hermes (如/clima)
│   └── clima/        # Plugin de clima con OpenWeatherMap
├── skills/           # Skills en .md para el LLM
│   └── clima/        # Skill de clima (documentación)
├── config/           # Configuraciones
│   ├── config.yaml.sample
│   └── config.yaml.example
├── SOUL.md           # Personalidad de Hermes (español, "Papurri")
└── .env.example      # Variables de entorno (sin valores reales)
```

## instalacion

```bash
# Clonar en nueva máquina
git clone https://github.com/fexdelu/hermes-config.git ~/.hermes-config

# Copiar archivos a su ubicación
cp ~/.hermes-config/SOUL.md ~/.hermes/
cp -r ~/.hermes-config/plugins/* ~/.hermes/plugins/
cp -r ~/.hermes-config/skills/* ~/.hermes/skills/

# Configurar .env
cp ~/.hermes-config/.env.example ~/.hermes/.env
# Editar ~/.hermes/.env con tus API keys reales

# Reiniciar Hermes
systemctl --user restart hermes-gateway
```

## Plugins

### clima
Plugin que provee el comando `/clima` para consultar el clima via OpenWeatherMap.

**Variables de entorno requeridas:**
- `WEATHER_API_KEY` - API key de OpenWeatherMap

**Uso:**
```
/clima Buenos Aires
/clima Milano
```

## Notas

- NO commitear `.env` - contiene API keys reales
- La base de datos `state.db` no se incluiye
- Sessions y logs no se incluyen
