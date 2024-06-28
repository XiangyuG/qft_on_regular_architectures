import sys
import csv
from Func import qft_Func
import qiskit


if len(sys.argv) != 4:
		print("Please enter arguments, the format should be:")
		print("python3 main.py [arch type] [N] [number of qubits]")
		print("Types: 2*N, N*N, sycamore, heavy-hex")
		sys.exit(1)

arch = sys.argv[1]
# arch = "N*N"
N = int(sys.argv[2])
num_qubits = int(sys.argv[3])

# if arch == "heavy-hex":
# 	num_qubits = N * 5
# elif arch == "2*N":
#     num_qubits = N * 2
# else:
# 	num_qubits = N * N

res = qft_Func(arch, num_qubits, N)

# print(qiskit.__version__)