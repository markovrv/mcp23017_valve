from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the MCP23017 valve component."""
    hass.async_create_task(
        discovery.async_load_platform(
            hass, 
            "switch", 
            DOMAIN, 
            {}, 
            config
        )
    )
    return True

async def async_setup_entry(hass, entry):
    """Set up from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True