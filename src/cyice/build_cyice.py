from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules == None:
            self.distribution.ext_modules = []
        # todo replace with cython stuff
        # self.distribution.ext_modules.append(
        #     Extension(
        #         "cyice",
        #         sources=["termial_random/random.c"],
        #         extra_compile_args=["-std=c17", "-lm"],
        #     )
        # )
