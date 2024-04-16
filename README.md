# qft_on_regular_architectures
This is the AD/AE for the paper (Optimizing Quantum Fourier Transformation (QFT)  Kernels  for Modern NISQ and FT Architectures)

## Verify the correctness and output the gate execution order in different architectures:
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
python3 lattice_sugery_qft_mix.py <# rows> <# column>
```




