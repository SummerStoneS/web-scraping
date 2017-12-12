import numpy as np

chess_board = np.zeros((11, 11))                        # 没棋子
chess_board[[1, 2, 3, 4, 5], 5] = 1                     # 黑棋子
chess_board[5, [1, 2, 3, 4]] = -1                       # 白棋子
chess_board[[4, 6, 3, 2, 5], [4, 5, 3, 2, 6]] = -1
chess_board[[1, 6, 4, 6], [1, 6, 6, 4]] = 1
current_status = (5, 5)                                 # 当前棋子的位置


class Chess(object):
    def __init__(self, direction, position):
       self.direction = direction
       self.position = position

    def get_before(self):
        if self.direction == 'horizontal':
            self.before = (self.position[0]-1, self.position[1])
        elif self.direction == 'vertical':
            self.before = (self.position[0] - 1, self.position[1])
        elif self.direction == 'northwest':
            self.before = (self.position[0] - 1, self.position[1] - 1)
        else:
            self.before = (self.position[0] - 1, self.position[1] + 1)
        return self.before

    def get_after(self):
        if self.direction == 'horizontal':
            self.after = (self.position[0], self.position[1] + 1)
        elif self.direction == 'vertical':
            self.after = (self.position[0] + 1, self.position[1])
        elif self.direction == 'northwest':
            self.after = (self.position[0] + 1, self.position[1] + 1)
        else:
            self.after = (self.position[0] + 1, self.position[1] - 1)
        return self.after


def is_win_this_way(current_position=(5, 5), direction='horizontal'):
    current_color = chess_board[current_position]                               # 获取最后这枚棋子的颜色
    core_chess = Chess(direction=direction, position=current_position)
    before_color = chess_board[core_chess.get_before()]
    after_color = chess_board[core_chess.get_after()]
    if (before_color != current_color) & (after_color != current_color):        # 如果前后都不等于这个颜色
        return None
    cumulative_color = 1                                                # 连着多少个该颜色，当前颜色计数为1                                                         # 已经计算了多少个棋子
    before_chess = Chess(direction=direction, position=current_position)
    after_chess = Chess(direction=direction, position=current_position)
    while before_color == current_color:                               # 先向左数有多少一样的
        cumulative_color += 1
        before_chess = Chess(direction=direction, position=before_chess.get_before())
        before_color = chess_board[before_chess.get_before()]
        if cumulative_color == 5:                                                               # 如果已经连着5个一样的了
            if (before_color != current_color) & (after_color != current_color):    # 两端的第6个不能是一个颜色
                return 1
            else:
                return None
    # 向右继续数有多少一样的
    while after_color == current_color:
        cumulative_color +=1
        after_chess = Chess(direction=direction, position=after_chess.get_before())
        after_color = chess_board[core_chess.get_after()]
        if cumulative_color == 5:
            if after_color != current_color:
                return 1
            else:
                return None

    return None

for direct in ['horizontal', 'vertical', 'northwest', 'northeast']:
    if is_win_this_way(current_position=current_status, direction=direct):
        print('win')
        break