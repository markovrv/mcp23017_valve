import logging
import smbus2
import time
import os
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN, DEFAULT_I2C_ADDRESS, DEFAULT_RELAY_OPEN_TIME

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the valve switches."""
    # Проверка доступности I2C
    i2c_device = "/dev/i2c-1"
    if not os.path.exists(i2c_device):
        _LOGGER.error(f"I2C устройство {i2c_device} не найдено!")
        return False

    try:
        bus = smbus2.SMBus(1)
        bus.read_byte(DEFAULT_I2C_ADDRESS)  # Проверка связи
        bus.close()
    except Exception as e:
        _LOGGER.error(f"Ошибка доступа к I2C: {e}")
        return False

    # Создаём сущности с уникальными ID
    valves = config.get("valves", [])
    entities = []
    for valve in valves:
        # Генерация unique_id на основе имени и реле
        unique_id = f"mcp23017_valve_{valve['name'].lower().replace(' ', '_')}"
        
        entities.append(
            MCP23017Valve(
                valve["name"],
                unique_id,  # Передаём unique_id в класс
                valve["open_relay"],
                valve["close_relay"],
                config.get("i2c_address", DEFAULT_I2C_ADDRESS),
                config.get("relay_open_time", DEFAULT_RELAY_OPEN_TIME),
            )
        )

    async_add_entities(entities)
    return True

class MCP23017Valve(SwitchEntity):
    def __init__(self, name, unique_id, open_relay, close_relay, i2c_address, relay_open_time):
        self._name = name
        self._unique_id = unique_id  # Сохраняем unique_id
        self._open_relay = open_relay
        self._close_relay = close_relay
        self._i2c_address = i2c_address
        self._relay_open_time = relay_open_time
        self._state = False
        self._bus = None

        try:
            self._bus = smbus2.SMBus(1)
            self._bus.write_byte_data(self._i2c_address, 0x00, 0x00)  # PORT A как выходы
            self._bus.write_byte_data(self._i2c_address, 0x01, 0x00)  # PORT B как выходы
        except Exception as e:
            _LOGGER.error(f"Ошибка инициализации MCP23017: {e}")
            raise

    @property
    def unique_id(self):
        """Возвращает уникальный идентификатор."""
        return self._unique_id

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        try:
            port = 0x14 if self._open_relay <= 8 else 0x15
            relay_num = self._open_relay - 1 if self._open_relay <= 8 else self._open_relay - 9
            self._bus.write_byte_data(self._i2c_address, port, 1 << relay_num)
            time.sleep(self._relay_open_time)
            self._bus.write_byte_data(self._i2c_address, port, 0)
            self._state = True
        except Exception as e:
            _LOGGER.error(f"Ошибка открытия крана: {e}")
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        try:
            port = 0x14 if self._close_relay <= 8 else 0x15
            relay_num = self._close_relay - 1 if self._close_relay <= 8 else self._close_relay - 9
            self._bus.write_byte_data(self._i2c_address, port, 1 << relay_num)
            time.sleep(self._relay_open_time)
            self._bus.write_byte_data(self._i2c_address, port, 0)
            self._state = False
        except Exception as e:
            _LOGGER.error(f"Ошибка закрытия крана: {e}")
        self.schedule_update_ha_state()