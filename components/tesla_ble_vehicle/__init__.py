import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client, binary_sensor, button, switch, number, sensor, text_sensor, lock, cover, climate, mqtt
from esphome.const import (
    CONF_ACCURACY_DECIMALS,
    CONF_DEVICE_CLASS,
    CONF_DISABLED_BY_DEFAULT,
    CONF_ENTITY_CATEGORY,
    CONF_FORCE_UPDATE,
    CONF_ICON,
    CONF_ID,
    CONF_INTERNAL,
    CONF_MODE,
    CONF_NAME,
    CONF_RESTORE_MODE,
    CONF_UNIT_OF_MEASUREMENT,
    ENTITY_CATEGORY_DIAGNOSTIC,
)
from esphome import automation


CODEOWNERS = ["@yoziru"]
DEPENDENCIES = ["ble_client"]
AUTO_LOAD = ["binary_sensor", "button", "switch", "number", "sensor", "text_sensor", "lock", "cover", "climate"]

tesla_ble_vehicle_ns = cg.esphome_ns.namespace("tesla_ble_vehicle")
TeslaBLEVehicle = tesla_ble_vehicle_ns.class_(
    "TeslaBLEVehicle", cg.PollingComponent, ble_client.BLEClientNode
)

# Custom button classes - generated via macro in C++, just reference here
# The class name follows pattern: Tesla{Id}Button where Id is PascalCase of id
TeslaWakeButton = tesla_ble_vehicle_ns.class_("TeslaWakeButton", button.Button)
TeslaPairButton = tesla_ble_vehicle_ns.class_("TeslaPairButton", button.Button)
TeslaRegenerateKeyButton = tesla_ble_vehicle_ns.class_("TeslaRegenerateKeyButton", button.Button)
TeslaForceUpdateButton = tesla_ble_vehicle_ns.class_("TeslaForceUpdateButton", button.Button)
TeslaFlashLightsButton = tesla_ble_vehicle_ns.class_("TeslaFlashLightsButton", button.Button)
TeslaHonkHornButton = tesla_ble_vehicle_ns.class_("TeslaHonkHornButton", button.Button)
TeslaUnlatchDriverDoorButton = tesla_ble_vehicle_ns.class_("TeslaUnlatchDriverDoorButton", button.Button)

# Custom switch classes - generated via macro in C++, just reference here
TeslaChargingSwitch = tesla_ble_vehicle_ns.class_("TeslaChargingSwitch", switch.Switch)
TeslaSteeringWheelHeatSwitch = tesla_ble_vehicle_ns.class_("TeslaSteeringWheelHeatSwitch", switch.Switch)
TeslaSentryModeSwitch = tesla_ble_vehicle_ns.class_("TeslaSentryModeSwitch", switch.Switch)

# Custom lock classes
TeslaDoorsLock = tesla_ble_vehicle_ns.class_("TeslaDoorsLock", lock.Lock)
TeslaChargePortLatchLock = tesla_ble_vehicle_ns.class_("TeslaChargePortLatchLock", lock.Lock)

# Custom cover classes
TeslaTrunkCover = tesla_ble_vehicle_ns.class_("TeslaTrunkCover", cover.Cover)
TeslaFrunkCover = tesla_ble_vehicle_ns.class_("TeslaFrunkCover", cover.Cover)
TeslaWindowsCover = tesla_ble_vehicle_ns.class_("TeslaWindowsCover", cover.Cover)
TeslaChargePortDoorCover = tesla_ble_vehicle_ns.class_("TeslaChargePortDoorCover", cover.Cover)

# Custom climate class
TeslaClimate = tesla_ble_vehicle_ns.class_("TeslaClimate", climate.Climate)

# Custom number classes
TeslaChargingAmpsNumber = tesla_ble_vehicle_ns.class_("TeslaChargingAmpsNumber", number.Number)
TeslaChargingLimitNumber = tesla_ble_vehicle_ns.class_("TeslaChargingLimitNumber", number.Number)

