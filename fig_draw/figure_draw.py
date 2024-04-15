import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter
import sys

# Define a function for y-axis tick label formatting
def sci_notation_yaxis(tick_val, pos):
    tick_len = len(str(tick_val))
    if tick_val != 0:
        return f'{(int)(tick_val / (10**(tick_len - 1)))}e{tick_len-1}'
    else:
        return '0'


# Set up the formatter
formatter = ScalarFormatter(useMathText=True)  # This will enable the mathematical text styling for scientific notation
formatter.set_scientific(True)  # Enable scientific notation
formatter.set_useOffset(False)  # Disable offset




# Check if the correct number of arguments are provided
if len(sys.argv) != 5:
    print("Usage: python3 figure_draw.py <arch type: N*N / Sycamore / Heavy-hex / Lattice Surgery> <our_csv_path> <sabre_csv_path> <column_name:depth or swap>")
    sys.exit(1)

# Assign variables from command-line arguments
arch, our_csv_path, sabre_csv_path, column_name = sys.argv[1:5]
lnn_csv_path = '../csv_data/lnn_lattice_surgery.csv'

# Font and axis settings with bold fontweight
fontsize = {'label': 30, 'axis': 27, 'title': 35}
fontweight = 'bold'  # Define font weight as bold

# Assign axis
x_start_pos = 0


# Read the CSV files into DataFrames
df1 = pd.read_csv(our_csv_path)
df2 = pd.read_csv(sabre_csv_path)
df_lnn = pd.read_csv(lnn_csv_path)

# Merge the two dataframes on the 'num_qubits' column to align them side by side
merged_df_12 = pd.merge(df1, df2, on='num_qubits', suffixes=('_our_approach', '_sabre'))
# print(merged_df_12)
# print(df_lnn)
merged_df = merged_df_12
if arch == 'Lattice_Surgery':
    merged_df = pd.merge(merged_df_12, df_lnn, on='num_qubits')
print(merged_df)

# Plotting
plt.figure(figsize=(10, 7))
# plt.plot(merged_df['num_qubits'], merged_df[column_name + '_our_approach'], label='Our approach', marker='s', color='blue', linestyle='', markersize=8)
# plt.plot(merged_df['num_qubits'], merged_df[column_name + '_sabre'], label='Sabre', marker='o', color='orange', linestyle='', markersize=8)
plt.plot(merged_df['num_qubits'], merged_df[column_name + '_our_approach'], label='Our approach', marker='s', color='blue', markersize=9.5, alpha=0.85, linewidth=4.5)
plt.plot(merged_df['num_qubits'], merged_df[column_name + '_sabre'], label='Sabre', marker='o', color='orange', markersize=9.5, alpha=0.9, linewidth=4.5)
if arch == 'Lattice_Surgery':
    plt.plot(merged_df['num_qubits'], merged_df[column_name], label='LNN', marker='o', color='green', markersize=8, alpha=0.85, linewidth=3)

# Set y-axis to use custom scientific notation
# plt.gca().yaxis.set_major_formatter(FuncFormatter(sci_notation_yaxis))
# plt.ticklabel_format(style='sci')
plt.gca().yaxis.set_major_formatter(formatter)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))


# Get the current exponent value from the y-axis OffsetText
# exponent_text = plt.gca().get_yaxis().get_offset_text()
# print(exponent_text)
# len_0 = len(str(exponent_text[0])) - 4
# Hide the original exponent
plt.gca().get_yaxis().get_offset_text().set_visible(False)
# Add a new exponent text with increased font size at the desired position
# plt.text(0.9, 0.9, f'1e{len_0}', fontsize=20, verticalalignment='top', horizontalalignment='left', transform=plt.gca().transAxes)



xticks = range(0, (int)(max(merged_df['num_qubits']) / 10) * 10 + 10, 10)
y_max_len = (int)(max(max(merged_df[column_name + '_sabre']), max(merged_df[column_name + '_our_approach'])) / 1000 * 1000) + 500
yticks = range(0, y_max_len, (int)((int)(y_max_len/5) / 1000) * 1000 + 500)
if arch == 'Lattice_Surgery':
    xticks = range(100, max(merged_df['num_qubits']) + 100, 300)
    x_start_pos = 50
    if column_name == 'swap':
        yticks = range(0, y_max_len, (int)((int)(y_max_len/5) / 10000) * 10000 + 20000)
    elif column_name == 'depth':
        yticks = range(0, y_max_len, (int)((int)(y_max_len/5) / 10000) * 10000 + 10000)
