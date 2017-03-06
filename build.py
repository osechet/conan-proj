
import os
from conan.packager import ConanMultiPackager

def build():
    channel = os.getenv("CONAN_CHANNEL", "testing")
    username = os.getenv("CONAN_USERNAME", "osechet")

    builder = ConanMultiPackager(username=username, channel=channel)
    builder.add_common_builds()
    builder.run()

if __name__ == "__main__":
    build()
