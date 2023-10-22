import chess
import chess.pgn
import chess.engine
from datetime import datetime


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
    engine_path = "../stockfish"
    game_count = 0
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        try:
            while True:
                game = play_game(engine)
                with open("./data/self_play_games.pgn", "a") as pgn_file:
                    print(game, file=pgn_file)
                    print("\n", file=pgn_file)
                game_count += 1
                print(f"Generated {game_count} games.")
        except KeyboardInterrupt:
            print("Script stopped manually.")
