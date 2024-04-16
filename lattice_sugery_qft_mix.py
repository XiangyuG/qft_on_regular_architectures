import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class mapping:
    def __init__(self, unit_size, unit_count, mapping_LtoP, mapping_PtoL):
        self.mapping_LtoP = mapping_LtoP
        self.mapping_PtoL = mapping_PtoL
        self.unit_size = unit_size

        assert unit_count % 2 == 0, 'unit count has to be an even number!'

        self.unit_count = unit_count

    
    def setup_initial_mapping(self):
        # N is the number of qubit in one unit.
        N = self.unit_size
        print(self.unit_count)
        # unit_count_half = self.unit_count//2
        physical_index = 0

        for i in range(0, self.unit_count, 2):
            start = i * N #this is the logical index of the first qubit in the i-th unit
            #first row
            for j in range(start, start+2*N, 2):
                self.mapping_PtoL[physical_index] = j
                self.mapping_LtoP[j] = physical_index
                # print(f'physical_index is {physical_index}, j is {j}')
                physical_index += 1
            
            #second row
            for j in range(start+1, start+ 2*N, 2):
                self.mapping_PtoL[physical_index] = j
                self.mapping_LtoP[j] = physical_index
                # print(f'physical_index is {physical_index}, j is {j}')

                physical_index += 1

    def print_mapping(self):
        print("Logical to Physical Mapping:")
        print(self.mapping_LtoP)
        print("Physical to Logical Mapping:")
        print(self.mapping_PtoL)
    
    def SWAP_gate_implementation(self, physical_q1, physical_q2):
        logical_q1 = self.mapping_PtoL[physical_q1]
        logical_q2 = self.mapping_PtoL[physical_q2]
        self.mapping_LtoP[logical_q1] = physical_q2
        self.mapping_LtoP[logical_q2] = physical_q1
        self.mapping_PtoL[physical_q1] = logical_q2
        self.mapping_PtoL[physical_q2] = logical_q1

        
