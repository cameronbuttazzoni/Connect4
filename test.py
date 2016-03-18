board = [['', '', '', '', '', '', ''],
         ['', '', '', '', '', '', ''],
         ['', '', '', '', '', '', ''],
         ['X', '', '', '', '', '', ''],
         ['X', '', '', '', '', '', ''],
         ['X', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '']]
CONNECT_NUM = 4
def check_double(piece, x, y=0):
    board[x][y] = piece
    win_count = 0
    count = 0
    f_flag = False #If True, already found one winning move
    flag = False #If True, already counting empty in count count
    emp_dist = 0 #distance away from empty space used in last win
    for a in range(2*CONNECT_NUM-1):
        print(a-1, x-CONNECT_NUM+a, count, f_flag, flag, emp_dist)
        if x-CONNECT_NUM+1+a < 0:
            continue
        if x-CONNECT_NUM+1+a >= 7:
                break
        new_piece = board[x-CONNECT_NUM+1+a][y]
        if new_piece == piece:
            count += 1
        elif not flag and new_piece == '':
            count += 1
            flag = True
        elif new_piece == '' and flag:
            emp_dist = 0
            if count > 1:
                if board[x-CONNECT_NUM+a][y] == piece:
                    count = 2
                    if board[x-CONNECT_NUM-1+a][y] == piece:
                        count = 3
            else:
                count = 1
        else:
            count = 0
            flag = False
        if flag:
            emp_dist += 1 #need to be CONNET_NUM-1 away
        if count == CONNECT_NUM:
            win_count += 1
            f_flag = True
        elif f_flag and count > CONNECT_NUM:
            if x-CONNECT_NUM+2+a >= 7: #require next piece ours
                break
            if board[x-CONNECT_NUM+2+a][y] in (piece, ''):
                win_count += 1
        elif f_flag and emp_dist == (CONNECT_NUM-1):
            if x-CONNECT_NUM+2+a >= 7: #require next piece ours
                break
            if board[x-CONNECT_NUM+2+a][y] == piece:
                win_count += 1
    print(win_count)
    return

check_double('X', 3)