# Actions
WakeAction = tesla_ble_vehicle_ns.class_("WakeAction", automation.Action)
PairAction = tesla_ble_vehicle_ns.class_("PairAction", automation.Action)
RegenerateKeyAction = tesla_ble_vehicle_ns.class_("RegenerateKeyAction", automation.Action)
ForceUpdateAction = tesla_ble_vehicle_ns.class_("ForceUpdateAction", automation.Action)
SetChargingAction = tesla_ble_vehicle_ns.class_("SetChargingAction", automation.Action)
SetChargingAmpsAction = tesla_ble_vehicle_ns.class_("SetChargingAmpsAction", automation.Action)
SetChargingLimitAction = tesla_ble_vehicle_ns.class_("SetChargingLimitAction", automation.Action)

# Configuration constants
CONF_VIN = "vin"
CONF_CHARGING_AMPS_MAX = "charging_amps_max"
DEFAULT_CHARGING_AMPS_MAX = 32
CONF_ROLE = "role"

# Per-entity overrides, keyed by the entity "id" used in the lists below, e.g.:
#   tesla_ble_vehicle:
#     entities:
#       climate: { disabled: true }        # entity is not created at all
#       battery_level: { internal: true }  # created, hidden from UI/API/MQTT
#       doors: { name: "Front Doors" }      # rename without editing the lists
# This is what lets a fork/override keep customizations in YAML instead of
# editing the ENTITY DEFINITIONS below.
CONF_ENTITIES = "entities"
ENTITY_OVERRIDE_SCHEMA = cv.Schema(
    {
        cv.Optional("disabled", default=False): cv.boolean,
        cv.Optional("internal"): cv.boolean,
        cv.Optional("name"): cv.string,
    }
)

# Polling configuration constants
CONF_VCSEC_POLL_INTERVAL = "vcsec_poll_interval"
CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE = "infotainment_poll_interval_awake" 
CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE = "infotainment_poll_interval_active"
CONF_INFOTAINMENT_SLEEP_TIMEOUT = "infotainment_sleep_timeout"

# Tesla key roles
TESLA_ROLES = {
    "DRIVER": "Keys_Role_ROLE_DRIVER",
    "CHARGING_MANAGER": "Keys_Role_ROLE_CHARGING_MANAGER",
}

# =============================================================================
# ENTITY DEFINITIONS - Add new sensors/controls here!
# =============================================================================
# Just add to these lists - no C++ changes needed unless custom logic is required.
# The sensor ID must match the ID used in vehicle_state_manager.cpp update methods.
#
# Each definition is a dict with:
#   - id: unique identifier (must match C++ usage)
#   - name: display name
#   - icon: MDI icon (optional)
#   - device_class: ESPHome device class (optional)
#   - unit: unit of measurement (optional, for sensors/numbers)
#   - accuracy_decimals: number of decimals for display precision (optional, for sensors only)
#   - disabled_by_default: whether disabled by default (optional, default False)
#   - entity_category: entity category (optional, e.g. "diagnostic")
#
# For buttons/switches, also include:
#   - class: the C++ class reference (e.g. TeslaWakeButton)
#   - setter: setter method name if needed for special handling (optional)
#
# For numbers, also include:
#   - min: minimum value
#   - max: maximum value (or "config" to use config value like charging_amps_max)
#   - step: step size

BINARY_SENSORS = [
    # VCSEC sensors
    {"id": "asleep", "name": "Asleep", "icon": "mdi:sleep"},
    {"id": "user_present", "name": "User Present", "icon": "mdi:account-check", "device_class": "occupancy"},
    {"id": "charger", "name": "Charger", "icon": "mdi:power-plug", "device_class": "plug"},
    
    # Drive sensors
    {"id": "parking_brake", "name": "Parking Brake", "icon": "mdi:car-brake-parking"},
    
    # Individual closure sensors (disabled by default since covers/locks show aggregate state)
    {"id": "door_driver_front", "name": "Door Driver Front", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True},
    {"id": "door_driver_rear", "name": "Door Driver Rear", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True},
    {"id": "door_passenger_front", "name": "Door Passenger Front", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True},
    {"id": "door_passenger_rear", "name": "Door Passenger Rear", "icon": "mdi:car-door", "device_class": "door", "disabled_by_default": True},
    {"id": "window_driver_front", "name": "Window Driver Front", "icon": "mdi:car-door", "device_class": "window", "disabled_by_default": True},
    {"id": "window_driver_rear", "name": "Window Driver Rear", "icon": "mdi:car-door", "device_class": "window", "disabled_by_default": True},
    {"id": "window_passenger_front", "name": "Window Passenger Front", "icon": "mdi:car-door", "device_class": "window", "disabled_by_default": True},
    {"id": "window_passenger_rear", "name": "Window Passenger Rear", "icon": "mdi:car-door", "device_class": "window", "disabled_by_default": True},
    {"id": "sunroof", "name": "Sunroof", "icon": "mdi:car-select", "device_class": "window", "disabled_by_default": True},

]

