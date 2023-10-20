import React, { useState, useEffect } from "react";
import axios from "axios";
import { Chess } from "chess.js";
import whiteKing from "./assets/white_king.png";
import whiteQueen from "./assets/white_queen.png";
import whiteRook from "./assets/white_rook.png";
import whiteBishop from "./assets/white_bishop.png";
import whiteKnight from "./assets/white_knight.png";
import whitePawn from "./assets/white_pawn.png";
import blackKing from "./assets/black_king.png";
import blackQueen from "./assets/black_queen.png";
import blackRook from "./assets/black_rook.png";
import blackBishop from "./assets/black_bishop.png";
import blackKnight from "./assets/black_knight.png";
import blackPawn from "./assets/black_pawn.png";
import "./Chessboard.css";

const imageMapping = {
  wK: whiteKing,
  wQ: whiteQueen,
  wR: whiteRook,
  wB: whiteBishop,
  wN: whiteKnight,
  wP: whitePawn,
  bK: blackKing,
  bQ: blackQueen,
  bR: blackRook,
  bB: blackBishop,
  bN: blackKnight,
  bP: blackPawn,
};

const Chessboard = () => {
  const [board, setBoard] = useState(new Chess());
  const [fen, setFen] = useState("start");
  const [dragging, setDragging] = useState(null);
  const [currentTurn, setCurrentTurn] = useState("w");
  const [gameStatus, setGameStatus] = useState("In Progress");

  const sendMoveToServer = async (move) => {
    try {
      const response = await axios.post("http://localhost:5001/move", {
        move: move,
      });
      const newFen = response.data.board;
      setFen(newFen);
      board.load(newFen);
      setCurrentTurn(board.turn());
      setGameStatus(response.data.status);
    } catch (error) {
      console.log("Error sending move:", error);
    }
  };

  const loadBoard = async () => {
    try {
      const response = await axios.post("http://localhost:5001/move", {
        fen: board.fen(),
      });
      const newFen = response.data.board;
      setFen(newFen);
      board.load(newFen);
      setCurrentTurn(board.turn());
      setGameStatus(response.data.status);
    } catch (error) {
      console.log("Error loading board:", error);
    }
  };

  const handleDrop = (to) => {
    try {
      const move = board.move({ from: dragging, to: to, promotion: "q" });
      if (move === null) {
        return;
      }
      sendMoveToServer(move.from + move.to);
    } catch (e) {
      console.log("Invalid move", e);
    }
  };

  useEffect(() => {
    loadBoard();
  }, []);

  const renderBoard = () => {
    const squares = [];
    for (let i = 7; i >= 0; i--) {
      for (let j = 0; j <= 7; j++) {
        const square = String.fromCharCode(97 + j) + (i + 1);
        const piece = board.get(square);
        const color = (i + j) % 2 === 0 ? "black" : "white";
        const pieceCode = piece
          ? `${piece.color}${piece.type.toUpperCase()}`
          : "";
        squares.push(
          <div
            key={square}
            className={`square ${color}`}
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => handleDrop(square)}
          >
            {piece && (
              <span
                draggable
                onDragStart={() => setDragging(square)}
                className="piece"
                style={{ backgroundImage: `url(${imageMapping[pieceCode]})` }}
              ></span>
            )}
          </div>
        );
      }
    }
    return squares;
  };

  const resetBoard = async () => {
    try {
      const response = await axios.post("http://localhost:5001/reset");
      const newFen = response.data.board;
      setFen(newFen);
      board.load(newFen);
      setCurrentTurn(board.turn());
    } catch (error) {
      console.log("Error resetting board:", error);
    }
  };

  return (
    <div>
      <div className="chessboard">{renderBoard()}</div>
      <div>Current Turn: {currentTurn === "w" ? "White" : "Black"}</div>
      <div>Game Status: {gameStatus}</div>
      <button onClick={resetBoard}>Play Again</button>
    </div>
  );
};

export default Chessboard;
