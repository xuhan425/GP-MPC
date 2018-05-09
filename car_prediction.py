# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:12:26 2018

@author: Helge-André Langåker
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sys import path
#path.append(r"C:\Users\helgeanl\Google Drive\NTNU\Masteroppgave\casadi-py36-v3.4.0")
path.append(r"C:\Users\helgeanl\Google Drive\NTNU\Masteroppgave\casadi-py36-v3.4.0")
path.append(r"./GP_MPC/")

import numpy as np
import casadi as ca

from gp_casadi.optimize import train_gp, validate
from gp_casadi.gp_functions import predict_casadi

from gp_casadi.mpc_class import MPC
from simulation.car_model_v2 import sim_system, onestep_system
dir_data = 'data/'
dir_parameters = 'parameters/'





if __name__ == "__main__":
    X = np.loadtxt(dir_data + 'X_matrix_car')
    Y = np.loadtxt(dir_data + 'Y_matrix_car')
    
    X_test = np.loadtxt(dir_data + 'X_matrix_test_car')
    Y_test = np.loadtxt(dir_data + 'Y_matrix_test_car')
    
    solver_opts = {}
    solver_opts['ipopt.linear_solver'] = 'ma27'
    solver_opts['ipopt.max_cpu_time'] = 10
    #solver_opts["ipopt.hessian_approximation"] = "limited-memory"
    solver_opts['expand']= True
#    solver_opts['ipopt.print_level'] = 5
    
    
    optimize = True
    meanFunc = 'zero'
    log = False
    N, Nx = X.shape  # Number of sampling points and inputs
    Ny = Y.shape[1]  # Number of outputs
    if optimize:
        opt = train_gp(X, Y, meanFunc=meanFunc, log=log, solver_opts=solver_opts)
        hyper = opt['hyper']
        invK  = opt['invK']
        lam_x = opt['lam_x']
        validate(X_test, Y_test, X, Y, invK, hyper, meanFunc)
        for i in range(Ny):
            np.savetxt(dir_parameters + 'invK' + str(i + 1), invK[i, :, :], delimiter=',')
        np.savetxt(dir_parameters + 'hyper_opt', hyper, delimiter=',')
    else:
        hyper = np.loadtxt(dir_parameters + 'hyper_opt', delimiter=',')
        invK = np.zeros((Ny, N, N))
        for i in range(Ny):
            invK[i, :, :] = np.loadtxt(dir_parameters + 'invK' + str(i + 1), delimiter=',')

    
    
    
    dt = 0.05
    x0 = np.array([2, 0.01, 0.01, 0.01, 0.01 , 0.01])
    x_sp = np.array([3., 0., 0., 0., 10., 0. ])
    ulb = [-.5, -.5, -.1,]
    uub = [.5, .5, .1,]
    xlb = [1, -.5, -2.0, -2.0, .0, .0]
    xub = [30, .5, 2.0, 2.0, np.inf, np.inf]
    
    u_test = np.array([0.1, 0.1, 0]).reshape(1,3)
    predict_casadi(X, Y, invK, hyper, x0, u_test, sim_system)
    
    
#    solver_opts['ipopt.check_derivatives_for_naninf'] = 'no'
#    solver_opts['print_time'] = True
#    solver_opts['verbose'] = True
#    mpc = MPC(X, Y, x0, x_sp, invK, hyper, horizon=1*dt,
#          sim_time=1*dt, dt=dt, method='TA',
#          ulb=ulb, uub=uub, xlb=xlb, xub=xub,
#          meanFunc=meanFunc, terminal_constraint=None, log=log,
#          costFunc='quad', feedback=True, solver_opts=solver_opts,simulator=sim_system, test=onestep_system)

#    mpc.plot()
   # x, u = mpc.solve(simulator=sim_system)
    
#    x_sp = np.array([4., 18., 14.2, 30.3])
#    x, u = mpc.solve(simulator=sim_system, x0=x[-1,:], x_sp=x_sp, u0=u[-1,:])

