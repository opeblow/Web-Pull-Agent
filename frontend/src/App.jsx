import { useState, useCallback, useRef, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import ChatInterface from './components/ChatInterface'
import ToolsPanel from './components/ToolsPanel'
import Settings from './components/Settings'
import { ChatProvider } from './context/ChatContext'
import './App.css'

function App() {
  const [showTools, setShowTools] = useState(false)
  const [activeTab, setActiveTab] = useState('chat')
  const mainRef = useRef(null)

  const toggleTools = useCallback(() => {
    setShowTools(prev => !prev)
  }, [])

  return (
    <ChatProvider>
      <BrowserRouter>
        <div className="app-container min-h-screen bg-surface-primary flex flex-col">
          <Header 
            activeTab={activeTab} 
            setActiveTab={setActiveTab}
            toggleTools={toggleTools}
            showTools={showTools}
          />
          
          <main 
            ref={mainRef}
            className="flex-1 flex overflow-hidden"
          >
            <div className="flex-1 flex flex-col">
              <Routes>
                <Route path="/" element={<ChatInterface />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </div>
            
            {showTools && (
              <ToolsPanel onClose={() => setShowTools(false)} />
            )}
          </main>
        </div>
      </BrowserRouter>
    </ChatProvider>
  )
}

export default App
