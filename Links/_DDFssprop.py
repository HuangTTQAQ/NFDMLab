# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 18:29:07 2019

@author: vinodbajaj
"""

# Copyright 2018, Sander Wahls (TU Delft)
# Copyright 2018, Marius Brehler (TU Dortmund)
# Copyright 2006, Thomas E. Murphy
#
# This file is part of NFDMLab.
#
# NFDMLab is free software; you can redistribute it and/or
# modify it under the terms of the version 2 of the GNU General
# Public License as published by the Free Software Foundation.
#
# NFDMLab is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with NFDMLab; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA

import numpy as np
from warnings import warn
import matplotlib.pyplot as plt

def _DDFssprop(u0,dt,dz,nz,alpha,D,R):
    """This function solves the nonlinear Schrodinger equation for
    pulse propagation in an optical fiber using the split-step
    Fourier method.
    It has feature to include length dependent variation in the 
    dispersion and nonlinear parameter varies over length.
    

    The following effects are included in the model: group velocity
    dispersion (GVD), loss, and self-phase
    modulation (gamma).

    USAGE

    u1 = ssprop(u0,dt,dz,nz,alpha,D,R)
    

    INPUT

    u0 - starting field amplitude (vector)
    dt - time step
    dz - propagation stepsize
    nz - number of steps to take, ie, ztotal = dz*nz
    alpha - power loss coefficient, ie, P=P0*exp(-alpha*z)
    D - dispersion parameter over length of span (vector : size 1 X Nsteps )
    R - nonlinear parameter over length of span (vector : size 1 X Nsteps )
    

    OUTPUT

    u1 - field at the output

    NOTES  The dimensions of the input and output quantities can
    be anything, as long as they are self consistent.  E.g., if
    |u|^2 has dimensions of Watts and dz has dimensions of
    meters, then gamma should be specified in W^-1*m^-1.
    Similarly, if dt is given in picoseconds, and dz is given in
    meters, then beta(n) should have dimensions of ps^(n-1)/m.

    AUTHORS

    This function is a Python port of the script ssprop.m by
    Thomas E. Murphy (tem@umd.edu), which comes with the SSPROP
    package (https://www.photonics.umd.edu/software/ssprop/).
    The port has been written by Sander Wahls and has been
    modified by Marius Brehler.
    """

    nt = np.size(u0)
    assert nt%2 == 0
    w = 2*np.pi*np.hstack((np.arange(0, nt/2), np.arange(-nt/2, 0)))/(dt*nt)
   
    u1 = u0    
    for iz in range(0, nz):
        beta  = D[iz]   # get beta_2 value at that location
        gamma = R[iz]   # get gamma value at that location
        halfstep = np.exp(1j*beta*w**2/2*dz/2)       

        uhalf = np.fft.ifft(halfstep*np.fft.fft(u1)) 
        uv = uhalf*np.exp(1j*gamma*(np.abs(u1)**2*dz))
        uv = np.fft.ifft(halfstep*np.fft.fft(uv))
        u1 = uv*np.exp(-alpha*dz)
    return u1