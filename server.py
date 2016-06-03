#!/usr/bin/python3
import argparse
import socket
import json

from common import GamePiece, GameMessages


class TicTacToe:
    def __init__(self):
        self.board_state = [GamePiece.blank] * 9
        self.free_spaces = list(range(9))

    def make_move(self, position, piece):
        if position in self.free_spaces:
            self.board_state[position] = piece
            self.free_spaces.remove(position)
            return True
        else:
            return False

    def has_won(self):
        # check columns
        for x in range(0, 3):
            if self.board_state[x] != GamePiece.blank and self.board_state[x] == self.board_state[x + 3] == \
                    self.board_state[x + 6]:
                return True

        # check rows
        for x in [0, 3, 6]:
            if self.board_state[x] != GamePiece.blank and self.board_state[x] == self.board_state[x + 1] == \
                    self.board_state[x + 2]:
                return True

        # check diagonals
        if self.board_state[4] != GamePiece.blank and self.board_state[0] == self.board_state[4] == self.board_state[8]:
            return True
        if self.board_state[4] != GamePiece.blank and self.board_state[2] == self.board_state[4] == self.board_state[6]:
            return True

        return False


class TicTacServer:
    def __init__(self, port):
        # create game state
        self.game = TicTacToe()
        self.x_player = None
        self.o_player = None

        # create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(2)

    def run(self):
        self.connect_players()

        winner = None
        for round in range(5):
            self.prompt_player(GamePiece.X)
            if self.game.has_won():
                winner = GamePiece.X
                break

            # X has last move in round 5.
            if round == 4:
                break

            self.prompt_player(GamePiece.O)
            if self.game.has_won():
                winner = GamePiece.O
                break

        self.end_game(winner)

    def end_game(self, winner):
        winner_msg = json.dumps({'msg': GameMessages.WINNER}).encode('UTF-8')
        loser_msg = json.dumps({'msg': GameMessages.LOSER}).encode('UTF-8')
        draw_msg = json.dumps({'msg': GameMessages.DRAW}).encode('UTF-8')

        if winner == GamePiece.X:
            self.x_player.send(winner_msg)
            self.o_player.send(loser_msg)
        elif winner == GamePiece.O:
            self.x_player.send(loser_msg)
            self.o_player.send(winner_msg)
        else:
            self.x_player.send(draw_msg)
            self.o_player.send(draw_msg)

        self.x_player.close()
        self.o_player.close()

    def connect_players(self):
        # first player to connect will be X player
        self.x_player = self.server_socket.accept()[0]
        # second player to connect will be O player
        self.o_player = self.server_socket.accept()[0]

    def prompt_player(self, player):
        player_socket = self.x_player if player == GamePiece.X else self.o_player
        while True:
            board_msg = {'msg': GameMessages.MAKE_MOVE, 'board': self.game.board_state}
            player_socket.send(json.dumps(board_msg).encode('utf-8'))
            user_move = int(player_socket.recv(4))
            is_valid_move = self.game.make_move(user_move, player)
            if is_valid_move:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    server = TicTacServer(args.port)
    server.run()
