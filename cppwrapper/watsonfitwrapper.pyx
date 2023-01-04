#!python
#cython: language_level=3, boundscheck=False, wraparound=False

cimport cython
import cython as cython
from cython.parallel import prange

cimport watsonfitwrapper
import numpy as np
cimport numpy as np
np.import_array()

def mw_openmp_mult(double[:,:] x, double[:,:] signal, double[:,:] est_signal, double[:,:] dipy_v, double[:,:,:,:] pysh_v, double[:,:,:,:] rot_pysh_v, double[:,:] angles_v, double[:] loss, int amount, int order, int num_of_dir, int no_spread):
        if order == 4:
                mw_openmp_mult_o4(x,signal,est_signal,dipy_v,pysh_v,rot_pysh_v,angles_v,loss,amount,num_of_dir,no_spread)
        elif order == 6:
                mw_openmp_mult_o6(x,signal,est_signal,dipy_v,pysh_v,rot_pysh_v,angles_v,loss,amount,num_of_dir,no_spread)
        elif order == 8:
                mw_openmp_mult_o8(x,signal,est_signal,dipy_v,pysh_v,rot_pysh_v,angles_v,loss,amount,num_of_dir,no_spread)

cdef void mw_openmp_mult_o4(double[:,:] x, double[:,:] signal, double[:,:] est_signal, double[:,:] dipy_v, double[:,:,:,:] pysh_v, double[:,:,:,:] rot_pysh_v, double[:,:] angles_v, double[:] loss, int amount, int num_of_dir, int no_spread):
        with nogil:
                watsonfitwrapper.minimize_watson_mult_o4(&x[0,0],&signal[0,0],&est_signal[0,0],&dipy_v[0,0],&pysh_v[0,0,0,0],&rot_pysh_v[0,0,0,0],&angles_v[0,0],&loss[0],amount,num_of_dir,no_spread)

cdef void mw_openmp_mult_o6(double[:,:] x, double[:,:] signal, double[:,:] est_signal, double[:,:] dipy_v, double[:,:,:,:] pysh_v, double[:,:,:,:] rot_pysh_v, double[:,:] angles_v, double[:] loss, int amount, int num_of_dir, int no_spread):
        with nogil:
                watsonfitwrapper.minimize_watson_mult_o6(&x[0,0],&signal[0,0],&est_signal[0,0],&dipy_v[0,0],&pysh_v[0,0,0,0],&rot_pysh_v[0,0,0,0],&angles_v[0,0],&loss[0],amount,num_of_dir,no_spread)

cdef void mw_openmp_mult_o8(double[:,:] x, double[:,:] signal, double[:,:] est_signal, double[:,:] dipy_v, double[:,:,:,:] pysh_v, double[:,:,:,:] rot_pysh_v, double[:,:] angles_v, double[:] loss, int amount, int num_of_dir, int no_spread):
        with nogil:
                watsonfitwrapper.minimize_watson_mult_o8(&x[0,0],&signal[0,0],&est_signal[0,0],&dipy_v[0,0],&pysh_v[0,0,0,0],&rot_pysh_v[0,0,0,0],&angles_v[0,0],&loss[0],amount,num_of_dir,no_spread)