"""Setup gradunwarp

Most configuration is now in setup.cfg/pyproject.toml. This file configures
extensions and a legacy script.
"""
from setuptools import setup, Extension
from numpy import get_include
from wheel.bdist_wheel import bdist_wheel


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        # Declare support back to cp32
        # Do not modify Python 2
        if python.startswith('cp3'):
            python, abi = 'cp32', 'abi3'

        return python, abi, plat


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
