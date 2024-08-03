import logging
from logging import Logger

log: Logger = logging.getLogger(__name__)


class JsActions:
    open_config_action: str = "open-config-action"
    open_check_media_action: str = "open-check-media-action"
