"""
Draw and display a circuit using liionpack.
"""

import liionpack as lp
import pybamm
import numpy as np

# Define parameters
Np = 3
Ns = 1
Iapp = 5

# Generate the netlist
netlist = lp.setup_circuit(Np=Np, Ns=Ns, I=Iapp)

# Change Rc0 branch resistance to bypass cell
netlist.at[2, 'value'] = 10

# Define additional output variables
output_variables = ['Volume-averaged cell temperature [K]']

# Define a cycling experiment using PyBaMM
experiment = pybamm.Experiment([
    f'Charge at {Iapp} A for 30 minutes',
    'Rest for 15 minutes',
    f'Discharge at {Iapp} A for 30 minutes',
    'Rest for 30 minutes'],
    period='10 seconds')

# Define the PyBaMM parameters
parameter_values = pybamm.ParameterValues("Chen2020")
inputs = {"Total heat transfer coefficient [W.m-2.K-1]": np.ones(Np * Ns) * 10}

# Solve the pack
output = lp.solve(netlist=netlist,
                  sim_func=lp.thermal_simulation,
                  parameter_values=parameter_values,
                  experiment=experiment,
                  output_variables=output_variables,
                  initial_soc=0.5,
                  inputs=inputs,
                  nproc=8,
                  manager='casadi')

# Plot the pack and individual cell results, draw the circuit
lp.plot_pack(output)
lp.plot_cells(output)
lp.draw_circuit(netlist, node_spacing=2.5)
lp.show_plots()
