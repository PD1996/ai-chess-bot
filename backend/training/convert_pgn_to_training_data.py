import json
import chess.pgn

def pgn_to_games(pgn_filepath):
    games = []

    with open(pgn_filepath) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            games.append(game)

    return games

def game_to_training_data(game):
    training_data = []
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
games = pgn_to_games(pgn_filepath)

training_test_split = 0.8
split_index = int(len(games) * training_test_split)

training_games = games[:split_index]
test_games = games[split_index:]

training_data = [data for game in training_games for data in game_to_training_data(game)]
test_data = [data for game in test_games for data in game_to_training_data(game)]

with open("./data/training_data.json", "w") as f:
    json.dump(training_data, f)

with open("./data/test_data.json", "w") as f:
    json.dump(test_data, f)