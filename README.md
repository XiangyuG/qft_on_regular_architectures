# qft_on_regular_architectures
This is the AD/AE for the paper (Optimizing Quantum Fourier Transformation (QFT)  Kernels  for Modern NISQ and FT Architectures)

## Part 1: Output the qubit mapping by generating the gate execution order in different architectures:
NISQ: Google Sycamore
```
python3 Googlesycamore_qft.py <the value of m for m*m grid>
```

NISQ: IBM Heavy-hex
```
python3 heavy_hex_qft.py <# qubits in the main row>
```

Fault Tolerant: Lattice sugery
```
python3 lattice_sugery_qft_mix.py <an even value of #units > <bool: 1, output circuit; 0 do not output circuit>
```

## Part 2: Reproduce the figure in our paper:
### To get the compiled program data in three different backends, just run following three commands (one for each architecture).
NISQ: Google Sycamore
```
python3 our_sycamore.py
```

NISQ: IBM Heavy-hex
```
python3 python3 our_heavy-hex.py
```

Fault Tolerant: Lattice sugery
```
python3 our_lattice_surgery.py
```

### Generate figures of different architectures (results will be saved in folder csv_data).
```
cd sabre
python3 sabre_qft.py "N*N"
python3 sabre_qft.py "sycamore"
python3 sabre_qft.py "heavy-hex"
```

### To do visualization you can implement the following code. 
```
cd ..
python3 draw_figures.py
```
The results will be stored in 6 pdf files (Heavyhex_Depth.pdf, Heavyhex_SWAP.pdf, Sycamore_Depth.pdf, Sycamore_SWAP.pdf, Lattice_surgery_Depth.pdf, Lattice_surgery_SWAP.pdf)

