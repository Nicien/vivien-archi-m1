// client/src/App.jsx
import { useEffect } from 'react'
import './App.css'

function App() {
    const size = 3
    const rows = Array.from({ length: size }, (_, r) => r)
    const total = 2 + 2 + 2 + 2

    useEffect(() => {
        console.log(`2+2+2+2 = ${total}`)
    }, [])

    return (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0 }}>
            <table style={{ width: '100%', height: '100%', borderCollapse: 'collapse', tableLayout: 'fixed' }}>
                <tbody>
                {rows.map((r) => (
                    <tr key={r} style={{ height: `${100 / size}%` }}>
                        {rows.map((c) => (
                            <td
                                key={c}
                                style={{
                                    border: '1px solid #ccc',
                                    width: `${100 / size}%`,
                                    textAlign: 'center',
                                    verticalAlign: 'middle',
                                }}
                            ></td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}

export default App