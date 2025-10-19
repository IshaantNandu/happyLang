class myLang:
    def __init__(self, code):
        self.preCode = code.splitlines()
        self.execution = ""
        self.handlers = {
            "speak": self._handle_speak,
            "listen": self._handle_listen,
            "repeat": self._handle_repeat,
            "end": self._handle_end
        }
        self.indent_level = 0

    def raise_error(self, message):
        raise ValueError(f"Error: {message}")

    def _get_indent_string(self):
        return "    " * self.indent_level

    # *** CRITICAL FIX HERE ***
    # This method is now responsible for ensuring every line added starts
    # with the correct indentation and is followed by a single newline.
    def _add_line(self, code_line):
        # Ensure we don't start with a blank line for the first line.
        # Otherwise, prepend the indentation string and append a newline.
        if self.execution == "":
            self.execution += code_line
        else:
            self.execution += "\n" + self._get_indent_string() + code_line

    def _handle_repeat(self, s):
        s_clean = s.rstrip(':').strip()
        parts = s_clean.split()

        if len(parts) != 3 or parts[2].lower() != "times":
            self.raise_error("Invalid 'repeat' syntax. Use: repeat <number> times")

        count_str = parts[1]
        self._add_line(f"for _i in range({count_str}):")
        self.indent_level += 1

    def _handle_end(self, s):
        if self.indent_level == 0:
            self.raise_error("'end' without matching block (e.g., 'repeat')")

        self.indent_level -= 1

    def _handle_speak(self, s):
        payload = s[5:].strip()
        if not payload:
            self.raise_error("Nothing to speak")

        # The fix is to NOT add a leading newline here. The _add_line method
        # handles the newline and indentation for all lines after the first.
        if len(payload) >= 2 and payload[0] in "\"'" and payload[-1] == payload[0]:
            self._add_line(f"print({payload})")
        elif payload.isidentifier():
            self._add_line(f"print({payload})")
        else:
            self._add_line(f"print({repr(payload)})")

    def _handle_listen(self, s):
        # Example format: listen <variable> int/text
        # s is the whole line, e.g., "listen t int"

        parts = s.split()

        if len(parts) != 3:
            self.raise_error("Invalid 'listen' syntax. Use: listen <variable> int or listen <variable> text")

        variable_name = parts[1]
        data_type = parts[2].lower()  # 'int' or 'text'

        if data_type == 'int':
            # This is the integer conversion we had before.
            self._add_line(f"{variable_name} = int(input())")
        elif data_type == 'text':
            # This is the string input (the default Python input).
            self._add_line(f"{variable_name} = input()")
        else:
            self.raise_error(f"Unknown data type '{data_type}'. Must be 'int' or 'text'.")


    def transpile(self):
        for line in self.preCode:
            s = line.strip()
            if not s:
                continue
            parts = s.split(None, 1)
            head = parts[0]

            handler = self.handlers.get(head)
            if handler:
                handler(s)
            else:
                if "=" in s:
                    self._add_line(s)
                else:
                    self.raise_error(f"Unknown word: '{head}'")

        if self.indent_level > 0:
            self.raise_error(f"Missing 'end' for {self.indent_level} block(s)")


with open("helloworld.hpy") as f:
    y = f.read()
    print(y)
    print("")
    x = myLang(y)
    x.transpile()
    print(x.execution)
    print("")
    exec(x.execution)