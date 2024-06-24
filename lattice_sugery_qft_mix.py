import sys
# import networkx as nx
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
        # this function sets up the initial mapping for NxN lattice
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


def LNN_qft_unit_base(n):
    # this is a unit base version of LNN_qft
    # every two layers of sway are performed together
    # n is the number of unit

    print('--------------- Getting unit base LNN QFT......')
    #preparing the original qft
    unit_operation_sequnece = {}
    step = 0
    for m in range(0, 4*n-6, 2):
        k = (m//2)+1
        i = 0
        operations = []
        while i < k - i:
            if i < n and k-i < n:
                # print(f'CX( q[{i}], q[{k-i}] )')
                operations.append((i, k-i))
            i += 1
        unit_operation_sequnece[f'CX{step}'] = operations
        step += 1
        
        i = 0
        operations = []
        while i < k - i:
            if i < n and k-i < n:
                # print(f'SWAP( q[{i}], q[{k-i}] )')
                operations.append((i, k-i))
            i += 1
        unit_operation_sequnece[f'SWAP{step}'] = operations
        step += 1
    # print(unit_operation_sequnece)

    # Convert original qft to make every two layers of SWAP are performed together
    # Convert the dictionary to a list of tuples for easier manipulation
    steps_list = list(unit_operation_sequnece.items())
    # print(steps_list)
    # Iterate through the steps and swap the order of every second SWAP with its preceding CX
    for i in range(len(steps_list)):
        if 'SWAP' in steps_list[i][0] and int(steps_list[i][0].replace('SWAP', '')) % 4 == 3:
            # Check if the previous step is a CX step
            if i > 0 and 'CX' in steps_list[i-1][0]:
                # Swap the current SWAP step with the previous CX step
                steps_list[i-1], steps_list[i] = steps_list[i], steps_list[i-1]

    # Convert the list of tuples back to a dictionary
    output = dict(steps_list)
    print('All numbers are logical unit index')
    print(output)
    return output

def qaoa_gates_sequence(start_position, gate_type, qubit_mapping, logical_unit_number):
    # this is a sequence of parallel swap/cphase gates depends on gate_type

    N = qubit_mapping.unit_size
    assert start_position != 0 or start_position != 1, 'start_position has to be 0 or 1!'
    offset = N * logical_unit_number
    for i in range(start_position+offset, N+offset, 2):
        if i+1 >= N+offset:
            # i guess here is to skip the last gate using qubit out of the unit
            continue
        if gate_type == 'cphase':
            print(f'')
            print(f'cphase( q[{i}], q[{i+1}] ) = cphase( Q[{qubit_mapping.mapping_LtoP[i]}], Q[{qubit_mapping.mapping_LtoP[i+1]}] )')
        elif gate_type == 'SWAP':
            print(f'QAOA-SWAP( Q[{qubit_mapping.mapping_LtoP[i]}], Q[{qubit_mapping.mapping_LtoP[i+1]}] )')
            qubit_mapping.SWAP_gate_implementation(qubit_mapping.mapping_LtoP[i], qubit_mapping.mapping_LtoP[i+1])


def logical_unit_swap(qubit_mapping, unit1, unit2):
    # this function swaps two logical units in the qubit_mapping
    N = qubit_mapping.unit_size
    for i in range(N):
        qubit_mapping.SWAP_gate_implementation(qubit_mapping.mapping_LtoP[unit1*N+i], qubit_mapping.mapping_LtoP[unit2*N+i])


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
def twOxN_qft(if_mix_qaoa, qubit_mapping, qft_unit_offset, qaoa_unit_offset):
    # this function generates the quantum circuit for a 2xN QFT from the paper toqm Fig. 13(c)
    # each qubit in this pattern is logical qubit, you need to convert it to physical qubit using the mapping!!!!!
    bipartite_all_to_all = []
    
    start = 0 # start is used to control the starting index of unit.
    unit_size = qubit_mapping.unit_size
    offset_qft = qft_unit_offset * unit_size


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
                physical_q1 = qubit_mapping.mapping_LtoP[j+offset_qft]
                physical_q2 = qubit_mapping.mapping_LtoP[2*i-j+offset_qft]
                print(f'QFT-SWAP( q[{j+offset_qft}], q[{2*i-j+offset_qft}] ) = SWAP( Q[{physical_q1}], Q[{physical_q2}] )')

                qubit_mapping.SWAP_gate_implementation(physical_q1, physical_q2)
                #insert QAOA SWAP here:
                if if_mix_qaoa and only_one_cycle:
                    if qaoa_cycle > 2*unit_size:
                        continue
                    # print(f'start_position is {qaoa_start_position}')
                    # TODO: add more intra-unit swap for other unit here.
                    qaoa_gates_sequence(qaoa_start_position, 'SWAP', qubit_mapping, qaoa_unit_offset)
                    only_one_cycle = False

        print("-----------------")
        for j in range(i):
            if j < n and (2*i-j) < n:
                print(f'loop2: CX( q[{j+offset_qft}], q[{2*i-j+offset_qft}] )')
        print("-----------------")

        only_one_cycle = True
        for j in range(i+1):
            if j < n and (2*i+1-j) < n:
                print(f'loop3: CX( q[{j+offset_qft}], q[{2*i+1-j+offset_qft}] )')
                
                #insert QAOA cphase here:
                # insert interactions between 2xN pattern and QAOA pattern
                # TODO: add more inter-unit cphase for other unit here.
                if if_mix_qaoa and only_one_cycle:
                    for physical_q in range(unit_size, 2*unit_size):
                        # those operations always happen between the second and the third unit. Hard coded here. No need offset.
                        # for example, unit0 = 0, 1, 2, 3; the interactions happen at physical qubits pair(4,8) (5,9)....
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
    result = twOxN_qft(if_mix_qaoa, qubit_mapping, 0, 2)
    print(f'number of interactions is {len(result)}')
    # LNN_qft(6)
    # qaoa_LNN(qubit_mapping.unit_size, qubit_mapping, unit_number=2)

    
if __name__ == "__main__":
    main()
    # LNN_qft_unit_base(6)