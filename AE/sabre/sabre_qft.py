import sys
import csv
from Func import qft_Func


'''
# Arguments
print("\nThere are",len(sys.argv),"arguments in total: ", str(sys.argv))

arch = str(sys.argv[1])
N = int(sys.argv[2])
num_qubits = N * N
print("Arch: ", arch)
print("Scale: ", N, "*", N)
'''

arch = str(sys.argv[1])

if arch == "N*N":
    arch = "N*N"
    with open('../csv_data/sabre_N*N.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['arch', 'num_qubits','scale', 'compilation_time', 'depth', 'swap'])
        for i in range(4, 28, 4):      # arch = "N*N"
            N = i                   # arch = "N*N"
            num_qubits = N * N
            res = qft_Func(arch, num_qubits, N)
            data = [res['arch'], res['num_qubits'], res['scale'], res['compilation_time'], res['depth'], res['swap']]
            writer.writerow(data)
            

if arch == "sycamore":
    arch = "sycamore"
    with open('../csv_data/sabre_sycamore.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['arch', 'num_qubits','scale', 'compilation_time', 'depth', 'swap'])
        for i in range(2, 6):      # arch = sycamore
            N = i * 2               # arch = sycamore
            num_qubits = N * N
            res = qft_Func(arch, num_qubits, N)
            data = [res['arch'], res['num_qubits'], res['scale'], res['compilation_time'], res['depth'], res['swap']]
            writer.writerow(data)


if arch == "heavy-hex":
    arch = "heavy-hex"
   
    with open('../csv_data/sabre_heavy-hex_100.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['arch', 'num_qubits','scale', 'compilation_time', 'depth', 'swap'])
       
        for i in range(1,21):
            print(i)
            N = i
            num_qubits = N * 5
            res = qft_Func(arch, num_qubits, N)
            data = [res['arch'], res['num_qubits'], res['scale'], res['compilation_time'], res['depth'], res['swap']]
            writer.writerow(data)

        









# Apendix

## 2*2
# coupling_map = [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 0], [0, 3]] 

## 3*3
'''
0 1 2
3 4 5
6 7 8
'''
# coupling_map = [[0, 1], [1, 0], [1, 2], [2, 1], 
#                 [3, 4], [4, 3], [4, 5], [5, 4],
#                 [6, 7], [7, 6], [7, 8], [8, 7],
#                 [0, 3], [3, 0], [3, 6], [6, 3],
#                 [1, 4], [4, 1], [4, 7], [7, 4],
#                 [2, 5], [5, 2], [5, 8], [8, 5]
#                 ] 


# google —— 20*20

## google 2*2 
'''
0       2
    1       3
'''
# coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2]]

## google 4*4 
'''
0       2       4       6
    1       3       5       7
8       10      12      14     
    9       11      13      15
'''
# coupling_map = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2],[3,4],[4,3],[4,5],[5,4],[5,6],[6,5],[6,7],[7,6],
#                 [8,9],[9,8],[9,10],[10,9],[10,11],[11,10],[11,12],[12,11],[12,13],[13,12],[13,14],[14,13],[14,15],[15,14],
#                 [1,8],[8,1],[1,10],[10,1],[3,10],[10,3],[3,12],[12,3],[5,12],[12,5],[5,14],[14,5],[7,14],[14,7]
#                 ]
