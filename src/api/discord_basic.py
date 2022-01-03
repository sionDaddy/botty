from .i_api import IApi
import json
import requests

class DiscordBasic(IApi):
    def _send(self, msg: str):
        msg = self._advanced_colors(msg)
        url = self._config.general['custom_message_hook']
        if not url:
            return

        headers = {}
        if self._config.advanced_options['message_headers']:
            headers = json.loads(self._config.advanced_options['message_headers'])

        data = json.loads(self._config.advanced_options['message_body_template'].format(msg=msg), strict=False)

        requests.post(url, headers=headers, json=data)

    def _advanced_colors(self, msg: str):        
        if self._config.advanced_options['message_highlight']:
            if " magic_" in msg:
                msg = f"```ini\\n[ {msg} \\n```"
            elif " set_" in msg:
                msg = f"```diff\\n+ {msg} \\n```"
            elif " rune_" in msg:
                msg = f"```css\\n[ {msg} ]\\n```"
            elif " uniq_" in msg or "rare" in msg:
                # TODO: It is more gold than yellow, find a better yellow highlight
                msg = f"```fix\\n- {msg} \\n```"
            elif " gray_" in msg:
                msg = f"```python\\n# {msg} \\n```"
            else:
                msg = f"```\\n{msg} \\n```"
        
        return msg
