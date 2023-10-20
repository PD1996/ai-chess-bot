from flask import Flask, request, jsonify
from flask_cors import CORS
import chess

app = Flask(__name__)
CORS(app)

board = chess.Board()


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
    return jsonify({"board": board.fen()}), 200


@app.route("/reset", methods=["POST"])
def reset_board():
    global board
    board = chess.Board()
    return jsonify({"board": board.fen()}), 200


if __name__ == "__main__":
    app.run(port=5001)
