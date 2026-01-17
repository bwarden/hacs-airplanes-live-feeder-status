"""Constants for airplanes.live feeder status."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Airplanes.live Feeder Status"
DOMAIN = "airplanes_live_feeder_status"
VERSION = "0.1.0"
ATTRIBUTION = "Data provided by Airplanes.live"

URL_FEED_STATUS = "https://api.airplanes.live/feed-status"