SENSORS = [
    # Charge state sensors
    {"id": "battery_level", "name": "Battery", "icon": "mdi:battery", "unit": "%"},
    {"id": "range", "name": "Range", "icon": "mdi:map-marker-distance", "device_class": "distance", "unit": "mi"},
    {"id": "charger_power", "name": "Charger Power", "icon": "mdi:flash", "device_class": "power", "unit": "kW"},
    {"id": "charger_voltage", "name": "Charger Voltage", "icon": "mdi:lightning-bolt", "device_class": "voltage", "unit": "V"},
    {"id": "charger_current", "name": "Charger Current", "icon": "mdi:current-ac", "device_class": "current", "unit": "A"},
    {"id": "evse_max_current", "name": "Charger Max", "icon": "mdi:ev-plug-tesla", "device_class": "current", "unit": "A"},
    {"id": "charge_current_request", "name": "Requested Current", "icon": "mdi:current-ac", "device_class": "current", "unit": "A", "entity_category": "diagnostic", "disabled_by_default": True},
    {"id": "vehicle_max_charge_current", "name": "Car Max Acceptable", "icon": "mdi:car-battery", "device_class": "current", "unit": "A"},
    {"id": "charger_phases", "name": "Charger Phases", "icon": "mdi:sine-wave", "unit": "", "accuracy_decimals": 0},
    {"id": "charger_power_estimated", "name": "Charger Power Estimated", "icon": "mdi:flash", "device_class": "power", "unit": "kW", "accuracy_decimals": 2},
    {"id": "charging_rate", "name": "Charging Rate", "icon": "mdi:speedometer", "device_class": "speed", "unit": "mph", "accuracy_decimals": 1},
    {"id": "energy_added", "name": "Energy Added", "icon": "mdi:battery-charging", "device_class": "energy", "unit": "kWh", "accuracy_decimals": 1},
    {"id": "time_to_full", "name": "Time to Full", "icon": "mdi:clock-outline", "device_class": "duration", "unit": "min"},
    
    # Climate state sensors
    {"id": "outside_temp", "name": "Outside Temperature", "icon": "mdi:thermometer", "device_class": "temperature", "unit": "°C", "accuracy_decimals": 1},
    
    # Drive state sensors
    {"id": "odometer", "name": "Odometer", "icon": "mdi:counter", "device_class": "distance", "unit": "mi", "disabled_by_default": True},
    
    # Tire pressure sensors
    {"id": "tpms_front_left", "name": "TPMS Front Left", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1},
    {"id": "tpms_front_right", "name": "TPMS Front Right", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1},
    {"id": "tpms_rear_left", "name": "TPMS Rear Left", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1},
    {"id": "tpms_rear_right", "name": "TPMS Rear Right", "icon": "mdi:car-tire-alert", "device_class": "pressure", "unit": "bar", "accuracy_decimals": 1},
]

TEXT_SENSORS = [
    {"id": "charging_state", "name": "Charging", "icon": "mdi:ev-station"},
    {"id": "iec61851_state", "name": "IEC 61851", "icon": "mdi:ev-plug-type2", "disabled_by_default": True},
    {"id": "shift_state", "name": "Shift State", "icon": "mdi:car-shift-pattern", "disabled_by_default": True},
    {"id": "charge_limit_reason", "name": "Charge Limit Reason", "icon": "mdi:ev-plug-tesla"},
    {"id": "last_command", "name": "Last Command", "icon": "mdi:history", "entity_category": "diagnostic", "disabled_by_default": True, "setter": "set_last_command_text_sensor"},
]

