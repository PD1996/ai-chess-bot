from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine


app = Flask(__name__)
CORS(app)

board = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci("./stockfish")


@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Chess API."


@app.route("/move", methods=["POST"])
def make_move():
    print("Received data:", request.json)
    global board
    move_uci = request.json.get("move", None)

    if move_uci is None:
        return jsonify({"error": "No move provided"}), 400

    try:
        move = chess.Move.from_uci(move_uci)
    except:
        return jsonify({"error": "Invalid UCI format"}), 400

    if move not in board.legal_moves:
        return jsonify({"error": "Illegal move"}), 400

    board.push(move)

    # AI's turn
    if not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)

    status = "In Progress"
    if board.is_checkmate():
        status = (
            f"Checkmate! - {'White' if board.turn == chess.BLACK else 'Black'} wins!"
        )
    elif board.is_stalemate():
        status = "Stalemate!"

    return jsonify({"board": board.fen(), "status": status}), 200


@app.route("/reset", methods=["POST"])
def reset_board():
    global board
    color = request.json.get("color", "w")
    board = chess.Board()
    if board.turn == chess.WHITE and color == "b":
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
    elif board.turn == chess.BLACK and color == "w":
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
    return jsonify({"board": board.fen(), "status": "In Progress"}), 200


if __name__ == "__main__":
    app.run(port=5001)
