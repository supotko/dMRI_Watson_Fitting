from setuptools import setup, Extension
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

suite_sparse_libs  = ['lapack', 'ccolamd', 'spqr', 'cholmod', 'colamd','camd', 'amd', 'suitesparseconfig']
ceres_libs         = ['glog', 'gflags']
libraries          = ceres_libs + suite_sparse_libs + ['pthread', 'fftw3', 'm', 'watsonfit']

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("watsonfit", 
                  sources=["cppwrapper/watsonfitwrapper.pyx"
                       ],
                  include_dirs=[".",np.get_include()],
                  libraries=libraries,
                  language="c++",
                  extra_compile_args=["-I.", "-O3", "-ffast-math", "-march=native", "-fopenmp"],
                  extra_link_args=["-L/usr/local/include","-fopenmp","-Wl,--no-as-needed"]
             )
        ]
)