BUTTONS = [
    {"id": "wake", "name": "Wake up", "class": TeslaWakeButton, "setter": "set_wake_button", "icon": "mdi:sleep-off"},
    {"id": "pair", "name": "Pair BLE Key", "class": TeslaPairButton, "setter": "set_pair_button", "icon": "mdi:key-wireless", "entity_category": "diagnostic"},
    {"id": "regenerate_key", "name": "Regenerate key", "class": TeslaRegenerateKeyButton, "setter": "set_regenerate_key_button", "icon": "mdi:key-change", "entity_category": "diagnostic", "disabled_by_default": True},
    {"id": "force_update", "name": "Force data update", "class": TeslaForceUpdateButton, "setter": "set_force_update_button", "icon": "mdi:database-sync", "entity_category": "diagnostic"},
    # Unique actions (not part of combined entities)
    {"id": "unlatch_driver_door", "name": "Unlatch Driver Door", "class": TeslaUnlatchDriverDoorButton, "setter": None, "icon": "mdi:car-door", "disabled_by_default": True},
    # Vehicle controls
    {"id": "flash_lights", "name": "Flash Lights", "class": TeslaFlashLightsButton, "setter": None, "icon": "mdi:car-light-high"},
    {"id": "honk_horn", "name": "Sound Horn", "class": TeslaHonkHornButton, "setter": None, "icon": "mdi:bullhorn"},
]

SWITCHES = [
    {"id": "charging", "name": "Charger", "class": TeslaChargingSwitch, "setter": "set_charging_switch", "icon": "mdi:ev-station"},
    {"id": "steering_wheel_heat", "name": "Heated Steering", "class": TeslaSteeringWheelHeatSwitch, "setter": "set_steering_wheel_heat_switch", "icon": "mdi:steering"},
    {"id": "sentry_mode", "name": "Sentry Mode", "class": TeslaSentryModeSwitch, "setter": "set_sentry_mode_switch", "icon": "mdi:shield-car"},
]

# Lock entities (combined sensor + control)
LOCKS = [
    {"id": "doors", "name": "Doors", "class": TeslaDoorsLock, "setter": "set_doors_lock", "icon": "mdi:car-door-lock"},
    {"id": "charge_port_latch", "name": "Charge Port Latch", "class": TeslaChargePortLatchLock, "setter": "set_charge_port_latch_lock", "icon": "mdi:ev-plug-tesla"},
]

# Cover entities (combined sensor + control)
COVERS = [
    {"id": "trunk", "name": "Trunk", "class": TeslaTrunkCover, "setter": "set_trunk_cover", "icon": "mdi:car-back", "device_class": "door"},
    {"id": "frunk", "name": "Frunk", "class": TeslaFrunkCover, "setter": "set_frunk_cover", "icon": "mdi:car", "device_class": "door"},
    {"id": "windows", "name": "Windows", "class": TeslaWindowsCover, "setter": "set_windows_cover", "icon": "mdi:car-door", "device_class": "awning"},
    {"id": "charge_port_door", "name": "Charge Port Door", "class": TeslaChargePortDoorCover, "setter": "set_charge_port_door_cover", "icon": "mdi:ev-plug-tesla", "device_class": "door"},
]

# Climate entity
CLIMATE = {
    "id": "climate",
    "name": "Climate",
    "class": TeslaClimate,
    "setter": "set_climate",
}

NUMBERS = [
    {
        "id": "charging_amps",
        "name": "Charging Amps",
        "class": TeslaChargingAmpsNumber,
        "setter": "set_charging_amps_number",
        "icon": "mdi:current-ac",
        "unit": "A",
        "min": 0,
        "max": "config",  # Will use charging_amps_max from config
        "step": 1,
    },
    {
        "id": "charging_limit",
        "name": "Charging Limit",
        "class": TeslaChargingLimitNumber,
        "setter": "set_charging_limit_number",
        "icon": "mdi:battery-charging-100",
        "unit": "%",
        "min": 50,
        "max": 100,
        "step": 1,
    },
]

