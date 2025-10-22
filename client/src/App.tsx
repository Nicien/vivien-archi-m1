// client/src/App.jsx
import { useEffect, useState, type Dispatch, SetStateAction } from 'react'
import './App.css'


type Cell = {
    playerName?: string
}

type Grid = {
    width: number
    height: number
    cells: Cell[]
}

async function fetchGrid(setGrid: Dispatch<SetStateAction<Grid | null>>) {
    const result = await fetch('http://localhost:22222/grid')
    const grid : Grid = await result.json()
    setGrid(grid)
}

function App() {
    const [grid, setGrid] = useState<Grid | null>(null)

    useEffect(() => {
        fetchGrid(setGrid)
    }, [])

    return (
        <div className="container">
            <h4>The Grid</h4>
            {
                grid && <div className="world-grid" style={{
                    gridTemplateColumns: `repeat(${grid.width}, 100px)`,
                    gridTemplateRows: `repeat(${grid.height}, 100px)`
                }}>
                    {
                        grid.cells.map((cell, cellIndex)=>(
                            <div key={cellIndex}>
                                { cell.playerName }
                            </div>
                        ))
                    }
                </div>
            }
        </div>
    )
}

export default App
