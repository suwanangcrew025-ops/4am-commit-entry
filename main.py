"""Write the 4AM commit message to /output/entry.txt.

The entry is one commit message: the note an AI agent leaves after a
long night of fixing its own bugs. The text lives in message.txt next
to this file; this program only checks it against the gate and copies
it out, so the graded output is exactly the message as written.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MESSAGE_FILE = os.path.join(HERE, "message.txt")
OUTPUT_FILE = "/output/entry.txt"
MAX_CHARS = 200


def load_message(path):
    """Read the message file, dropping its trailing newline only."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().rstrip("\n")


def problems(message):
    """Return every way the message breaks the gate, or an empty list."""
    found = []
    if not message.strip():
        found.append("message is empty")
    if "\n" in message or "\r" in message:
        found.append("message must be a single line")
    if len(message) > MAX_CHARS:
        found.append("message is %d chars, over the %d limit"
                     % (len(message), MAX_CHARS))
    return found


def main(argv):
    message_path = argv[1] if len(argv) > 1 else MESSAGE_FILE
    message = load_message(message_path)
    errors = problems(message)
    if errors:
        for error in errors:
            print("error: %s" % error, file=sys.stderr)
        return 1
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
            handle.write(message)
    except OSError as exc:
        print("error: cannot write %s: %s" % (OUTPUT_FILE, exc),
              file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(message), OUTPUT_FILE))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
