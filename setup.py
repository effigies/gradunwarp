"""Setup gradunwarp

Most configuration is now in setup.cfg/pyproject.toml. This file configures
extensions and a legacy script.
"""
import sys
from setuptools import setup, Extension
from numpy import get_include
from wheel.bdist_wheel import bdist_wheel


class bdist_wheel_abi3(bdist_wheel):
    def finalize_options(self):
        self.py_limited_api = f"cp3{sys.version_info[1]}"
        super().finalize_options()

setup(
    ext_modules=[
        Extension(
            'gradunwarp.core.{}_ext'.format(mod),
            include_dirs=[get_include()],
            sources=['gradunwarp/core/{}_ext.c'.format(mod)],
            extra_compile_args=['-O3'],
            define_macros=[
                ('Py_LIMITED_API', '0x03020000'),
                ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
            ],
            py_limited_api=True,
        )
        for mod in ('interp3', 'legendre', 'transform_coordinates')
    ],
    scripts=['gradunwarp/core/gradient_unwarp.py'],
    cmdclass={'bdist_wheel': bdist_wheel_abi3},
)
