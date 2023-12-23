import chess
import chess.pgn
import chess.engine

from datetime import datetime

import os


def count_games_in_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content.count('[Event "Self-play"]')


def play_game(engine):
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["Event"] = "Self-play"
    game.headers["Site"] = "Local"
    game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
    game.headers["Round"] = 1
    game.headers["White"] = "Stockfish"
    game.headers["Black"] = "Stockfish"
    node = game

    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        node = node.add_variation(result.move)
        board.push(result.move)

    game.headers["Result"] = board.result()
    return game


if __name__ == "__main__":
    # Detect the operating system
    if os.name == 'nt':  # Windows
        engine_path = "../stockfish-windows.exe"
    else:  # MacOS or Linux
        engine_path = "../stockfish"

    pgn_file_path = "./data/self_play_games.pgn"
    game_count = 0
    total_games_in_file = count_games_in_file(pgn_file_path)

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        try:
            while True:
                game = play_game(engine)
                with open(pgn_file_path, "a") as pgn_file:
                    print(game, file=pgn_file)
                    print("\n", file=pgn_file)

                game_count += 1
                total_games_in_file += 1

                print(f"Generated {game_count} games during this run.")
                print(f"Total games in file: {total_games_in_file}")
        except KeyboardInterrupt:
            print("Script stopped manually.")
