import { useCallback, useEffect, useState } from "react";
import "./App.css";
import type { components } from "./backend-schema";

type UpdateCellBody = components["schemas"]["UpdateBody"];
type Grid = components["schemas"]["Grid"];

const getApiUrl = () => {
  if (import.meta.env) {
    if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  }

  if (window.location.hostname !== "localhost") {
    return `${window.location.protocol}//${window.location.hostname}:22222`;
  }

  return "http://localhost:22222";
};

const getWsUrl = () => {
  if (import.meta.env) {
    if (import.meta.env.VITE_WS_URL) return import.meta.env.VITE_WS_URL;
  }

  if (window.location.hostname !== "localhost") {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${window.location.hostname}:22222/ws`;
  }

  return "ws://localhost:22222/ws";
};

const API_URL = getApiUrl();
const WS_URL = getWsUrl();

async function resetGrid() {
  await fetch(`${API_URL}/reset`, { method: "POST" });
}

async function handleUpdateCell(cellIndex: number, color: string) {
  const body: UpdateCellBody = { caption: "", color, size: 1 };
  await fetch(`${API_URL}/cell/${cellIndex}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

function App() {
  const [grid, setGrid]         = useState<Grid | null>(null);
  const [color, setColor]       = useState("#00ffff");
  const [online, setOnline]     = useState(false);
  const [flashCell, setFlash]   = useState<number | null>(null);

  // Compte le nombre de joueurs actifs (cellules avec un player)
  const playerCount = grid
    ? grid.cells.filter((c) => c.player != null).length
    : 0;

  useEffect(() => {
    let ws: WebSocket;
    let retryTimer: ReturnType<typeof setTimeout>;

    function connect() {
      ws = new WebSocket(WS_URL);

      ws.onopen = () => setOnline(true);

      ws.onmessage = (event) => {
        const gridData: Grid = JSON.parse(event.data);
        setGrid(gridData);
      };

      ws.onerror = () => setOnline(false);
      ws.onclose = () => {
        setOnline(false);
        retryTimer = setTimeout(connect, 2000);
      };
    }

    connect();
    return () => {
      clearTimeout(retryTimer);
      ws?.close();
    };
  }, []);

  const handleCellClick = useCallback(
    (cellIndex: number) => {
      handleUpdateCell(cellIndex, color);
      setFlash(cellIndex);
      setTimeout(() => setFlash(null), 260);
    },
    [color]
  );

  return (
    <div className="container">
      <h1 className="title" data-text="GRID//CYBER">
        GRID//CYBER
      </h1>

      {/* HUD */}
      <div className="hud-bar">
        <div className="color-wrapper">
          <span className="hud-label">Couleur</span>
          <input
            type="color"
            className="color-picker"
            value={color}
            onChange={(e) => setColor(e.target.value)}
          />
        </div>

        <button className="btn-reset" onClick={resetGrid}>
          <span>[ RESET ]</span>
        </button>

        <div className="player-count">
          <span className="hud-label">Joueurs</span>
          <span className="count">{playerCount}</span>
        </div>
      </div>

      {grid && (
        <>
          <p className="case-count">
            GRILLE {grid.width} × {grid.height} — {grid.width * grid.height} CASES
          </p>

          <div
            className="world-grid"
            style={{
              gridTemplateColumns: `repeat(${grid.width}, 50px)`,
              gridTemplateRows:    `repeat(${grid.height}, 50px)`,
            }}
          >
            {grid.cells.map((cell, cellIndex) => (
              <div
                key={cellIndex}
                className={`cell${flashCell === cellIndex ? " clicked" : ""}`}
                onClick={() => handleCellClick(cellIndex)}
                style={{
                  backgroundColor: cell.color ?? "transparent",
                }}
              >
                {cell.caption ?? ""}
                {cell.player && (
                  <span
                    className="player-marker"
                    style={{ backgroundColor: cell.player.color }}
                  />
                )}
              </div>
            ))}
          </div>
        </>
      )}

      {/* Status bar */}
      <div className="status-bar">
        <span>v0.1.0</span>
        <span className={online ? "status-online" : "status-offline"}>
          {online ? "◉ CONNECTÉ" : "◎ DÉCONNECTÉ"}
        </span>
        <span>ORT/PLACE</span>
      </div>
    </div>
  );
}

export default App;
