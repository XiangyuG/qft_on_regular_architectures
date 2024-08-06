import sys
# import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class mapping:
    def __init__(self, unit_size, unit_count, mapping_LtoP, mapping_PtoL):
        self.mapping_LtoP = mapping_LtoP
        self.mapping_PtoL = mapping_PtoL
        self.unit_size = unit_size
        self.unit_LtoP = {}
        self.unit_PtoL = {}
        self.circuit = []
        self.cphase_count = 0

        assert unit_count % 2 == 0, 'unit count has to be an even number!'

        self.unit_count = unit_count

    
    def setup_initial_mapping(self):
        # this function sets up the initial mapping for NxN lattice
        # N is the number of qubit in one unit.
        N = self.unit_size
        # print(self.unit_count)
        # unit_count_half = self.unit_count//2
        physical_index = 0

        for i in range(0, self.unit_count, 2):
            start = i * N #this is the logical index of the first qubit in the i-th unit
            #first row
            for j in range(start, start+2*N, 2):
                self.mapping_PtoL[physical_index] = j
                self.mapping_LtoP[j] = physical_index
                # # print(f'physical_index is {physical_index}, j is {j}')
                physical_index += 1
            
            #second row
            for j in range(start+1, start+ 2*N, 2):
                self.mapping_PtoL[physical_index] = j
                self.mapping_LtoP[j] = physical_index
                # # print(f'physical_index is {physical_index}, j is {j}')
                physical_index += 1
        # initlize the unit mapping
        for i in range(0, self.unit_count):
            self.unit_LtoP[i] = i
            self.unit_PtoL[i] = i


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
        self.circuit.append(f'SWAP( Q[{physical_q1}], Q[{physical_q2}] )')


    def logical_unit_swap(self, logical_u1, logical_u2):
        # this function swaps two logical units in the qubit_mapping
        # offset is added in this function
        physical_u1 = self.unit_LtoP[logical_u1]
        physical_u2 = self.unit_LtoP[logical_u2]
        
        N = self.unit_size
        for i in range(N):
            self.SWAP_gate_implementation(physical_u1*N+i, physical_u2*N+i)
        self.unit_LtoP[logical_u1] = physical_u2
        self.unit_LtoP[logical_u2] = physical_u1
        self.unit_PtoL[physical_u1] = logical_u2
        self.unit_PtoL[physical_u2] = logical_u1

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

    # print('--------------- Getting unit base LNN QFT......')
    #preparing the original qft
    unit_operation_sequnece = {}
    step = 0
    for m in range(0, 4*n-6, 2):
        k = (m//2)+1
        i = 0
        operations = []
        while i < k - i:
            if i < n and k-i < n:
                # # print(f'CX( q[{i}], q[{k-i}] )')
                operations.append((i, k-i))
            i += 1
        unit_operation_sequnece[f'CX{step}'] = operations
        step += 1
        
        i = 0
        operations = []
        while i < k - i:
            if i < n and k-i < n:
                # # print(f'SWAP( q[{i}], q[{k-i}] )')
                operations.append((i, k-i))
            i += 1
        unit_operation_sequnece[f'SWAP{step}'] = operations
        step += 1
    # # print(unit_operation_sequnece)

    # Convert original qft to make every two layers of SWAP are performed together
    # Convert the dictionary to a list of tuples for easier manipulation
    steps_list = list(unit_operation_sequnece.items())
    # # print(steps_list)
    # Iterate through the steps and swap the order of every second SWAP with its preceding CX
    for i in range(len(steps_list)):
        if 'SWAP' in steps_list[i][0] and int(steps_list[i][0].replace('SWAP', '')) % 4 == 3:
            # Check if the previous step is a CX step
            if i > 0 and 'CX' in steps_list[i-1][0]:
                # Swap the current SWAP step with the previous CX step
                steps_list[i-1], steps_list[i] = steps_list[i], steps_list[i-1]

    # Convert the list of tuples back to a dictionary
    output = dict(steps_list)
    # print('(All numbers are logical unit index)')
    # print(output)
    return output

def qaoa_gates_sequence(start_position, gate_type, qubit_mapping, logical_unit_number):
    # this is a sequence of intra-unit parallel swap/cphase gates depends on gate_type

    N = qubit_mapping.unit_size
    assert start_position != 0 or start_position != 1, 'start_position has to be 0 or 1!'
    offset = N * qubit_mapping.unit_LtoP[logical_unit_number]
    s = []
    for i in range(start_position+offset, N+offset, 2):
        if i+1 >= N+offset:
            # i guess here is to skip the last gate using qubit out of the unit
            continue
        if gate_type == 'cphase':
            print(f'')
            # print(f'cphase( q[{i}], q[{i+1}] ) = cphase( q[{qubit_mapping.mapping_LtoP[i]}], q[{qubit_mapping.mapping_LtoP[i+1]}] )')
        elif gate_type == 'SWAP':
            # # print(f'QAOA-SWAP( Q[{qubit_mapping.mapping_LtoP[i]}], Q[{qubit_mapping.mapping_LtoP[i+1]}] )')
            qubit_mapping.SWAP_gate_implementation(i, i+1)
            s.append(f'SWAP( Q[{i}], Q[{i+1}] )')
    # print(f'qaoa-intra-unit-logical-{logical_unit_number}-{gate_type}: {s}')


def qaoa_2D(qubit_mapping, unit_pair_list):
    def bfs(node, visited, graph, units_start, start):
        # start is the qubit start postion in the unit
    # BFS to decide the start position of each unit
    # start position has to be alternating
        queue = deque([(node, start)])  # Initialize the queue with the starting node and start value
        while queue:
            current_node, current_start = queue.popleft()
            if current_node not in visited:
                visited.add(current_node)
                units_start[current_node] = current_start
                next_start = 1 - current_start  # Alternate the start value for neighbors
                
                for neighbor in graph[current_node]:
                    if neighbor not in visited:
                        queue.append((neighbor, next_start))
    # unit_pair_list contains logical units
    # Create the Adjacency List for BFS
    unit_neighbor = {}
    for l in unit_pair_list:
        for u, v in l:
            if u not in unit_neighbor:
                unit_neighbor[u] = []
            if v not in unit_neighbor:
                unit_neighbor[v] = []
            unit_neighbor[u].append(v)
            unit_neighbor[v].append(u)


    # # print('swap is not needed in shorter list')
    # n steps in inter-unit cphase in longer list and n - 1 steps in intra-unit swap in longer list
    unit_size = qubit_mapping.unit_size
    
    for cycle in range(0, unit_size):
        c1 = []
        c2 = []
        # implement inter-unit cphase
        for unit_pair in unit_pair_list[0]:
            # unit number is the logical unit number not the physical unit number
            physical_u1 = qubit_mapping.unit_LtoP[unit_pair[0]]
            physical_u2 = qubit_mapping.unit_LtoP[unit_pair[1]]
            for i in range(unit_size):
                # be careful with the mapping here, logical qubits are placed 0 2 4 6 in a unit. 
                # # print(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
                qubit_mapping.circuit.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')   
                qubit_mapping.cphase_count += 1
                c1.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
        # print("-----------------")
        # print(f'inter-cphase-unit at U: {unit_pair_list[0]}')
        # print(f'c1 is {c1}')
        # print("-----------------")

        for unit_pair in unit_pair_list[1]:
            physical_u1 = qubit_mapping.unit_LtoP[unit_pair[0]]
            physical_u2 = qubit_mapping.unit_LtoP[unit_pair[1]]
            for i in range(unit_size):
                # # print(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
                qubit_mapping.circuit.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
                qubit_mapping.cphase_count += 1
                c2.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
        # print(f'inter-cphase-unit at U: {unit_pair_list[1]}')
        # print(f'c2 is {c2}')

        # print("-----------------")
        # implement intra-unit swap
        '''It is better to use queue to implement the swap here using info in unit_neighbor'''
        # Implement BFS to Visit Each Node Once
        bfs_start_node = unit_pair_list[0][0][0]
        visited = set()
        units_start = {}
        start = cycle%2
        bfs(bfs_start_node, visited, unit_neighbor, units_start, start)
        # print(f'swap unit list{unit_pair_list}')
        # print(f'units_start is {units_start}')
        # print(f'bfs_start_node is {bfs_start_node}')
        for key in unit_neighbor:
            physical_u = qubit_mapping.unit_LtoP[key]
            # print(f'intra-swap-unit at U: physical_u={physical_u}, logical_u={key}')
            qaoa_gates_sequence(units_start[key], 'SWAP', qubit_mapping, key)

    
def qaoa_LNN(N, qubit_mapping, physical_unit_number = 0):
    #this is a qaoa pattern in LNN architecture
    #TODO: mapping is not updated in this version
    # print(f'unit_size is {N}')
    # print(f'unit_size is {physical_unit_number}')

    for cycle in range(0, 2*N-2+1, 4):
        # print(f'cycle {cycle}')
        qaoa_gates_sequence(0, 'cphase', qubit_mapping, physical_unit_number)
        # print("-----------------")
        qaoa_gates_sequence(1, 'SWAP', qubit_mapping, physical_unit_number)
        # print("-----------------")
        qaoa_gates_sequence(1, 'cphase', qubit_mapping, physical_unit_number)
        # print("-----------------")
        qaoa_gates_sequence(0, 'SWAP', qubit_mapping, physical_unit_number)
        # print("-----------------")

def find_path(pairs, head):
    def bfs(bfs_start_node, visited, graph):
    # BFS to decide the start position of each unit
    # start position has to be alternating
        path = [bfs_start_node]
        queue = deque([bfs_start_node])  # Initialize the queue with the starting node and start value
        while queue:
            current_node = queue.popleft()
            if current_node not in visited:
                visited.add(current_node)
                
                for neighbor in graph[current_node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        path.append(neighbor)
        return path
    # Create the Adjacency List for BFS
    graph = {}
    # # print(pairs)
    for l in pairs:
        for u, v in l:
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u)

    # BFS to find the path
    # Implement BFS to Visit Each Node Once
    bfs_start_node = head
    visited = set()
    path = bfs(bfs_start_node, visited, graph)

    return path
def generate_unit_pairs_cphase(lst):
    # Generate the first list of pairs starting at index 0
    first_list = []
    for i in range(0, len(lst) - 1, 2):
        if i + 1 < len(lst):
            first_list.append((lst[i], lst[i + 1]))

    # Generate the second list of pairs starting at index 1
    second_list = []
    for i in range(1, len(lst) - 1, 2):
        if i + 1 < len(lst):
            second_list.append((lst[i], lst[i + 1]))

    return first_list, second_list

def twOxN_qft(if_mix_qaoa, qubit_mapping, qft_unit_offset, qaoa_unit_offset, unit_interaction_list):
    # this function generates the quantum circuit for a 2xN QFT from the paper toqm Fig. 13(c)
    # each qubit in this pattern is logical qubit, you need to convert it to physical qubit using the mapping!!!!!
    bipartite_all_to_all = []
    
    start = 0 # start is used to control the starting index within a unit.
    unit_size = qubit_mapping.unit_size
    offset_qft = qft_unit_offset * unit_size

    unit_order = []
    l1_start_0 = []#logical units in the list
    l2_start_1 = []#logical units in the list
    if if_mix_qaoa:
        # print('Implementing 2xN qft mix with a unit below it, a bipartite all-to-all qaoa pattern')
        # sort the unit_interaction_list to make the 'qft_unit_offset' unit is the first unit in the list
        # for example, unit_order = [2,3,1,4,0,5] in the paper, QFT paper Fig. 15
        unit_order = find_path(unit_interaction_list, qft_unit_offset)
        # print(f'unit_position is {unit_order}')
        # given the list, generate two lists of consecutive pairs to help generate inter-unit cphase
        # l1_start_0 = [(0,1), (2,3), (4,5)] l2_start_1 = [(1,2), (3,4), (5,0)]
        l1_start_0, l2_start_1 = generate_unit_pairs_cphase(unit_order)

    n = 2*unit_size
    qaoa_cycle = 0 # used to control the start posotion of intra-unit swap gates in qaoa pattern and stop qaoa pattern early.
    for i in range(start, start + n-2 + 1):
        
        #used to contrl qaoa part
        qaoa_start_position = (1+qaoa_cycle//2) % 2 # be careful with the start position, we need +1 cuz the first swap loop will be skipped.
        # if qaoa_cycle > 2*(unit_size-1): 
        #     if_mix_qaoa = False
        
        only_one_cycle = True # used to control the one cycle of qaoa pattern. Performing a sequence of parallel swap/cphase gates in one cycle.
        '''The following code contains three for loops correpsonding to the three steps in the paper,TOQM Fig. 14'''
        # a sequence of parallel swap gates in 2xN QFT, so we need only_one_cycle to control the qaoa pattern onl inserted once.
        # print(f'3cycles SWAP-{i} in 2xN QFT,(step2)')
        s = []
        for j in range(i):
            if j < n and (2*i-j) < n:
                physical_q1 = qubit_mapping.mapping_LtoP[j+offset_qft]
                physical_q2 = qubit_mapping.mapping_LtoP[2*i-j+offset_qft]
                # # print(f'QFT-SWAP( q[{j+offset_qft}], q[{2*i-j+offset_qft}] ) = SWAP( Q[{physical_q1}], Q[{physical_q2}] )')
                qubit_mapping.SWAP_gate_implementation(physical_q1, physical_q2)
                qubit_mapping.circuit.append(f'SWAP( Q[{physical_q1}], Q[{physical_q2}] )')
                s.append(f'SWAP( Q[{physical_q1}], Q[{physical_q2}] )')
                #insert QAOA SWAP here:
                if if_mix_qaoa and only_one_cycle:
                    if qaoa_cycle > 2*(unit_size):
                        # after 2*(unit_size-1) cycles, we not need to insert qaoa gates. so do not need swap gates.
                        # but we need to finish all mixed qft and qaoa part.
                        only_one_cycle = False
                        continue
                    # # print(f'start_position is {qaoa_start_position}')
                    # add more intra-unit swap for other unit here.
                    # # print('this is a mixed qaoa swap')
                    qaoa_gates_sequence(qaoa_start_position, 'SWAP', qubit_mapping, qubit_mapping.unit_PtoL[qaoa_unit_offset])
                    if len(unit_order) < 3:
                        raise ValueError('unit_order is not correct!  units number is worng!')
                    for u in range(3,len(unit_order)):
                        qaoa_start_position = 1-qaoa_start_position
                        qaoa_gates_sequence(qaoa_start_position, 'SWAP', qubit_mapping,qubit_mapping.unit_PtoL[u])
                    only_one_cycle = False
        # print(f'qft-swaps: {s}')
        qubit_mapping.circuit = qubit_mapping.circuit + s

        
        # print("-----------------")
        # this loop is for the third step in the paper, TOQM Fig. 14
        c = []
        # print(f'3cycles CX-{i} in 2xN QFT, loop2(step3)')
        for j in range(i):
            if j < n and (2*i-j) < n:
                # # print(f'loop2: CX( q[{j+offset_qft}], q[{2*i-j+offset_qft}] )')
                qubit_mapping.circuit.append(f'CX( q[{j+offset_qft}], q[{2*i-j+offset_qft}] )')
                qubit_mapping.cphase_count += 1
                c.append(f'CX( q[{j+offset_qft}], q[{2*i-j+offset_qft}] )')
        # print(f'qft-cx: {c}')
        
        
        # print("-----------------")
        # print(f'3cycles CX-{i} in 2xN QFT, loop3(step1)')
        only_one_cycle = True
        # this loop is for the first step in the paper, TOQM Fig. 14
        qft_cx = []
        qaoa_cx_0 = {} # used to store the inter-unit cphase for the even-odd unit
        qaoa_cx_1 = {} # used to store the inter-unit cphase for the odd-even unit
        for j in range(i+1):
            if j < n and (2*i+1-j) < n: # this if is used to control weather we enter the loop 3 or not. 
                # if we enter the loop 3, we need to insert qaoa gates.
                qft_cx.append(f'CX( q[{j+offset_qft}], q[{2*i+1-j+offset_qft}] )')
                #insert QAOA cphase here:
                # insert interactions between 2xN pattern and QAOA pattern
                # add more inter-unit cphase for other unit here.
                if if_mix_qaoa and only_one_cycle: # the loop is within a for loop of qft gates, so we only need to insert qaoa gates once.
                    # print(f'l2_start_1: {l2_start_1}')
                    # insert the inter-unit cphase for pairs of odd-even unit: (1,2) (3,4)...
                    qaoa_cx_at_unit = []
                        # this is the mixed qft and qaoa part. 
                    for physical_q in range(unit_size, 2*unit_size):
                        # those operations always happen between the second and the third unit. Hard coded here. No need offset.
                        # for example, unit0 = 0, 1, 2, 3; the interactions happen at physical qubits pair(4,8) (5,9)....
                        pair1 = (qubit_mapping.mapping_PtoL[physical_q], qubit_mapping.mapping_PtoL[physical_q+ unit_size])
                        pair2 = (qubit_mapping.mapping_PtoL[physical_q+unit_size], qubit_mapping.mapping_PtoL[physical_q])
                        if (pair1 not in bipartite_all_to_all) and (pair2 not in bipartite_all_to_all):
                            bipartite_all_to_all.append(pair1)
                            # # print(pair1)
                            # qaoa_cx.append(f'qaoa: CX( q[{pair1[0]}], q[{pair1[1]}] )')
                            qaoa_cx_at_unit.append(f'cphase( q[{pair1[0]}], q[{pair1[1]}] )')
                    qaoa_cx_1[(qft_unit_offset+1, qubit_mapping.unit_PtoL[qaoa_unit_offset])] = qaoa_cx_at_unit
                    
                    if qaoa_cycle > 2*(unit_size-1):
                        # after 2*(unit_size-1) cycles, we not need to insert qaoa gates. so do not need swap gates.
                        # but we need to finish all mixed qft and qaoa part.
                        only_one_cycle = False
                        continue
                    
                        # this is the pure qaoa part.
                    for pair in l2_start_1[1:]:
                        qaoa_cx_at_unit = []
                        physical_u1 = qubit_mapping.unit_LtoP[pair[0]]
                        physical_u2 = qubit_mapping.unit_LtoP[pair[1]]
                        for i in range(unit_size):
                            qaoa_cx_at_unit.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
                        qaoa_cx_1[pair] = qaoa_cx_at_unit

                    # insert the inter-unit cphase for pairs of even-odd unit: (0,1) (2,3)...
                    # print(f'l1_start_0: {l1_start_0}')
                    for pair in l1_start_0[1:]:
                        qaoa_cx_at_unit = []
                        physical_u1 = qubit_mapping.unit_LtoP[pair[0]]
                        physical_u2 = qubit_mapping.unit_LtoP[pair[1]]
                        for i in range(unit_size):
                            qaoa_cx_at_unit.append(f'cphase( q[{qubit_mapping.mapping_PtoL[physical_u1*unit_size+i]}], q[{qubit_mapping.mapping_PtoL[physical_u2*unit_size+i]}] )')
                        qaoa_cx_0[pair] = qaoa_cx_at_unit

                    only_one_cycle = False
        # print(f'qft_cx: {qft_cx}')
        qubit_mapping.circuit = qubit_mapping.circuit + qft_cx
        qubit_mapping.cphase_count += len(qft_cx)
        if if_mix_qaoa:
            # print("-------")
            # print(f'qaoa_cx_0: {qaoa_cx_0}')
            for key in qaoa_cx_0:
                qubit_mapping.circuit = qubit_mapping.circuit + qaoa_cx_0[key]
                qubit_mapping.cphase_count += len(qaoa_cx_0[key])
            # print("-------")
            # print(f'qaoa_cx_1: {qaoa_cx_1}')
            for key in qaoa_cx_1:
                qubit_mapping.circuit = qubit_mapping.circuit + qaoa_cx_1[key]
                qubit_mapping.cphase_count += len(qaoa_cx_1[key])
        # print("-----------------")
        qaoa_cycle += 2

    return bipartite_all_to_all


def qft_lattice(n, mapping):
    '''
    n is the unit size and number of units
    '''
    circuit = []
    # getting united based qft pattern. units are logical units
    unit_pattern = LNN_qft_unit_base(n)
    keys = list(unit_pattern.keys())
    # # print(keys)

    # sort those operations, so we can iterate them in order and do the corresponding operations.
    # print(' ')
    # print('Putting two steps together:')
    unit_operations = {} # unit_opration = {qft0: [[(2,1)][(0,1)(2,3)]]}
    for i in range(len(unit_pattern.items())):   
        if ((i+1) >= len(unit_pattern)) and 'SWAP' in keys[i]:
            # Skip the last SWAP operation
            break
        if i == 0:
            unit_operations['qft0'] = unit_pattern[keys[i]]
            continue
        elif 'CX' in keys[i] and 'CX' in keys[i+1]:
            unit_operations[f'qft(step: {i},step: {i+1})'] = [unit_pattern[keys[i]], unit_pattern[keys[i+1]]]
            i = i + 1
        elif 'SWAP' in keys[i] and 'SWAP' in keys[i+1]:
            unit_operations[f'swap(step:{i},step:{i+1})'] = [unit_pattern[keys[i]], unit_pattern[keys[i+1]]]
            i = i + 1
    # print(unit_operations)
    # sys.exit()

    # in this loop, we can do the corresponding operations in the order of the sorted keys.
    # print('-------------Start generating the quantum circuit----------------')
    mix_step = 0
    for index, (key,item) in enumerate(unit_operations.items()):
        # print('')
        # print('---------------------------------------')
        # print(f' (Unit cycle: {index}, doing {key} ): ')
        if 'qft' in key:
            mix_tuple = (mix_step, mix_step+1)
            if (mix_tuple in item) or (len(item) == 2 and (mix_tuple in item[0] or mix_tuple in item[1])):
                # print(f'we do mix-qft here',key, item)
                if len(item) == 1:
                    # this is the first step AE(u0, u1)
                    # if number of unit is even, this if statement should be right. not sure about the odd number of units.
                    # print('non mixed-qft: this is the first step AE(u0, u1)')
                    twOxN_qft(False, mapping, mix_step, 0, item)
                else:
                    # print('mixed-qft: twOxN_qft(True)-check here later!!!!!!!!!!!!!!')
                    twOxN_qft(True, mapping, mix_step, 2, item) # 2 is the third physical unit 
                mix_step += 2
                
            else:
                # print(f'we do pure qaoa here', key,item)
                qaoa_2D(mapping, item)
          
        elif 'swap' in key:
            # print(f'we do logical unit swap here', key, item)
            for swap_step in item:
                # we only have two steps
                for swap_unit in swap_step:
                    # # print(f'SWAP unit: {swap_unit[0]}, {swap_unit[1]}')
                    mapping.logical_unit_swap(swap_unit[0], swap_unit[1])
    return circuit

def main(row, if_output_circuit):
    # N = 4 # N is the unit size
    # coupling_graph = nx.grid_2d_graph(N, N)
    # coupling_graph = nx.convert_node_labels_to_integers(coupling_graph)
    # # print(coupling_graph.edges)
    
    #setup initial mapping
    unit_count = unit_size = row

    # if len(sys.argv) > 1:
    #     unit_count = int(sys.argv[1])
    #     unit_size = int(sys.argv[2])
    # # print(f'unit_count is {unit_count}, unit_size is {unit_size}')

    mapping_LtoP = {}
    mapping_PtoL = {}
    qubit_mapping = mapping(unit_size, unit_count, mapping_LtoP, mapping_PtoL)
    qubit_mapping.setup_initial_mapping()
    # qubit_mapping.# print_mapping()
    if_mix_qaoa = True
    # result = twOxN_qft(if_mix_qaoa, qubit_mapping, 0, 2)
    # # print(f'number of interactions is {len(result)}')
    qft_lattice(unit_size, qubit_mapping)
    # print(f'Original circuit gates are: {(unit_size*unit_size-1+1)*(unit_size*unit_size-1)/2}')
    # print(f'Compiled circuit gates are: {qubit_mapping.cphase_count}')
    if if_output_circuit:
        # print(' ')
        # print('!!!!--------OUTPUTING CIRCUIT---------!!!!')
        
        print(qubit_mapping.circuit)
    # LNN_qft(6)
    # qaoa_LNN(qubit_mapping.unit_size, qubit_mapping, unit_number=2)

    
if __name__ == "__main__":
    row = 4
    if_output_circuit = 1
    if len(sys.argv) == 2:
        # Access command line arguments
        row = int(sys.argv[1])
    if len(sys.argv) == 3:
        row = int(sys.argv[1])
        if_output_circuit = int(sys.argv[1])
        
    main(row, if_output_circuit)
    # LNN_qft_unit_base(6)
