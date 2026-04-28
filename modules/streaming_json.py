import json


class JsonObjectStream:
    def __init__(self):
        self.buffer = ""
        self.decoder = json.JSONDecoder(strict=False)
        self.started = False
        self.in_string = False
        self.escape = False
        self.depth = 0
        self.object_start = None
        self.consumed_until = 0

    def feed(self, text):
        self.buffer += text
        emitted = []
        i = self.consumed_until
        while i < len(self.buffer):
            ch = self.buffer[i]
            if not self.started:
                if ch == "[":
                    self.started = True
                i += 1
                continue

            if self.object_start is None:
                if ch == "{":
                    self.object_start = i
                    self.depth = 1
                    self.in_string = False
                    self.escape = False
                elif ch == "]":
                    self.consumed_until = i + 1
                    break
                i += 1
                continue

            if self.in_string:
                if self.escape:
                    self.escape = False
                elif ch == "\\":
                    self.escape = True
                elif ch == '"':
                    self.in_string = False
            else:
                if ch == '"':
                    self.in_string = True
                elif ch == "{":
                    self.depth += 1
                elif ch == "}":
                    self.depth -= 1
                    if self.depth == 0:
                        raw = self.buffer[self.object_start : i + 1]
                        emitted.append(self.decoder.decode(raw))
                        self.object_start = None
                        self.consumed_until = i + 1
            i += 1

        self.consumed_until = i
        if self.consumed_until > 4096 and self.object_start is None:
            self.buffer = self.buffer[self.consumed_until :]
            i -= self.consumed_until
            self.consumed_until = 0
        return emitted


def iter_anthropic_text(response):
    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line or not raw_line.startswith("data:"):
            continue
        data = raw_line[5:].strip()
        if data == "[DONE]":
            break
        try:
            event = json.loads(data)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "content_block_delta":
            delta = event.get("delta") or {}
            if delta.get("type") == "text_delta":
                yield delta.get("text", "")
