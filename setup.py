"""Setup gradunwarp

Most configuration is now in pyproject.toml. This file configures
extensions and a legacy script.
"""
from setuptools import setup, Extension
from numpy import get_include


setup(
    ext_modules=[
        Extension(
            'gradunwarp.core.{}_ext'.format(mod),
            include_dirs=[get_include()],
            sources=['gradunwarp/core/{}_ext.c'.format(mod)],
            extra_compile_args=['-O3'],
        )
        for mod in ('interp3', 'legendre', 'transform_coordinates')
    ],
    scripts=['gradunwarp/core/gradient_unwarp.py'],
)
