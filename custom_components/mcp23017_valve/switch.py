import logging
import smbus2
import time
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN, DEFAULT_RELAY_OPEN_TIME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    i2c_address = config_entry.data.get("i2c_address")
    relay_open_time = config_entry.data.get("relay_open_time", DEFAULT_RELAY_OPEN_TIME)
    valves = config_entry.options.get("valves", [])

    entities = []
    for valve in valves:
        entities.append(
            MCP23017Valve(
                hass,
                valve["name"],
                valve["open_relay"],
                valve["close_relay"],
                i2c_address,
                relay_open_time,
            )
        )

    async_add_entities(entities)

class MCP23017Valve(SwitchEntity):
    def __init__(self, hass, name, open_relay, close_relay, i2c_address, relay_open_time):
        self._hass = hass
        self._name = name
        self._open_relay = open_relay
        self._close_relay = close_relay
        self._i2c_address = i2c_address
        self._relay_open_time = relay_open_time
        self._state = False
        self._bus = smbus2.SMBus(1)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._bus.write_byte_data(self._i2c_address, 0x14, 1 << (self._open_relay - 1))
        time.sleep(self._relay_open_time)
        self._bus.write_byte_data(self._i2c_address, 0x14, 0)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self._bus.write_byte_data(self._i2c_address, 0x14, 1 << (self._close_relay - 1))
        time.sleep(self._relay_open_time)
        self._bus.write_byte_data(self._i2c_address, 0x14, 0)
        self._state = False
        self.schedule_update_ha_state()