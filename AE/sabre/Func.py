from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.transpiler.passes import SabreSwap
from qiskit.circuit.library import QFT
import time


def qft_Func(arch, num_qubits, N):

    qc_qft = QFT(num_qubits=num_qubits, do_swaps=False, inverse=False, name='qft')

    # Decompose the QFT circuit
    decomposed_qft = qc_qft.decompose()
    # decomposed_qft.draw(output = 'text', filename = 'decomposed.pdf', fold = 400)

    # N*N (2-20)
    ## Depth  gate count(swap,cp)    

    coupling_map = []
    if arch == "2*N":
        # Row
        for i in range(2):
            for j in range(N-1):
                pos = i * N + j
                coupling_map.append([pos, pos+1])
                coupling_map.append([pos+1, pos])
        # Col
        for i in range(N):
            for j in range(1):
                pos = j * N + i
                coupling_map.append([pos, pos+N])
                coupling_map.append([pos+N, pos])
    elif arch == "N*N":
        # Row
        for i in range(N):
            for j in range(N-1):
                pos = i * N + j
                coupling_map.append([pos, pos+1])
                coupling_map.append([pos+1, pos])
        # Col
        for i in range(N-1):
            for j in range(N):
                pos = i * N + j
                coupling_map.append([pos, pos+N])
                coupling_map.append([pos+N, pos])
    elif arch == "sycamore":
        for step in range((int)((N-2)/2) + 1):   
            # intra  
            i = 0 + 2 * step * N
            for j in range(2*N - 1):
                pos = i + j
                coupling_map.append([pos, pos+1])
                coupling_map.append([pos+1, pos])
            # inter
            if i != 0:
                pos = i
                next = i
                for k in range(2*N - 1):
                    if k % 2 == 0:
                        next = pos-2*N+1  
                    else:
                        next = pos+2*N+1
                    coupling_map.append([pos, next])
                    coupling_map.append([next, pos])
                    pos = next
    elif arch == "heavy-hex":
        # first unit
        for j in range(4):
            coupling_map.append([j, j + 1])
            coupling_map.append([j + 1, j])

        # 2nd to Nth unit
        pos = 3
        for i in range(N - 1):
            coupling_map.append([pos, pos + 2]) # 3 5
            coupling_map.append([pos + 2, pos]) 
            pos += 1    # pos = 4
            for j in range(4):
                pos += 1
                coupling_map.append([pos, pos + 1]) # 5 6, 6 7, 7 8, 8 9
                coupling_map.append([pos + 1, pos])

    
            

        '''
        if N == 1:
            coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2],
                            [3,4],[4,3]]
        elif N == 2:
            coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2],[3,5],[5,3],[5,6],[6,5],[6,7],[7,6],[7,8],[8,7]
                            [3,4],[4,3],[8,9],[9,8]]
        elif N == 3:
            coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2],[3,5],[5,3],[5,6],[6,5],[6,7],[7,6],[7,8],[8,7],[8,10],[10,8][10,11],[11,10],[11,12],[12,11],[12,13],[13,12]
                            [3,4],[4,3],[8,9],[9,8],[13,14],[14,13]]
        elif N == 4:
            coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2],[3,5],[5,3],[5,6],[6,5],[6,7],[7,6],[7,8],[8,7],[8,10],[10,8][10,11],[11,10],[11,12],[12,11],[12,13],[13,12],[13,15],[15,13],[15,16],[16,15],[16,17],[17,16],[17,18],[18,17]
                            [3,4],[4,3],[8,9],[9,8],[13,14],[14,13],[18,19],[19,18]]
        '''
        
    

    # print("\nThe Physical circuit coupling map is:\n", coupling_map)

    

    # Use the decomposed circuit in the transpile function
    start_time = time.time()
    sabre_circuit = transpile(decomposed_qft, backend=AerSimulator(),
                            coupling_map=coupling_map,
                            seed_transpiler=1,    # Sets random seed for the stochastic parts of the transpiler
                            optimization_level=0, # How much optimization to perform on the circuits.
                            layout_method='sabre',
                            routing_method='sabre',
                            basis_gates=['swap', 'cx', 'cp', 'u'])
    end_time = time.time()

    compilation_time = end_time - start_time
    print(f'\nCompilation time is {compilation_time} s')
    # sabre_circuit.draw(output='mpl', filename='compiled_output.pdf', fold=4000)
    # sabre_circuit.qasm(filename="compiled_qasm.qasm")
    print(f'\nDepth: {sabre_circuit.depth()}\ngate count: {sabre_circuit.count_ops()}\n')

    # res = {'arch': arch, 'num_qubits': num_qubits, 'scale': N, 'compilation_time': compilation_time, 'depth': sabre_circuit.depth(), 'swap': sabre_circuit.count_ops()['swap'], 'cp': sabre_circuit.count_ops()['cp']}
    res = {'arch': arch, 'num_qubits': num_qubits, 'scale': N, 'compilation_time': compilation_time, 'depth': sabre_circuit.depth(), 'swap': sabre_circuit.count_ops()['swap']}

    print(res)

    return res
