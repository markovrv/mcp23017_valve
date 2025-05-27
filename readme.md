# MCP23017 Water Valve Control for Home Assistant

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.12-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![License](https://img.shields.io/github/license/markovrv/mcp23017_valve)

Custom Home Assistant integration for controlling water valves via MCP23017 I2C relay module. Perfect for smart home irrigation systems or water control automation.

## Features

- 🚰 Control up to 8 water valves (expandable to 16)
- ⏳ Configurable relay activation time (default 6 seconds)
- 🖥️ Web interface configuration (no YAML editing required)
- 🔄 Toggle-style switches for open/close operations
- 🔌 Automatic I2C bus detection
- 🏠 Seamless Home Assistant integration

## Installation

### Via HACS (Recommended)
1. Add this repository to HACS:
   - Go to **HACS → Integrations → Custom Repositories**
   - Add `https://github.com/markovrv/mcp23017_valve`
2. Install "MCP23017 Water Valve" integration
3. Restart Home Assistant

### Manual Installation
1. Clone this repository to your `custom_components` folder:
   ```bash
   cd /config/custom_components
   git clone https://github.com/markovrv/mcp23017_valve.git
   ```
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "MCP23017 Water Valve"
3. Enter configuration:
   - I2C Address (default: 0x20)
   - Relay Activation Time (default: 6 seconds)

### Adding Valves
After initial setup:
1. Click on the integration
2. Select "Options"
3. Add valves with:
   - Friendly name (e.g., "Garden Valve")
   - Open Relay Number (1-16)
   - Close Relay Number (1-16)

## Hardware Setup

### Required Components
- Raspberry Pi (any model with I2C)
- MCP23017 I2C Port Expander
- 16-Channel Relay Module
- 3.3V to 5V Logic Level Converter (if needed)
- Water Solenoid Valves

### Wiring Diagram
```
RPi 3.3V → MCP23017 VCC
RPi GND → MCP23017 GND
RPi SDA → MCP23017 SDA
RPi SCL → MCP23017 SCL

MCP23017 GPA0-GPA7 → Relay Module IN1-IN8
MCP23017 GPB0-GPB7 → Relay Module IN9-IN16
```

## Usage

After installation:
- New switches will appear in Home Assistant
- Each switch toggles between open/close states
- Valve state is maintained in Home Assistant

## Example Automations

```yaml

switch:
  - platform: mcp23017_valve
    i2c_address: 0x20
    relay_open_time: 6
    valves:
      - name: "Кран 1"
        open_relay: 1
        close_relay: 8


automation:
  - alias: "Close all valves at night"
    trigger:
      platform: time
      at: "23:00:00"
    action:
      service: switch.turn_off
      target:
        entity_id:
          - switch.garden_valve
          - switch.kitchen_valve

  - alias: "Notify if valve left open"
    trigger:
      platform: state
      entity_id: switch.garden_valve
      to: "on"
      for:
        hours: 2
    action:
      service: notify.mobile_app_phone
      data:
        message: "Garden valve has been open for 2 hours!"
```

## Troubleshooting

### Common Issues
1. **I2C not detected**:
   - Enable I2C in `raspi-config`
   - Check wiring with `i2cdetect -y 1`

2. **Relays not activating**:
   - Verify power supply to relay module
   - Check MCP23017 address with `i2cdetect`

3. **Valve state not updating**:
   - Restart Home Assistant
   - Check logs for errors

### Checking Logs
Add to `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    custom_components.mcp23017_valve: debug
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

**Disclaimer**: Use at your own risk. Always install proper backflow prevention devices when working with water systems.