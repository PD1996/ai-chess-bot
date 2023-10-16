import React, { useState } from "react";
import axios from "axios";

const Chessboard = () => {
  const [board, setBoard] = useState(Array(8).fill(Array(8).fill(".")));
  const [move, setMove] = useState("");

  const handleMove = async () => {
    try {
      const response = await axios.post("http://localhost:5001/move", {
        move,
      });
      console.log("Response from server:", response.data);

      // Assuming the new board state is returned in response.data.board
      const boardString = response.data.board;
      const boardArray = boardString.split("\n").map((row) => row.split(" "));
      setBoard(boardArray);
    } catch (error) {
      console.log("Error sending move:", error);
    }
  };

  return (
    <div>
      <div>
        {board.map((row, i) => (
          <div key={i}>
            {row.map((cell, j) => (
              <span key={j}>{cell}</span>
            ))}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={move}
        onChange={(e) => setMove(e.target.value)}
      />
      <button onClick={handleMove}>Make Move</button>
    </div>
  );
};

export default Chessboard;
