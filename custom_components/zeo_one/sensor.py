from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from roborock.roborock_message import RoborockZeoProtocol
from roborock.code_mappings import ZeoError, ZeoMode, ZeoProgram, ZeoTemperature, ZeoRinse, ZeoSpin, ZeoDryingMode, ZeoDetergentType, ZeoSoftenerType
from .const import *

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Zeo One sensors from config entry."""

    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    async_add_entities([
        ZeoOneModeSensor(coordinator, config_id),
        ZeoOneStateSensor(coordinator, config_id),
        ZeoOneCountdownSensor(coordinator, config_id),
        ZeoOneWashingLeftSensor(coordinator, config_id),
        ZeoOneErrorSensor(coordinator, config_id),
        ZeoOneTimesAfterCleanSensor(coordinator, config_id),
        ZeoOneDetergentEmptySensor(coordinator, config_id),
        ZeoOneSoftenerEmptySensor(coordinator, config_id),
        ZeoOneProgramSensor(coordinator, config_id),
        ZeoOneTempSensor(coordinator, config_id),
        ZeoOneRinseTimesSensor(coordinator, config_id),
        ZeoOneSpinLevelSensor(coordinator, config_id),
        ZeoOneDryingModeSensor(coordinator, config_id),
        ZeoOneDetergentTypeSensor(coordinator, config_id),
        ZeoOneSoftenerTypeSensor(coordinator, config_id),
        ZeoOneSoundSetSensor(coordinator, config_id),
    ])


class ZeoOneBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, config_id: str):
        super().__init__(coordinator)
        self.config_id = config_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name="Zeo One",
            manufacturer="Zeo",
            suggested_area="Bathroom",
        )

class ZeoOneModeSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Mode"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_mode"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.MODE, "unknown")


class ZeoOneStateSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One State"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_state"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.STATE, "unknown")

class ZeoOneCountdownSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Countdown"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_countdown"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.COUNTDOWN, 0)


class ZeoOneWashingLeftSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Washing Left"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_washing_left"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.WASHING_LEFT, 0)


class ZeoOneErrorSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Error"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_error"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        error_code = status.get(RoborockZeoProtocol.ERROR, 0)
        return ZeoError(error_code).name


class ZeoOneTimesAfterCleanSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Times After Clean"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_times_after_clean"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.TIMES_AFTER_CLEAN, 0)


class ZeoOneDetergentEmptySensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Detergent Empty"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_detergent_empty"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.DETERGENT_EMPTY, False)


class ZeoOneSoftenerEmptySensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Softener Empty"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_softener_empty"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.SOFTENER_EMPTY, False)


class ZeoOneProgramSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Program"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_program"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        program_code = status.get(RoborockZeoProtocol.PROGRAM, 0)
        return ZeoProgram(program_code).name


class ZeoOneTempSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Temperature"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_temp"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        temp_code = status.get(RoborockZeoProtocol.TEMP, 0)
        return ZeoTemperature(temp_code).name

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS


class ZeoOneRinseTimesSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Rinse Times"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_rinse_times"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        rinse_code = status.get(RoborockZeoProtocol.RINSE_TIMES, 0)
        return ZeoRinse(rinse_code).name


class ZeoOneSpinLevelSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Spin Level"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_spin_level"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        spin_code = status.get(RoborockZeoProtocol.SPIN_LEVEL, 0)
        return ZeoSpin(spin_code).name


class ZeoOneDryingModeSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Drying Mode"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_drying_mode"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        drying_mode_code = status.get(RoborockZeoProtocol.DRYING_MODE, 0)
        return ZeoDryingMode(drying_mode_code).name


class ZeoOneDetergentTypeSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Detergent Type"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_detergent_type"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        detergent_type_code = status.get(RoborockZeoProtocol.DETERGENT_TYPE, 0)
        return ZeoDetergentType(detergent_type_code).name


class ZeoOneSoftenerTypeSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Softener Type"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_softener_type"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        softener_type_code = status.get(RoborockZeoProtocol.SOFTENER_TYPE, 0)
        return ZeoSoftenerType(softener_type_code).name


class ZeoOneSoundSetSensor(ZeoOneBaseSensor):
    @property
    def name(self) -> str:
        return "Zeo One Sound Set"

    @property
    def unique_id(self) -> str:
        return f"{self.config_id}_sound_set"

    @property
    def state(self) -> str:
        status: dict = self.coordinator.data
        return status.get(RoborockZeoProtocol.SOUND_SET, False)