import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { api } from '../services/api'

const ChatContext = createContext(null)

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(async (content) => {
    if (!content.trim()) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      const response = await api.chat(content, sessionId)
      
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        toolUsed: response.tool_used,
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err.message || 'Failed to get response')
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Error: ${err.message || 'Failed to get response. Please try again.'}`,
        timestamp: new Date().toISOString(),
        isError: true,
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const clearMessages = useCallback(() => {
    setMessages([])
    setError(null)
  }, [])

  const executeTool = useCallback(async (toolName, params) => {
    try {
      const response = await api.executeTool(toolName, params, sessionId)
      return response.result
    } catch (err) {
      throw new Error(err.message || `Failed to execute ${toolName}`)
    }
  }, [sessionId])

  return (
    <ChatContext.Provider value={{
      messages,
      isLoading,
      error,
      sessionId,
      sendMessage,
      clearMessages,
      executeTool,
    }}>
      {children}
    </ChatContext.Provider>
  )
}

export function useChat() {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider')
  }
  return context
}
