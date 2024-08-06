import pandas as pd
import matplotlib.pyplot as plt

#########################---Heavy-Hex---#########################
#########################---depth---#########################

# Read the CSV files
our_hh = pd.read_csv('csv_data/our_heavy-hex.csv')
sabre_hh = pd.read_csv('csv_data/sabre_heavy-hex_100.csv')

# Extract the columns
x1 = our_hh['num_qubits']
y1 = our_hh['depth'] / 1000  # Normalize by 1000
x2 = sabre_hh['num_qubits']
y2 = sabre_hh['depth'] / 1000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('Depth (1e3)')
plt.title('Heavy-hex: Depth vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Heavyhex_Depth.pdf')
# plt.show()

#########################---swap---#########################
# Extract the columns
x1 = our_hh['num_qubits']
y1 = our_hh['swap'] / 1000  # Normalize by 1000
x2 = sabre_hh['num_qubits']
y2 = sabre_hh['swap'] / 1000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('SWAP (1e3)')
plt.title('Heavy-hex: SWAP vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Heavyhex_SWAP.pdf')
# plt.show()

#########################---Sycamore---#########################
#########################---depth---#########################

# # Read the CSV files
our_sycamore = pd.read_csv('csv_data/our_sycamore.csv')
sabre_sycamore = pd.read_csv('csv_data/sabre_sycamore.csv')

# Extract the columns
x1 = our_sycamore['num_qubits']
y1 = our_sycamore['depth'] / 1000  # Normalize by 1000
x2 = sabre_sycamore['num_qubits']
y2 = sabre_sycamore['depth'] / 1000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('Depth (1e3)')
plt.title('Sycamore: Depth vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Sycamore_Depth.pdf')
# plt.show()

#########################---swap---#########################
# Extract the columns
x1 = our_sycamore['num_qubits']
y1 = our_sycamore['swap'] / 1000  # Normalize by 1000
x2 = sabre_sycamore['num_qubits']
y2 = sabre_sycamore['swap'] / 1000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('SWAP (1e3)')
plt.title('Sycamore: SWAP vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Sycamore_SWAP.pdf')
# plt.show()

#########################---Lattice-Surgery---#########################
#########################---depth---#########################

# Read the CSV files
our_lattice_surgery = pd.read_csv('csv_data/our_lattice_surgery.csv')
sabre_lattice_surgery = pd.read_csv('csv_data/sabre_N*N.csv')

# Extract the columns
x1 = our_lattice_surgery['num_qubits']
y1 = our_lattice_surgery['depth'] / 10000  # Normalize by 1000
x2 = sabre_lattice_surgery['num_qubits']
y2 = sabre_lattice_surgery['depth'] / 10000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('Depth (1e4)')
plt.title('Lattice_surgery: Depth vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Lattice_surgery_Depth.pdf')
# plt.show()

#########################---swap---#########################
# Extract the columns
x1 = our_lattice_surgery['num_qubits']
y1 = our_lattice_surgery['swap'] / 100000  # Normalize by 1000
x2 = sabre_lattice_surgery['num_qubits']
y2 = sabre_lattice_surgery['swap'] / 100000  # Normalize by 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker='o', linestyle='-', label='Our approach')
plt.plot(x2, y2, marker='s', linestyle='--', label='Sabre')

# Add titles and labels
plt.xlabel('# qubits')
plt.ylabel('SWAP (1e5)')
plt.title('Lattice_surgery: SWAP vs. Number of Qubits')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig('Lattice_surgery_SWAP.pdf')
# plt.show()