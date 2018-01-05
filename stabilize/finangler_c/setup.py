from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

ext_sources = [

    "finangler.pyx",

    # ... additional C sources if necessary

]

ext_modules = Extension(

    name         = "finangler",
    sources      = ext_sources,
    include_dirs = [ numpy.get_include() ]

)

setup(

    name        = "FinAngler",
    version     = "1.0",
    author      = "Izzy Brand and Benjamin Shanahan",
    description = "Calculate rocket fin angles for stabilization.",

    ext_modules = cythonize([ ext_modules ])

)