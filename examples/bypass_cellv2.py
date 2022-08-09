"""
Create small pack with different SOC for each cell. Adjust the Iapp current
such that voltage limits are reached. The Rc resistance should be adjusted to
bypass a cell. See line 450 in solvers.py for voltage check and Rc value.
"""

import liionpack as lp
import pybamm
import numpy as np

# Define parameters
Np = 3
Ns = 1
Iapp = 12

# Generate the netlist
netlist = lp.setup_circuit(Np=Np, Ns=Ns, I=Iapp)

# Change Rc0 branch resistance to bypass cell
# netlist.at[2, 'value'] = 20

# Define additional output variables
output_variables = [
    'Volume-averaged cell temperature [K]',
    "X-averaged negative particle surface concentration [mol.m-3]",
    "X-averaged positive particle surface concentration [mol.m-3]"]

# Define a cycling experiment using PyBaMM
experiment = pybamm.Experiment([
    f'Charge at {Iapp} A for 30 minutes',
    'Rest for 15 minutes',
    f'Discharge at {Iapp} A for 30 minutes',
    'Rest for 30 minutes'],
    period='10 seconds')

# Define the PyBaMM parameters
param = pybamm.ParameterValues("Chen2020")

soc = np.array([0.5, 0.5, 0.5])
c_s_n_init, c_s_p_init = lp.update_init_conc(param, SoC=soc, update=False)

param.update({
    "Initial concentration in negative electrode [mol.m-3]": "[input]",
    "Initial concentration in positive electrode [mol.m-3]": "[input]"})

inputs = {
    "Initial concentration in negative electrode [mol.m-3]": c_s_n_init,
    "Initial concentration in positive electrode [mol.m-3]": c_s_p_init,
    "Total heat transfer coefficient [W.m-2.K-1]": np.ones(Np * Ns) * 10}

# Solve the pack
output = lp.solve(netlist=netlist,
                  sim_func=lp.thermal_simulation,
                  parameter_values=param,
                  experiment=experiment,
                  output_variables=output_variables,
                  initial_soc=None,
                  inputs=inputs,
                  nproc=8,
                  manager='casadi')

# Plot the pack and individual cell results, draw the circuit
lp.plot_pack(output)
lp.plot_cells(output)
lp.draw_circuit(netlist, node_spacing=2.5)
lp.show_plots()
