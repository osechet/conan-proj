import os
from conans import ConanFile, CMake
from conans.tools import download, unzip, patch

class ProjConan(ConanFile):
    name = "proj"
    version = "4.9.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    exports = ["CMakeLists.txt", "FindPROJ.cmake"]
    url="http://github.com/bilke/conan-proj"
    license="https://github.com/OSGeo/proj.4"

    ZIP_FOLDER_NAME = "proj.4-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.version + ".zip"
        download("https://github.com/OSGeo/proj.4/archive/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        # produced with `diff -U 1 -p Proj4Config.cmake tmp.cmake`
        patch_content = '''--- cmake/Proj4Config.cmake	2016-04-25 09:27:06.000000000 +0200
+++ cmake/Proj4Config.cmake	2016-04-25 09:27:02.000000000 +0200
@@ -38,2 +38,2 @@ set(PACKAGE_VERSION "${${PROJECT_INTERN_

-configure_file(cmake/proj_config.cmake.in src/proj_config.h)
+configure_file(${PROJ4_SOURCE_DIR}/cmake/proj_config.cmake.in ${CMAKE_SOURCE_DIR}/_build/%s/src/proj_config.h)
''' % self.ZIP_FOLDER_NAME
        patch(patch_string=patch_content, base_path=self.ZIP_FOLDER_NAME)
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        self.run("%s && cmake .. -DPROJ4_TESTS=OFF -DBUILD_NAD2BIN=OFF -DCMAKE_INSTALL_PREFIX=../%s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindPROJ.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
            self.cpp_info.libs = ["proj"]