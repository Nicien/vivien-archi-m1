import { useEffect, useState } from "react";
import "./App.css";
import type { components } from "./backend-schema";

type UpdateCellBody = components["schemas"]["UpdateBody"];
type Grid = components["schemas"]["Grid"];

function App() {
  const [grid, setGrid] = useState<Grid | null>(null);
  const [color, setColor] = useState("#b2e27b");

  // Connexion WebSocket
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:22222/ws");
    ws.onmessage = (event) => setGrid(JSON.parse(event.data));
    return () => ws.close();
  }, []);

  // API Calls
  const resetGrid = () => fetch("http://localhost:22222/reset", { method: "POST" });
  const startBadApple = () => fetch("http://localhost:22222/play-bad-apple", { method: "POST" });

  const handleUpdateCell = async (cellIndex: number, cellColor: string) => {
    const body: UpdateCellBody = { caption: "", color: cellColor };
    await fetch(`http://localhost:22222/cell/${cellIndex}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  };

  // Adaptation dynamique de la taille des cases
  const isVideoMode = grid && grid.width > 20;
  const cellSize = isVideoMode ? "15px" : "50px";

  return (
    <div className="container">
      <h4>The Grid - Bad Apple Edition</h4>

      <div className="controls" style={{ marginBottom: "20px" }}>
        <input type="color" value={color} onChange={(e) => setColor(e.target.value)} />
        <button onClick={resetGrid}>Reset</button>

        <button
          onClick={startBadApple}
          style={{ marginLeft: "10px", background: "#2ecc71", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer" }}
        >
          ▶ PLAY
        </button>

        <button
          onClick={resetGrid}
          style={{ marginLeft: "5px", background: "#e74c3c", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer" }}
        >
          🛑 OFF
        </button>
      </div>

      {grid && (
        <>
          <p>Taille de la grille : {grid.width}x{grid.height}</p>
          <div
            className="world-grid"
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${grid.width}, ${cellSize})`,
              gap: "0px",
              background: "#ffffff",
              padding: "8px",
              borderRadius: "8px",
              margin: "0 auto",
              width: "fit-content",
              boxSizing: "border-box"
            }}
          >
            {grid.cells.map((cell, idx) => (
              <div
                key={idx}
                className="cell"
                onClick={() => handleUpdateCell(idx, color)}
                style={{
                  width: cellSize,
                  height: cellSize,
                  minWidth: cellSize,
                  minHeight: cellSize,
                  maxWidth: cellSize,
                  maxHeight: cellSize,
                  backgroundColor: cell.color ?? "transparent",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "10px",
                  boxSizing: "border-box",
                  border: "0.1px solid #222",
                  padding: "0"
                }}
              >
                {!isVideoMode && cell.caption}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;