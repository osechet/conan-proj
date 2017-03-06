
import os
from conans import ConanFile, CMake

CHANNEL = os.getenv("CONAN_CHANNEL", "testing")
USERNAME = os.getenv("CONAN_USERNAME", "osechet")

class TestProjConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "proj/4.9.2@%s/%s" % (USERNAME, CHANNEL)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run("cd bin && .%stest" % os.sep)
