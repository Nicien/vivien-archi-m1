import { useEffect, useState } from "react";
import "./App.css";
import type { components } from "./backend-schema";

type UpdateCellBody = components["schemas"]["UpdateBody"];
type Grid = components["schemas"]["Grid"];

async function resetGrid() {
    await fetch("http://localhost:22222/reset", {
        method: "POST",
    });
}

async function handleUpdateCell(
  cellIndex: number,
  color: string
) {
  const body: UpdateCellBody = {
    caption: "",
    color: color,
  };
  await fetch(`http://localhost:22222/cell/${cellIndex}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
}

function App() {
  const [grid, setGrid] = useState<Grid | null>(null);
  const [color, setColor] = useState("#00ffff");

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:22222/ws");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const gridData: Grid = JSON.parse(event.data);
      setGrid(gridData);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="container">
      <h4>The Grid</h4>
      <input type="color" value={color} onChange={(e) => setColor(e.target.value)} />

        <input
            type="button"
            value="Reset"
            onClick={() => resetGrid()}
        />

      {grid && (
        <>
          {/* Affichage clair du nombre de cases */}
          <p className="case-count">
            Nombre de cases : {grid.width * grid.height}
          </p>

          <div
            className="world-grid"
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${grid.width}, 50px)`,
              gridTemplateRows: `repeat(${grid.height}, 50px)`,
            }}
          >
            {grid.cells.map((cell, cellIndex) => (
              <div
                key={cellIndex}
                className="cell"
                onClick={() => handleUpdateCell(cellIndex, color)}
                style={{
                  backgroundColor: cell.color ?? "transparent",
                }}
              >
                {cell.caption ?? ""}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
