# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf
from mytask.task_scheduler import  fetch_volume_predict

@plugins.register(
    name="yykplugin",
    desire_priority=99,
    hidden=True,
    desc="yykplugin",
    version="0.1",
    author="YYK",
)


class Yykplugin(Plugin):

    def __init__(self):
        super().__init__()
        try:
            self.config = super().load_config()
            if not self.config:
                self.config = self._load_config_template()
            logger.info("[YYKplugin] initialized")
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        except Exception as e:
            logger.error(f"[YYKplugin] Initialization failed: {e}")
            raise Exception("[YYKplugin] init failed, ignored.")


    def on_handle_context(self, e_context: EventContext):
        """
        Handles incoming events and provides JSON data as a reply.
        """
        if e_context["context"].type != ContextType.TEXT:
            return

        content = e_context["context"].content.strip()
        logger.debug(f"[YYKplugin] on_handle_context content: {content}")

        if content == "交易量":
            # Fetch JSON data

            formated_msg = fetch_volume_predict()
            # Prepare the reply
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = formated_msg
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # Stop further processing
            return

    def fetch_json(self):
        """
        Custom function to fetch JSON data.
        Replace this with actual logic to fetch data from an API or database.
        """
        return {
            "status": "success",
            "data": {
                "message": "Hello from YYKplugin!",
                "details": "This is a JSON response.",
                "timestamp": "2024-12-19T12:00:00Z"
            }
        }

    def get_help_text(self, **kwargs):
        """
        Returns help text for the plugin.
        """
        help_text = "输入“交易量”，我会回复交易量数据。\n"
        return help_text

    def _load_config_template(self):
        """
        Loads the plugin configuration template if no config is found.
        """
        logger.debug("No YYKplugin config.json, using plugins/yykplugin/config.json.template")
        try:
            plugin_config_path = os.path.join(self.path, "config.json.template")
            if os.path.exists(plugin_config_path):
                with open(plugin_config_path, "r", encoding="utf-8") as f:
                    plugin_conf = json.load(f)
                    return plugin_conf
        except Exception as e:
            logger.exception(e)