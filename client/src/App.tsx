import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import "./App.css";
import type { components } from './backend-schema'

type UpdateCellBody = components['schemas']['UpdateBody']

type Cell = {
  playerName?: string;
};

type Grid = {
  width: number;
  height: number;
  cells: Cell[];
};

async function fetchGrid(setGrid: Dispatch<SetStateAction<Grid | null>>) {
  const result = await fetch("http://localhost:22222/grid");
  const grid: Grid = await result.json();
  setGrid(grid);
}

async function updateCell(
  cellIndex: number,
  setGrid: Dispatch<SetStateAction<Grid | null>>
) {
  const body : UpdateCellBody = {
    caption: 'player1'
  }
  await fetch(`http://localhost:22222/cell/${cellIndex}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  await fetchGrid(setGrid);
}

function App() {
  const [grid, setGrid] = useState<Grid | null>(null);

  useEffect(() => {
    fetchGrid(setGrid);
  }, []);

  return (
    <div className="container">
      <h4>The Grid</h4>

      {grid && (
        <div
          className="world-grid"
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${grid.width}, 100px)`,
            gridTemplateRows: `repeat(${grid.height}, 100px)`,
          }}
        >
          {grid.cells.map((cell, cellIndex) => (
            <div
              key={cellIndex}
              className="cell"
              onClick={() => updateCell(cellIndex, setGrid)}
              style={{
                border: "1px solid black",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
              }}
            >
              {cell.playerName ?? ""}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
