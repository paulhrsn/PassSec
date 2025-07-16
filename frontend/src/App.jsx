import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo  from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4 space-y-6">
      {/* ——— TAILWIND SMOKE TEST ——— */}
      <div className="bg-red-500 text-white px-4 py-2 rounded-lg">
        If you see this in a red box, Tailwind is working ✅
      </div>
    <div className="App">
      <header className="App-header">
        <img src={viteLogo}  className="App-logo"        alt="Vite Logo" />
        <img src={reactLogo} className="App-logo react"  alt="React Logo" />
        <p>Vite + React</p>
        <button onClick={() => setCount((c) => c + 1)}>
          count is {count}
        </button>
        <p>Edit <code>src/App.jsx</code> and save to test HMR</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    </div>
  )
}

export default App
