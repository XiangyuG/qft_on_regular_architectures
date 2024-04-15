from util import *
import sys

def reverse_LNN(pos, I, r1, N, swap_total):
    assert r1 % 2 == 0, "start from the wrong row number"
    total = N * 2
    for i in range(2 * total - 3):
        idx = N - 1
        if i % 2 == 0:
            # CPHASE + SWAP
            while 1:
                if idx < 0:
                    break
                cnode = pos[r1 + 1][idx]
                tnode = pos[r1][idx]
                # breakpoint()
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    # CPHASE
                    I[cnode][tnode] = 1
                    # SWAP
                    swap_total += 1
                    pos[r1 + 1][idx] = tnode
                    pos[r1][idx] = cnode
                    idx -= 1
                else:
                    break
        else:
            # CPHASE + SWAP
            while 1:
                if idx - 1 < 0:
                    break
                cnode = pos[r1][idx]
                tnode = pos[r1 + 1][idx - 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    # CPHASE
                    I[cnode][tnode] = 1
                    # SWAP
                    swap_total += 1
                    pos[r1][idx] = tnode
                    pos[r1 + 1][idx - 1] = cnode
                    idx -= 1
                else:
                    break
    return pos, I, swap_total

def LNN(pos, I, r1, N, swap_total):
    assert r1 % 2 == 0, "start from the wrong row number"
    total = N * 2
    for i in range(2 * total - 3):
        idx = 0
        # breakpoint()
        if i % 2 == 0:
            # CPHASE + SWAP
            while 1:
                if idx >= len(pos[0]):
                    break
                cnode = pos[r1][idx]
                tnode = pos[r1 + 1][idx]
                # breakpoint()
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    # CPHASE
                    I[cnode][tnode] = 1
                    # SWAP
                    swap_total += 1
                    pos[r1][idx] = tnode
                    pos[r1 + 1][idx] = cnode
                    idx += 1
                else:
                    break
        else:
            # CPHASE + SWAP
            while 1:
                if idx + 1 >= len(pos[0]):
                    break
                cnode = pos[r1 + 1][idx]
                tnode = pos[r1][idx + 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    # CPHASE
                    I[cnode][tnode] = 1
                    # SWAP
                    swap_total += 1
                    pos[r1 + 1][idx] = tnode
                    pos[r1][idx + 1] = cnode
                    idx += 1
                else:
                    break
        # print("curr I =", I)
    return pos, I, swap_total

'''Swap 2 units'''
def USWAP(pos, r1, swap_total):
    size = len(pos)
    # print("size =", size)
    # Step 1: swap r1 + 1 with r1 + 2
    # print("r1 =", r1, "before USWAP pos =", pos)
    swap_total += size
    for i in range(size):
        pos[r1 + 1][i], pos[r1 + 2][i] = pos[r1 + 2][i], pos[r1 + 1][i]
    # Step 2: swap r1 with r1 + 1; r1 + 2 with r1 + 3
    swap_total += size * 2
    for i in range(size):
        pos[r1][i], pos[r1 + 1][i] = pos[r1 + 1][i], pos[r1][i]
        pos[r1 + 2][i], pos[r1 + 3][i] = pos[r1 + 3][i], pos[r1 + 2][i]
    # Step 3: swap r1 + 1 with r1 + 2
    swap_total += size
    for i in range(size):
        pos[r1 + 1][i], pos[r1 + 2][i] = pos[r1 + 2][i], pos[r1 + 1][i]
    # print("after USWAP pos =", pos)
    return pos, swap_total

'''Inter-unit''' 
# TODO: finish the inter_u based on the current version at ASPLOS paper: allowing > 1 CPHASE
def INTER_U(pos, I, r1, swap_total):
    # print("Before inter, pos =", pos)
    size = len(pos)
    # Step 1 (a for loop):
    for j in range(size * 2 + 1):
        if j % 2 == 0:
            # CPHASE row r1 + 1 and row r1 + 2, Left CPHASE direction
            for i in range(size):
                cnode = pos[r1 + 1][i]
                tnode = pos[r1 + 2][i]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                else:
                    break
            # CPHASE row r1 + 1 and row r1 + 2, Right CPHASE direction
            for i in range(size - 1):
                cnode = pos[r1 + 1][i]
                tnode = pos[r1 + 2][i + 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                else:
                    break
            # SWAP row r1 and row r1 + 1, SWAP row r1 + 2 and row r1 + 3, start from 0
            if j < size * 2:
                swap_total += size
                for i in range(size):
                    pos[r1][i], pos[r1 + 1][i] = pos[r1 + 1][i], pos[r1][i]
                    pos[r1 + 2][i], pos[r1 + 3][i] = pos[r1 + 3][i], pos[r1 + 2][i]
        else:
            # CPHASE row r1 + 1 and row r1 + 2, Left CPHASE direction
            for i in range(size):
                cnode = pos[r1 + 1][i]
                tnode = pos[r1 + 2][i]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
            # CPHASE row r1 + 1 and row r1 + 2, Right CPHASE direction
            for i in range(size - 1):
                cnode = pos[r1 + 1][i]
                tnode = pos[r1 + 2][i + 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
            # SWAP row r1 and row r1 + 1, SWAP row r1 + 2 and row r1 + 3, start from 1
            if j < size * 2:
                swap_total += (size - 1)
                for i in range(1, size):
                    pos[r1][i], pos[r1 + 1][i - 1] = pos[r1 + 1][i - 1], pos[r1][i]
                    pos[r1 + 2][i], pos[r1 + 3][i - 1] = pos[r1 + 3][i - 1], pos[r1 + 2][i]
    # print("Before step 2 in inter, pos =", pos)
    # Step 2 (fix):
    # 1. SWAP row r1, r1 + 1
    swap_total += size
    for i in range(size):
        pos[r1][i], pos[r1 + 1][i] = pos[r1 + 1][i], pos[r1][i]
        
    # 2. CPHASE row r1 + 1 and row r1 + 2 Left CPHASE direction
    for i in range(size):
        cnode = pos[r1 + 1][i]
        tnode = pos[r1 + 2][i]
        if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
            I[cnode][tnode] = 1
    # 3. SWAP row r1 and row r1 + 1, row r1 + 2 and row r1 + 3
    swap_total += size * 2
    for i in range(size):
        pos[r1][i], pos[r1 + 1][i] = pos[r1 + 1][i], pos[r1][i]
        pos[r1 + 2][i], pos[r1 + 3][i] = pos[r1 + 3][i], pos[r1 + 2][i]

    # 4. CPHASE row r1 + 1 and row r1 + 2 Left CPHASE direction
    for i in range(size):
        cnode = pos[r1 + 1][i]
        tnode = pos[r1 + 2][i]
        if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
            I[cnode][tnode] = 1

    # 5. SWAP row r1 + 2 and row r1 + 3
    swap_total += size
    for i in range(size):
        pos[r1 + 2][i], pos[r1 + 3][i] = pos[r1 + 3][i], pos[r1 + 2][i]
    # print("After inter, pos =", pos)
    return pos, I, swap_total


# pdb.set_trace()
def main(argv):
    if len(argv) != 2:
        print("Usage: python3", argv[0], "<the value of m for m*m grid>")
        sys.exit(1)
    # Build the initial mapping of Google Sycamore
    N = int(argv[1])
    if N % 2 != 0:
        print("Please set m to be even number")
        sys.exit(1)
    pos = []
    for i in range(int(N / 2)):
        u_l = []
        d_l = []
        for j in range(i * N * 2, i * N * 2 + N * 2):
            if j % 2 == 0:
                u_l.append(j)
            else:
                d_l.append(j)
        pos.append(u_l)
        pos.append(d_l)
    up_pos = pos

    # Dependency 2D arrary
    I = []
    for i in range(N * N):
        l = []
        for j in range(N * N):
            l.append(0)
        I.append(l)
    
    # Dependency across units
    initial_pos = []
    for i in range(int(N / 2)):
        initial_pos.append(i)
    inter_unit_I = []
    for i in range(int(N / 2)):
        l = []
        for j in range(int(N / 2)):
            l.append(0)
        inter_unit_I.append(l)
    
    # Start QFT
    swap_total = 0
    total_depth = 0
    for i in range(N - 1):
        if i % 2 == 0:
            total_depth += 4 * 2 * N - 6
            if i % 4 == 0:
                up_pos, up_I, swap_total = LNN(up_pos, I, 0, N, swap_total)
            else:
                up_pos, up_I, swap_total = reverse_LNN(up_pos, I, 0, N, swap_total)
            for j in range(1, int(N/2) - 1, 2):
                cnode = initial_pos[j]
                tnode = initial_pos[j + 1]
                if cnode < tnode and OK_to_do_control(cnode, inter_unit_I) and inter_unit_I[cnode][tnode] == 0:
                    initial_pos[j], initial_pos[j + 1] = initial_pos[j + 1], initial_pos[j] 
                    inter_unit_I[cnode][tnode] = 1
                    up_pos, up_I, swap_total = INTER_U(up_pos, I, j * 2, swap_total) 
                    up_pos, swap_total = USWAP(up_pos, j * 2, swap_total) 
                else:
                    break
        else:
            total_depth += 3 * 2 * N + 5
            for j in range(0, int(N/2) - 1, 2):
                cnode = initial_pos[j]
                tnode = initial_pos[j + 1]
                if cnode < tnode and OK_to_do_control(cnode, inter_unit_I) and inter_unit_I[cnode][tnode] == 0:
                    initial_pos[j], initial_pos[j + 1] = initial_pos[j + 1], initial_pos[j] 
                    inter_unit_I[cnode][tnode] = 1
                    up_pos, up_I, swap_total = INTER_U(up_pos, I, j * 2, swap_total)
                    up_pos, swap_total = USWAP(up_pos, j * 2, swap_total) 
                else:
                    break
        # print("after i =", i, "initial_pos =", initial_pos)
    if check_qft_gates(I):
        final_print([], swap_total, total_depth)
if __name__ == '__main__':
    main(sys.argv)