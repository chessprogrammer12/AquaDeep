#!/usr/bin/env python3
# search.py

import chess
import eval
import time

MAX_DEPTH = 4  # Bullet speed

def quiescence(board, alpha, beta):
    stand_pat = eval.evaluate(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True):
        if board.is_capture(move):
            board.push(move)
            score = -quiescence(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def negamax(board, depth, alpha, beta, start_time, time_limit):
    if time.time() - start_time > time_limit:
        raise TimeoutError
    if depth == 0 or board.is_game_over():
        return quiescence(board, alpha, beta)

    max_eval = -99999
    # Move ordering: captures first
    moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
    for move in moves:
        board.push(move)
        try:
            score = -negamax(board, depth-1, -beta, -alpha, start_time, time_limit)
        except TimeoutError:
            board.pop()
            raise
        board.pop()
        if score > max_eval:
            max_eval = score
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return max_eval

def find_best_move(board: chess.Board, max_time=1.0):
    best_move = None
    start_time = time.time()
    depth = 1
    try:
        while True:
            max_eval = -99999
            moves = sorted(board.legal_moves, key=lambda m: board.is_capture(m), reverse=True)
            for move in moves:
                board.push(move)
                try:
                    score = -negamax(board, depth-1, -100000, 100000, start_time, max_time)
                except TimeoutError:
                    board.pop()
                    raise
                board.pop()
                if score > max_eval:
                    max_eval = score
                    best_move = move
            print(f"info depth {depth} score cp {max_eval} pv {best_move}")
            depth += 1
            if depth > MAX_DEPTH:
                break
    except TimeoutError:
        pass
    return best_move
