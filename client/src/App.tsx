import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import "./App.css";
import type { components } from './backend-schema'


type UpdateCellBody = components['schemas']['UpdateBody']
type Grid = components['schemas']['Grid']


async function fetchGrid(setGrid: Dispatch<SetStateAction<Grid | null>>) {

  const result = await fetch("http://localhost:22222/grid");
  const grid: Grid = await result.json();
  setGrid(grid);
}

async function updateCell(
  cellIndex: number,
  setGrid: Dispatch<SetStateAction<Grid | null>>,
  color: string
) {
  const body : UpdateCellBody = {
    caption: '',
    color : color
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

  const[color,setColor] = useState('white')

  useEffect(() => {
    fetchGrid(setGrid);
    

    const interval = setInterval(()=>{
        fetchGrid(setGrid);
    },10)
  }, []);

console.log("grid:", grid);

  return (
  <div className="container">
    <h4>The Grid</h4>
    <input type="color"
    onChange={(e) => 
      setColor(e.target.value )
    } 
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
            gridTemplateColumns: `repeat(${grid.width}, minmax(60px, 1fr))`,
          }}
        >
          {grid.cells.map((cell, cellIndex) => (
            <div
              key={cellIndex}
              className="cell"
              onClick={() => updateCell(cellIndex, setGrid, color)}
              style={
                {
                  width: "50px",
                  height: "50px",
                  backgroundColor : cell?.color || "white",
                }
              }
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
