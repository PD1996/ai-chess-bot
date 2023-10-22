import json
import chess.pgn


def pgn_to_training_data(pgn_filepath):
    training_data = []

    with open(pgn_filepath) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            board = game.board()
            result = game.headers["Result"]
            reward = 0

            if result == "1-0":
                reward = 1
            elif result == "0-1":
                reward = -1

            for move in game.mainline_moves():
                state_representation = board.fen()
                action_representation = move.uci()

                training_data.append(
                    {
                        "state": state_representation,
                        "action": action_representation,
                        "reward": reward,
                    }
                )

                board.push(move)

    return training_data


pgn_filepath = "./data/self_play_games.pgn"
training_data = pgn_to_training_data(pgn_filepath)

with open("./data/training_data.json", "w") as f:
    json.dump(training_data, f)
