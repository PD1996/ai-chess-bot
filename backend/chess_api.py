from flask import Flask, request, jsonify
import chess

app = Flask(__name__)
board = chess.Board()


@app.route("/move", methods=["POST"])
def make_move():
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
    return jsonify({"board": str(board)}), 200


if __name__ == "__main__":
    app.run(port=5000)
