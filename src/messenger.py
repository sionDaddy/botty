from config import Config
import json
import requests


class Messenger:
    def __init__(self):
        self._config = Config()

    def send(self, msg):
        if self._config.advanced_options['message_highlight']:
            if " magic_" in msg or " (매직)" in msg:
                msg = f"```ini\\n[ {msg} \\n```"
            elif " set_" in msg or " (세트)" in msg:
                msg = f"```diff\\n+ {msg} \\n```"
            elif " rune_" in msg or "룬(" in msg:
                msg = f"```css\\n[ {msg} ]\\n```"
            elif " uniq_" in msg or "rare" in msg or " (유니크)" in msg or " (레어)" in msg:
                # TODO: It is more gold than yellow, find a better yellow highlight
                msg = f"```fix\\n- {msg} \\n```"
            elif " gray_" in msg or " (회색)" in msg:
                msg = f"```python\\n# {msg} \\n```"
            else:
                msg = f"```\\n{msg} \\n```"

        self._send(msg=msg)

    def _send(self, msg):
        url = self._config.general['custom_message_hook']
        if not url:
            return

        headers = {}
        if self._config.advanced_options['message_headers']:
            headers = json.loads(self._config.advanced_options['message_headers'])

        data = json.loads(self._config.advanced_options['message_body_template'].format(msg=msg), strict=False)

        requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    messenger = Messenger()
    messenger.send(msg=f" uniq_test")
