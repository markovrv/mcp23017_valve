import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_I2C_ADDRESS, DEFAULT_RELAY_OPEN_TIME

class MCP23017ValveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="MCP23017 Valves", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("i2c_address", default=DEFAULT_I2C_ADDRESS): int,
                vol.Required("relay_open_time", default=DEFAULT_RELAY_OPEN_TIME): int,
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MCP23017ValveOptionsFlow(config_entry)

class MCP23017ValveOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "valves",
                    default=self.config_entry.options.get("valves", []),
                ): vol.All(
                    cv.ensure_list,
                    [
                        {
                            vol.Required("name"): str,
                            vol.Required("open_relay"): int,
                            vol.Required("close_relay"): int,
                        }
                    ],
                ),
            }),
        )