# =============================================================================
# MQTT WIRING
# =============================================================================
#
# All entities above are built from plain dicts instead of being run through
# each platform's own cv.Schema (e.g. sensor.sensor_schema()). That schema is
# where ESPHome normally injects a `cv.OnlyWith(CONF_MQTT_ID, "mqtt")` default
# that drives automatic MQTT publishing - skipping it means these entities
# are otherwise invisible to MQTT even with `mqtt:` enabled (they still show
# up fine over the native API, since that doesn't go through the same path).
#
# ESPHome also requires every Component id to have been seen during the
# initial config-validation ID sweep (esphome/config.py's IDPassValidationStep)
# before it can be registered as a component in to_code() - ids invented only
# at codegen time fail with "Component ID ... was not declared to inherit
# from Component". So each entity gets its own `cv.OnlyWith(..., "mqtt")` key
# added to CONFIG_SCHEMA below (present only when `mqtt:` is loaded), exactly
# mirroring what each platform's own schema does for its own entities.

def _object_id(definition, suffix):
    return f"tesla_{definition['id']}_{suffix}"


def _mqtt_config_key(definition, suffix):
    return f"{_object_id(definition, suffix)}_mqtt_id"


# Maps our entity "suffix" (see _object_id) to the matching ESPHome MQTT
# wrapper class.
_MQTT_COMPONENT_CLASSES = {
    "sensor": mqtt.MQTTSensorComponent,
    "binary_sensor": mqtt.MQTTBinarySensorComponent,
    "text_sensor": mqtt.MQTTTextSensor,
    "button": mqtt.MQTTButtonComponent,
    "switch": mqtt.MQTTSwitchComponent,
    "lock": mqtt.MQTTLockComponent,
    "cover": mqtt.MQTTCoverComponent,
    "climate": mqtt.MQTTClimateComponent,
    "number": mqtt.MQTTNumberComponent,
}


def _entity_specs():
    """Yield (definition, suffix, mqtt_kind) for every entity this component creates."""
    for definition in BINARY_SENSORS:
        yield definition, "sensor", "binary_sensor"
    for definition in SENSORS:
        yield definition, "sensor", "sensor"
    for definition in TEXT_SENSORS:
        yield definition, "sensor", "text_sensor"
    for definition in BUTTONS:
        yield definition, "button", "button"
    for definition in SWITCHES:
        yield definition, "switch", "switch"
    for definition in LOCKS:
        yield definition, "lock", "lock"
    for definition in COVERS:
        yield definition, "cover", "cover"
    for definition in NUMBERS:
        yield definition, "number", "number"
    yield CLIMATE, "climate", "climate"


_MQTT_ID_SCHEMA = {
    cv.OnlyWith(_mqtt_config_key(definition, suffix), "mqtt"): cv.declare_id(
        _MQTT_COMPONENT_CLASSES[mqtt_kind]
    )
    for definition, suffix, mqtt_kind in _entity_specs()
}


async def _register_mqtt(top_config, entity, definition, suffix):
    """Publish an entity via MQTT, using the id pre-declared in CONFIG_SCHEMA."""
    mqtt_id = top_config.get(_mqtt_config_key(definition, suffix))
    if mqtt_id is None:
        return
    mqtt_var = cg.new_Pvariable(mqtt_id, entity)
    await mqtt.register_mqtt_component(mqtt_var, {})


# =============================================================================
# CONFIG SCHEMA
# =============================================================================

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(TeslaBLEVehicle),
            cv.Required(CONF_VIN): cv.string,
            cv.Optional(CONF_CHARGING_AMPS_MAX, default=DEFAULT_CHARGING_AMPS_MAX): cv.int_range(min=1, max=48),
            cv.Optional(CONF_ROLE, default="DRIVER"): cv.enum(TESLA_ROLES, upper=True),
            # Polling intervals (in seconds)
            cv.Optional(CONF_VCSEC_POLL_INTERVAL, default=10): cv.int_range(min=5, max=300),
            cv.Optional(CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE, default=30): cv.int_range(min=10, max=600), 
            cv.Optional(CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE, default=10): cv.int_range(min=5, max=120),
            cv.Optional(CONF_INFOTAINMENT_SLEEP_TIMEOUT, default=660): cv.int_range(min=60, max=3600),
            cv.Optional(CONF_ENTITIES, default={}): cv.Schema(
                {cv.string: ENTITY_OVERRIDE_SCHEMA}
            ),
            **_MQTT_ID_SCHEMA,
        },
    )
    .extend(cv.polling_component_schema("10s"))
    .extend(ble_client.BLE_CLIENT_SCHEMA)
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_device_class_const(component_module, device_class_str):
    """Convert device class string to the actual constant."""
    if device_class_str is None:
        return None
    return getattr(component_module, f"DEVICE_CLASS_{device_class_str.upper()}", None)


