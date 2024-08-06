import csv

alg = 'our'
# alg = 'lnn'
max_m = 32

# Function to calculate depth based on the given formula
def calculate_depth(m, alg):
    if alg == 'our':
        return 5*m**2 - 1.5*m - 9
    elif alg == 'lnn':
        ori_depth = 4*m**2 - 6
        slow_swap_cycle = 3
        quick_swap_cycle = 1
        all_quick_swap_cycle = 2 * (2 * m - 1)    # cycles before meet the first slow swap

        quick_depth = 0.5 * ori_depth + all_quick_swap_cycle
        slow_depth = ori_depth - quick_depth
        return quick_depth * quick_swap_cycle + slow_depth * slow_swap_cycle

# Function to calculate SWAP based on the given formula
def calculate_swap(m, alg):
    if alg == 'our':
        # return m*m*m*m/2 + 0.75*m*m*m - 2*m*m
        return (m**4)/4 + (m**3)/4 - 0.5*(m**2)
    elif alg == 'lnn':
        return 0.5 * (m**4 + m**3 - m**2 - m)
    

# List of m values for which to calculate depth and SWAP
m_values = []
for i in range(4, max_m + 2, 2):
    m_values.append(i)

# Specify the CSV file path where the results will be saved
csv_file_path = f'csv_data/{alg}_lattice_surgery.csv'

# Fieldnames for the CSV
fieldnames = ['num_qubits', 'scale', 'depth', 'swap']

# Write the data to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for m in m_values:
        depth = calculate_depth(m, alg=alg)
        swap = calculate_swap(m, alg=alg)
        writer.writerow({'num_qubits': m * m, 'scale': m, 'depth': depth, 'swap': swap})

print(f"Data has been written to {csv_file_path}")
