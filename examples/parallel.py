"""
Compare a generated netlist circuit to a LTspice netlist circuit. Dataframes
from the two approaches should be similar. Voltage and current results should
be the same for the two netlist approaches.
"""

import liionpack as lp
import numpy as np

# Define parameters
Np = 3
Ns = 1
Iapp = 5
V = 4.2
Ri = 1e-2
Rc = 1e-2
Rb = 1e-4
Rt = 1e-5

# Generate the netlist and solve circuit
netlist = lp.setup_circuit(Np=Np, Ns=Ns, Ri=Ri, Rc=Rc, Rb=Rb, Rt=Rt, I=Iapp, V=V)
volt, curr = lp.solve_circuit(netlist)

# Load the netlist and solve circuit
netlist2 = lp.read_netlist(filepath='parallel.cir', Rb=Rb, Ri=Ri, Rc=Rc, Rt=Rt, I=Iapp, V=V)
volt2, curr2 = lp.solve_circuit(netlist2)

# Compare netlist dataframes
print(netlist)
print(netlist2)

# Compare voltage and current results
print(f'V match: {np.allclose(np.sort(volt), np.sort(volt2))}')
print(f'I match: {np.allclose(np.sort(curr), np.sort(curr2))}')

# Plot the circuit using netlist from setup_circuit
# The netlist from LTspice is not compatible with draw_circuit
lp.draw_circuit(netlist, node_spacing=2.5)
lp.show_plots()