plt.xticks(xticks, fontsize = fontsize['axis'], fontweight=fontweight)   # number of x-axis
# plt.xlim(x_start_pos, max(merged_df['num_qubits']) + (3 if arch != 'Lattice_Surgery' else 20))  # Set x limits to be explicit about the range
plt.xlim(left=x_start_pos)
plt.yticks(yticks, fontsize=fontsize['axis'], fontweight=fontweight)                # number of y-axis
plt.ylim(bottom=-(y_max_len/50))

# plt.title('Comparison on ' + arch +  ' Between Our Approach and Sabre', fontsize=20)





# Set labels

plt.xlabel('# qubits', fontsize=fontsize['label'], fontweight=fontweight)
len_0 = len((str)(max(max(merged_df[column_name + '_sabre']), max(merged_df[column_name + '_our_approach'])))) - 1
if column_name == "depth":
    plt.ylabel(f'Depth(1e{len_0})', fontsize=fontsize['label'], fontweight=fontweight)
elif column_name == "swap":
    plt.ylabel(f'# SWAPs(1e{len_0})', fontsize=fontsize['label'], fontweight=fontweight)





plt.legend(prop={'weight': fontweight, 'size': fontsize['title']})
# plt.grid(True)
plt.tight_layout()

# Save the plot to a file. Replace 'output_plot.png' with your desired file path and name.
plt.savefig(column_name + '.png')
print('Comparison on ' + arch +  ' Between Our Approach and Sabre')
# Display the plot
plt.show()





# import sys
# import pandas as pd
# import matplotlib.pyplot as plt

# # Check for the correct number of command-line arguments
# if len(sys.argv) != 5:
#     print("Usage: python3 figure_draw.py <arch type: N*N / Sycamore / Heavy-hex / Lattice Surgery> <our_csv_path> <sabre_csv_path> <column_name: depth or swap>")
#     sys.exit(1)

# # Assign command-line arguments to variables
# arch, our_csv_path, sabre_csv_path, column_name = sys.argv[1:5]

# # Fontsize and axis configuration
# fontsize = {'label': 30, 'axis': 27, 'title': 35}
# x_start_pos = 0

# # Load data from CSV files into Pandas DataFrames
# our_data = pd.read_csv(our_csv_path)
# sabre_data = pd.read_csv(sabre_csv_path)

# # Merge DataFrames on the 'num_qubits' column
# merged_data = pd.merge(our_data, sabre_data, on='num_qubits', suffixes=('_our', '_sabre'))

# # Plotting
# plt.figure(figsize=(10, 6))
# plt.plot(merged_data['num_qubits'], merged_data[column_name + '_our'], label='Our approach', marker='s', color='blue', markersize=6, alpha=0.8)
# plt.plot(merged_data['num_qubits'], merged_data[column_name + '_sabre'], label='Sabre', marker='o', color='orange', markersize=6, alpha=0.8)

# # Axis labels and ticks configuration
# plt.xlabel('# qubits', fontsize=fontsize['label'])
# ylabel = 'Depth' if column_name == "depth" else '# SWAPs'
# plt.ylabel(ylabel, fontsize=fontsize['label'])

# # X-axis and Y-axis tick adjustment
# max_qubits = merged_data['num_qubits'].max()
# y_max = max(merged_data[column_name + '_sabre'].max(), merged_data[column_name + '_our'].max())
# xticks_interval = 10 if arch != 'Lattice_Surgery' else 300
# xticks = range(0, (int(max_qubits / xticks_interval) + 1) * xticks_interval, xticks_interval)
# y_max_adjusted = (int(y_max / 1000) + 1) * 1000
# yticks_interval = (int(y_max_adjusted / 5) / 1000) * 1000 + 500
# yticks = range(0, y_max_adjusted, int(yticks_interval))
# if arch == 'Lattice_Surgery':
#     xticks = range(100, max_qubits + 300, 300)
#     x_start_pos = 50
#     if column_name == 'swap':
#         yticks_interval = (int(y_max_adjusted / 5) / 10000) * 10000 + 20000
#         yticks = range(0, y_max_adjusted + 500, (int)(yticks_interval))
#     elif column_name == 'depth':
#         yticks_interval = (int(y_max_adjusted / 5) / 10000) * 10000 + 20000
#         yticks = range(0, y_max_adjusted + 500, (int)(yticks_interval))

# plt.xticks(xticks, fontsize=fontsize['axis'])
# plt.xlim(x_start_pos, max_qubits + 20)
# plt.yticks(yticks, fontsize=fontsize['axis'])
# plt.ylim(bottom=-(y_max_adjusted / 50))

# # Legend and layout adjustments
# plt.legend(fontsize=fontsize['title'])
# plt.tight_layout()

# # Output and display plot
# output_filename = f"{column_name}.png"
# plt.savefig(output_filename)
# print(f'Comparison on {arch} Between Our Approach and Sabre saved as {output_filename}')
# plt.show()
