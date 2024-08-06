def out_I(I):
    for i in range(len(I)):
        print("i =", i, "list =", I[i])
def final_print(up_pos, swap_total, total_depth):
    print("final pos =", up_pos)
    print("swap_total =", swap_total)
    print("total_depth =", total_depth)

'''Check whether all gates in QFT have been executed or not'''
def check_qft_gates(I):
    N = len(I)
    for i in range(N):
        for j in range(N):
            if i < j:
                if I[i][j] == 0:
                    print("i =", i, "j =", j)
                    print("False checking!!!")
                    return False
                else:
                    continue
            else:
                if I[i][j] == 1:
                    print("False checking!!!")
                    return False
                else:
                    continue
    print("Pass checking")
    return True

'''Check whether this cnode is OK or not to do CX gate over others'''
def OK_to_do_control(cnode, I):
    for i in range(cnode):
        if I[i][cnode] == 0:
            return False
    return True