def LNN_qft(n):
    for m in range(0, 4*n-6, 2):
        k = (m//2)+1
        i = 0
        while i < k - i:
            if i < n and k-i < n:
                print(f'CX( q[{i}], q[{k-i}] )')
            i += 1
            
        i = 0
        while i < k - i:
            if i < n and k-i < n:
                print(f'SWAP( q[{i}], q[{k-i}] )')
            i += 1


def qaoa_gates_sequence(start_position, gate_type, qubit_mapping, physical_unit_number):
    # qubit_mapping.print_mapping()
    # this is a sequence of parallel swap/cphase gates

    N = qubit_mapping.unit_size
    assert start_position != 0 or start_position != 1, 'start_position has to be 0 or 1!'
    offset = N * physical_unit_number
    for i in range(start_position+offset, N+offset, 2):
        if i+1 >= N+offset:
            continue
        if gate_type == 'cphase':
            print(f'cphase( Q[{i}], Q[{i+1}] )')
            print(f'cphase( q[{qubit_mapping.mapping_PtoL[i]}], q[{qubit_mapping.mapping_PtoL[i+1]}] )')
        elif gate_type == 'SWAP':
            print(f'SWAP( Q[{i}], Q[{i+1}] )')
            qubit_mapping.SWAP_gate_implementation(i, i+1)



def qaoa_LNN(N, qubit_mapping, physical_unit_number = 0):
    #this is a qaoa pattern in LNN architecture
    #TODO: mapping is not updated in this version
    print(f'unit_size is {N}')
    print(f'unit_size is {physical_unit_number}')

    for cycle in range(0, 2*N-2+1, 4):
        print(f'cycle {cycle}')
        qaoa_gates_sequence(0, 'cphase', qubit_mapping, physical_unit_number)
        print("-----------------")
        qaoa_gates_sequence(1, 'SWAP', qubit_mapping, physical_unit_number)
        print("-----------------")
        qaoa_gates_sequence(1, 'cphase', qubit_mapping, physical_unit_number)
        print("-----------------")
        qaoa_gates_sequence(0, 'SWAP', qubit_mapping, physical_unit_number)
        print("-----------------")

# this qft version cannot do unit swap!!!! add " offset = 0 " later
def twOxN_qft(if_mix_qaoa, qubit_mapping):
    # this function generates the quantum circuit for a 2xN QFT from the paper Fig. 13(e)
    # each qubit in this pattern is logical qubit, you need to convert it to physical qubit using the mapping!!!!!
    bipartite_all_to_all = []
    
    start = 0 # start is used to control the starting index of unit. 
    unit_size = qubit_mapping.unit_size
    n = 2*unit_size
    qaoa_cycle = 0
    for i in range(start, start + n-2 + 1):
        
        #used to contrl qaoa part
        qaoa_start_position = (1+qaoa_cycle//2) % 2 # be careful with the start position, we need +1 cuz the first swap loop will be skipped.
        # if qaoa_cycle > 2*unit_size: 
        #     if_mix_qaoa = False
        
        only_one_cycle = True # used to control the one cycle of qaoa pattern. Performing a sequence of parallel swap/cphase gates in one cycle.

        # a sequence of parallel swap gates in 2xN QFT, so we need only_one_cycle to control the qaoa pattern only inserted once.
        for j in range(i):
            if j < n and (2*i-j) < n:
                print(f'SWAP( q[{j}], q[{2*i-j}] )')
                physical_q1 = qubit_mapping.mapping_LtoP[j]
                physical_q2 = qubit_mapping.mapping_LtoP[2*i-j]
                qubit_mapping.SWAP_gate_implementation(physical_q1, physical_q2)
                #insert QAOA SWAP here:
                if if_mix_qaoa and only_one_cycle:
                    if qaoa_cycle > 2*unit_size:
                        continue
                    # print(f'start_position is {qaoa_start_position}')
                    qaoa_gates_sequence(qaoa_start_position, 'SWAP', qubit_mapping, physical_unit_number=2)
                    only_one_cycle = False

        print("-----------------")
        for j in range(i):
            if j < n and (2*i-j) < n:
                print(f'loop2: CX( q[{j}], q[{2*i-j}] )')
        print("-----------------")

        only_one_cycle = True
        for j in range(i+1):
            if j < n and (2*i+1-j) < n:
                print(f'loop3: CX( q[{j}], q[{2*i+1-j}] )')
                # insert interactions between 2xN pattern and QAOA pattern
                if if_mix_qaoa and only_one_cycle:
                    for physical_q in range(unit_size, 2*unit_size):
                        pair1 = (qubit_mapping.mapping_PtoL[physical_q], qubit_mapping.mapping_PtoL[physical_q+ unit_size])
                        pair2 = (qubit_mapping.mapping_PtoL[physical_q+unit_size], qubit_mapping.mapping_PtoL[physical_q])
                        if (pair1 not in bipartite_all_to_all) and (pair2 not in bipartite_all_to_all):
                            bipartite_all_to_all.append(pair1)
                            print(pair1)

                    only_one_cycle = False
        print("-----------------")
        qaoa_cycle += 2

    return bipartite_all_to_all
        
def main():
    # N = 4 # N is the unit size
    # coupling_graph = nx.grid_2d_graph(N, N)
    # coupling_graph = nx.convert_node_labels_to_integers(coupling_graph)
    # print(coupling_graph.edges)
    
    #setup initial mapping
    unit_count = 8
    unit_size = 8

    if len(sys.argv) > 1:
        unit_count = int(sys.argv[1])
        unit_size = int(sys.argv[2])
    print(f'unit_count is {unit_count}, unit_size is {unit_size}')

    mapping_LtoP = {}
    mapping_PtoL = {}
    qubit_mapping = mapping(unit_size, unit_count, mapping_LtoP, mapping_PtoL)
    qubit_mapping.setup_initial_mapping()
    # qubit_mapping.print_mapping()
    if_mix_qaoa = True
    result = twOxN_qft(if_mix_qaoa, qubit_mapping)
    print(f'number of interactions is {len(result)}')
    # LNN_qft(6)
    # qaoa_LNN(qubit_mapping.unit_size, qubit_mapping, unit_number=2)

    
if __name__ == "__main__":
    main()
