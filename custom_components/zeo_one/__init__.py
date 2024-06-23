"""The Zeo One integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_COUNTRY_CODE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from roborock.web_api import RoborockApiClient
from roborock.version_a01_apis import RoborockMqttClientA01
from roborock import DeviceData
from roborock.roborock_message import RoborockZeoProtocol
from roborock.version_a01_apis.roborock_client_a01 import zeo_data_protocol_entries

from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Zeo One from a config entry."""

    email = config_entry.data[CONF_EMAIL]
    country = config_entry.data[CONF_COUNTRY_CODE]
    password = config_entry.data[CONF_PASSWORD]

    session = async_get_clientsession(hass)
    api = RoborockApiClient(email,f"https://{country}iot.roborock.com")
    ud = await api.pass_login(password)
    hd = await api.get_home_data_v2(ud)
    devlist = [i for i in hd.devices if i.name=='H1'or i.name=='H1 Neo']
    device = devlist[0]
    model = None
    cat = None
    for p in hd.products:
        if p.name=='H1' or p.name=='H1 Neo':
            cat = p.category
            model = p.model
    client = RoborockMqttClientA01(ud, DeviceData(device, model), cat)

    async def update_status():
        try:
            async with async_timeout.timeout(40):
                #status = await client.update_values([RoborockZeoProtocol.MODE, RoborockZeoProtocol.STATE])
                status = await client.update_values(zeo_data_protocol_entries.keys())
                _LOGGER.debug("Fetched status: %s", status)
                return status
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {repr(err)}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=60),
        update_method=update_status,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        DATA_KEY_COORDINATOR: coordinator
    }

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN]

    return unload_ok