def _base_config(definition, id_type, suffix, overrides=None):
    overrides = overrides or {}
    config = {
        CONF_ID: cv.declare_id(id_type)(_object_id(definition, suffix)),
        CONF_NAME: overrides.get("name", definition["name"]),
        CONF_DISABLED_BY_DEFAULT: definition.get("disabled_by_default", False),
    }
    if "icon" in definition:
        config[CONF_ICON] = definition["icon"]
    if definition.get("entity_category") == "diagnostic":
        config[CONF_ENTITY_CATEGORY] = ENTITY_CATEGORY_DIAGNOSTIC
    if "internal" in overrides:
        config[CONF_INTERNAL] = overrides["internal"]
    return config


def _with_device_class(config, module, definition):
    if "device_class" in definition:
        dc = get_device_class_const(module, definition["device_class"])
        if dc:
            config[CONF_DEVICE_CLASS] = dc
    return config


async def _attach(var, entity, definition, top_config, mqtt_kind, suffix):
    cg.add(entity.set_parent(var))
    if definition.get("setter"):
        cg.add(getattr(var, definition["setter"])(entity))
    await _register_mqtt(top_config, entity, definition, suffix)
    return entity


async def create_binary_sensor(var, definition, top_config, overrides=None):
    """Create a binary sensor and register with TeslaBLEVehicle using generic setter."""
    config = _with_device_class(
        _base_config(definition, binary_sensor.BinarySensor, "sensor", overrides),
        binary_sensor, definition)
    sens = await binary_sensor.new_binary_sensor(config)
    cg.add(var.set_binary_sensor(definition["id"], sens))
    await _register_mqtt(top_config, sens, definition, "sensor")
    return sens


async def create_sensor(var, definition, top_config, overrides=None):
    """Create a sensor and register with TeslaBLEVehicle using generic setter."""
    config = _base_config(definition, sensor.Sensor, "sensor", overrides)
    config[CONF_FORCE_UPDATE] = False
    if "unit" in definition:
        config[CONF_UNIT_OF_MEASUREMENT] = definition["unit"]
    if "accuracy_decimals" in definition:
        config[CONF_ACCURACY_DECIMALS] = definition["accuracy_decimals"]
    config = _with_device_class(config, sensor, definition)
    sens = await sensor.new_sensor(config)
    cg.add(var.set_sensor(definition["id"], sens))
    await _register_mqtt(top_config, sens, definition, "sensor")
    return sens


async def create_text_sensor(var, definition, top_config, overrides=None):
    """Create a text sensor and register with TeslaBLEVehicle using generic setter."""
    config = _base_config(definition, text_sensor.TextSensor, "sensor", overrides)
    config[CONF_FORCE_UPDATE] = False
    sens = await text_sensor.new_text_sensor(config)
    if definition.get("setter"):
        cg.add(getattr(var, definition["setter"])(sens))
    else:
        cg.add(var.set_text_sensor(definition["id"], sens))
    await _register_mqtt(top_config, sens, definition, "sensor")
    return sens


async def create_button(var, definition, top_config, overrides=None):
    """Create a button and register with TeslaBLEVehicle."""
    btn = await button.new_button(
        _base_config(definition, definition["class"], "button", overrides))
    return await _attach(var, btn, definition, top_config, "button", "button")


async def create_switch(var, definition, top_config, overrides=None):
    """Create a switch and register with TeslaBLEVehicle."""
    config = _base_config(definition, definition["class"], "switch", overrides)
    config[CONF_RESTORE_MODE] = switch.RESTORE_MODES['RESTORE_DEFAULT_OFF']
    sw = await switch.new_switch(config)
    return await _attach(var, sw, definition, top_config, "switch", "switch")


