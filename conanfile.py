
import os
import re
from os import close, remove
from shutil import move
from tempfile import mkstemp
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip

class ProjConan(ConanFile):
    name = "proj"
    version = "4.9.2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["FindProj.cmake"]
    url = "http://github.com/bilke/conan-proj"
    license = "https://github.com/OSGeo/proj.4"

    ZIP_FOLDER_NAME = "proj.4-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.version + ".zip"
        download("https://github.com/OSGeo/proj.4/archive/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

        datum = "proj-datumgrid-1.5.zip"
        download("http://download.osgeo.org/proj/%s" % datum, datum)
        unzip(datum, "%s/nad" % self.ZIP_FOLDER_NAME)
        os.unlink(datum)

    def build(self):
        if self.settings.os == "Windows":
            self._build_win()
        else:
            self._build_unix()

    def _build_win(self):
        self._replace_in_file("%s/nmake.opt" % (self.ZIP_FOLDER_NAME),
                              r"^INSTDIR=.*",
                              "INSTDIR=%s" % (self.package_folder.replace('\\', r'\\')))
        self.run("cd %s && nmake /f makefile.vc" % (self.ZIP_FOLDER_NAME))
        self.run("cd %s && nmake /f makefile.vc install" % (self.ZIP_FOLDER_NAME))

    def _build_unix(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            config_args = ["--prefix %s" % self.package_folder]

            if self.options.shared:
                config_args += ["--enable-shared=yes", "--enable-static=no"]
            else:
                config_args += ["--enable-shared=no", "--enable-static=yes"]
            if self.settings.os != "Windows":
                self.run("chmod +x %s/configure" % self.ZIP_FOLDER_NAME)
                self.run("chmod +x %s/install-sh" % self.ZIP_FOLDER_NAME)

            self.run("cd %s && ../%s/configure %s"
                     % (self.ZIP_FOLDER_NAME, self.ZIP_FOLDER_NAME, " ".join(config_args)))
            self.run("cd %s && make" % (self.ZIP_FOLDER_NAME))
            self.run("cd %s && make install" % (self.ZIP_FOLDER_NAME))

    def package(self):
        self.copy("FindProj.cmake", ".", ".")

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["proj_4_9_d"]
            else:
                self.cpp_info.libs = ["proj_4_9"]
        else:
            self.cpp_info.libs = ["proj"]

    def _replace_in_file(self, file_path, pattern, subst):
        file_handler, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    new_file.write(re.sub(pattern, subst, line))
        close(file_handler)
        remove(file_path)
        move(abs_path, file_path)
