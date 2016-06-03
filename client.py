#!/usr/bin/python3
import argparse
import socket
import json

from common import GamePiece, GameMessages


class TicTacClient():

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((self.host, self.port))

        while True:
            response = server_socket.recv(128)
            decoded_response = json.loads(response.decode('utf-8'))
            if decoded_response['msg'] == GameMessages.WINNER:
                print('You won the game')
                break
            elif decoded_response['msg'] == GameMessages.LOSER:
                print('You lost the game')
                break
            elif decoded_response['msg'] == GameMessages.DRAW:
                print('You drew the game')
                break
            else:
                game_state = json.loads(response.decode('utf-8'))
                self.print_board(game_state['board'])
                self.make_move(server_socket)

    @staticmethod
    def print_board(game_state):
        for idx, val in enumerate(game_state):
            if val == GamePiece.X:
                space = 'X'
            elif val == GamePiece.O:
                space = 'O'
            else:
                space = idx
            print(' ' + str(space) + ' ', end='')
            if idx % 3 == 2:
                print('\n-----------')
            else:
                print('|', end='')

    def make_move(self, server_socket):
        move = int(input('Where would you like to go?'))
        server_socket.send(str(move).encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    host = args.host
    port = args.port

    client = TicTacClient(host, port)
    client.run()