async def create_number(var, definition, top_config, overrides=None):
    """Create a number and register with TeslaBLEVehicle."""
    max_val = definition["max"]
    if max_val == "config":
        max_val = top_config.get(CONF_CHARGING_AMPS_MAX, DEFAULT_CHARGING_AMPS_MAX)
    num_config = _base_config(definition, definition["class"], "number", overrides)
    num_config[CONF_MODE] = number.NUMBER_MODES['AUTO']
    if "unit" in definition:
        num_config[CONF_UNIT_OF_MEASUREMENT] = definition["unit"]
    num = await number.new_number(
        num_config,
        min_value=definition["min"],
        max_value=max_val,
        step=definition["step"]
    )
    return await _attach(var, num, definition, top_config, "number", "number")


async def create_lock(var, definition, top_config, overrides=None):
    """Create a lock and register with TeslaBLEVehicle."""
    config = _base_config(definition, definition["class"], "lock", overrides)
    lck = cg.new_Pvariable(config[CONF_ID])
    await lock.register_lock(lck, config)
    return await _attach(var, lck, definition, top_config, "lock", "lock")


async def create_cover(var, definition, top_config, overrides=None):
    """Create a cover and register with TeslaBLEVehicle."""
    config = _base_config(definition, definition["class"], "cover", overrides)
    if "device_class" in definition:
        config[CONF_DEVICE_CLASS] = definition["device_class"]
    cvr = cg.new_Pvariable(config[CONF_ID])
    await cover.register_cover(cvr, config)
    return await _attach(var, cvr, definition, top_config, "cover", "cover")


async def create_climate_entity(var, definition, top_config, overrides=None):
    """Create a climate entity and register with TeslaBLEVehicle."""
    from esphome.components.climate import CONF_VISUAL
    config = _base_config(definition, definition["class"], "climate", overrides)
    config.update({CONF_VISUAL: {}, CONF_ACCURACY_DECIMALS: 1})
    clm = cg.new_Pvariable(config[CONF_ID])
    await climate.register_climate(clm, config)
    return await _attach(var, clm, definition, top_config, "climate", "climate")


# =============================================================================
# CODE GENERATION
# =============================================================================

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)

    cg.add(var.set_vin(config[CONF_VIN]))
    
    role = config[CONF_ROLE]
    charging_amps_max = config[CONF_CHARGING_AMPS_MAX]
    vcsec_interval_seconds = config[CONF_VCSEC_POLL_INTERVAL]
    
    cg.add(var.set_update_interval(vcsec_interval_seconds * 1000))
    # str() strips cv.enum()'s EnumValue subclass so the short role word
    # ("DRIVER"/"CHARGING_MANAGER") reaches C++ instead of the long protobuf name.
    cg.add(var.set_role(str(role)))
    cg.add(var.set_charging_amps_max(charging_amps_max))
    
    # Set polling intervals (convert from seconds to milliseconds)
    cg.add(var.set_vcsec_poll_interval(vcsec_interval_seconds * 1000))
    cg.add(var.set_infotainment_poll_interval_awake(config[CONF_INFOTAINMENT_POLL_INTERVAL_AWAKE] * 1000))
    cg.add(var.set_infotainment_poll_interval_active(config[CONF_INFOTAINMENT_POLL_INTERVAL_ACTIVE] * 1000))
    cg.add(var.set_infotainment_sleep_timeout(config[CONF_INFOTAINMENT_SLEEP_TIMEOUT] * 1000))
    
    entity_overrides = config[CONF_ENTITIES]

    def _overrides_for(definition):
        return entity_overrides.get(definition["id"])

    for creators in (
        (BINARY_SENSORS, create_binary_sensor),
        (SENSORS, create_sensor),
        (TEXT_SENSORS, create_text_sensor),
        (BUTTONS, create_button),
        (SWITCHES, create_switch),
        (LOCKS, create_lock),
        (COVERS, create_cover),
    ):
        for definition in creators[0]:
            overrides = _overrides_for(definition)
            if overrides and overrides.get("disabled"):
                continue
            await creators[1](var, definition, config, overrides)

    for definition in NUMBERS:
        overrides = _overrides_for(definition)
        if overrides and overrides.get("disabled"):
            continue
        await create_number(var, definition, config, overrides)

    climate_overrides = _overrides_for(CLIMATE)
    if not (climate_overrides and climate_overrides.get("disabled")):
        await create_climate_entity(var, CLIMATE, config, climate_overrides)


# =============================================================================
# ACTION SCHEMAS
# =============================================================================

_SIMPLE_ACTION_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle),
})

TESLA_WAKE_ACTION_SCHEMA = _SIMPLE_ACTION_SCHEMA
TESLA_PAIR_ACTION_SCHEMA = _SIMPLE_ACTION_SCHEMA
TESLA_REGENERATE_KEY_ACTION_SCHEMA = _SIMPLE_ACTION_SCHEMA
TESLA_FORCE_UPDATE_ACTION_SCHEMA = _SIMPLE_ACTION_SCHEMA

TESLA_SET_CHARGING_ACTION_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle),
    cv.Required("state"): cv.templatable(cv.boolean),
})

TESLA_SET_CHARGING_AMPS_ACTION_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle),
    cv.Required("amps"): cv.templatable(cv.int_range(min=0, max=80)),
})

TESLA_SET_CHARGING_LIMIT_ACTION_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(TeslaBLEVehicle),
    cv.Required("limit"): cv.templatable(cv.int_range(min=50, max=100)),
})


# =============================================================================
# ACTION REGISTRATION
# =============================================================================

async def _simple_to_code(config, action_id, template_arg):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)


async def _param_to_code(config, action_id, template_arg, args, key, setter, ctype):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[key], args, ctype)
    cg.add(getattr(var, setter)(template_))
    return var


@automation.register_action(
    "tesla_ble_vehicle.wake", WakeAction, TESLA_WAKE_ACTION_SCHEMA, synchronous=True
)
async def tesla_wake_to_code(config, action_id, template_arg, args):
    return await _simple_to_code(config, action_id, template_arg)


@automation.register_action(
    "tesla_ble_vehicle.pair", PairAction, TESLA_PAIR_ACTION_SCHEMA, synchronous=True
)
async def tesla_pair_to_code(config, action_id, template_arg, args):
    return await _simple_to_code(config, action_id, template_arg)


@automation.register_action(
    "tesla_ble_vehicle.regenerate_key", RegenerateKeyAction, TESLA_REGENERATE_KEY_ACTION_SCHEMA, synchronous=True
)
async def tesla_regenerate_key_to_code(config, action_id, template_arg, args):
    return await _simple_to_code(config, action_id, template_arg)


@automation.register_action(
    "tesla_ble_vehicle.force_update", ForceUpdateAction, TESLA_FORCE_UPDATE_ACTION_SCHEMA, synchronous=True
)
async def tesla_force_update_to_code(config, action_id, template_arg, args):
    return await _simple_to_code(config, action_id, template_arg)


@automation.register_action(
    "tesla_ble_vehicle.set_charging", SetChargingAction, TESLA_SET_CHARGING_ACTION_SCHEMA, synchronous=True
)
async def tesla_set_charging_to_code(config, action_id, template_arg, args):
    return await _param_to_code(config, action_id, template_arg, args, "state", "set_state", bool)


@automation.register_action(
    "tesla_ble_vehicle.set_charging_amps", SetChargingAmpsAction, TESLA_SET_CHARGING_AMPS_ACTION_SCHEMA, synchronous=True
)
async def tesla_set_charging_amps_to_code(config, action_id, template_arg, args):
    return await _param_to_code(config, action_id, template_arg, args, "amps", "set_amps", int)


@automation.register_action(
    "tesla_ble_vehicle.set_charging_limit", SetChargingLimitAction, TESLA_SET_CHARGING_LIMIT_ACTION_SCHEMA, synchronous=True
)
async def tesla_set_charging_limit_to_code(config, action_id, template_arg, args):
    return await _param_to_code(config, action_id, template_arg, args, "limit", "set_limit", int)
