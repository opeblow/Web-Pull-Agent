import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, ExternalLink, Copy, Check } from 'lucide-react'
import clsx from 'clsx'
import { useChat } from '../context/ChatContext'

export default function ChatInterface() {
  const { messages, isLoading, sendMessage } = useChat()
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return
    const message = input
    setInput('')
    await sendMessage(message)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="flex-1 flex flex-col h-full">
      <div className="flex-1 overflow-y-auto chat-messages">
        <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
          {messages.length === 0 && (
            <WelcomeMessage onSuggestionClick={(text) => setInput(text)} />
          )}
          
          {messages.map((message) => (
            <Message
              key={message.id}
              message={message}
              onCopy={copyToClipboard}
            />
          ))}
          
          {isLoading && <LoadingIndicator />}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="border-t border-surface-tertiary p-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <div className="search-box bg-surface-secondary rounded-2xl border border-surface-tertiary flex items-end">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything..."
                className="flex-1 bg-transparent text-white placeholder-gray-500 px-4 py-3 pr-12 resize-none focus:outline-none max-h-40"
                rows={1}
                disabled={isLoading}
                style={{ minHeight: '48px' }}
              />
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className={clsx(
                  'absolute right-2 bottom-2 p-2 rounded-lg transition-colors',
                  input.trim() && !isLoading
                    ? 'bg-google-blue text-white hover:bg-google-blue/90'
                    : 'text-gray-500 cursor-not-allowed'
                )}
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            <p className="text-xs text-gray-500 text-center mt-2">
              Press Enter to send, Shift+Enter for new line
            </p>
          </form>
        </div>
      </div>
    </div>
  )
}

function WelcomeMessage({ onSuggestionClick }) {
  const suggestions = [
    { text: 'What\'s the weather in New York?', icon: '🌤' },
    { text: 'Tell me about artificial intelligence', icon: '📚' },
    { text: 'Latest news in technology', icon: '📰' },
    { text: 'Search for Python tutorials', icon: '🔍' },
  ]

  return (
    <div className="text-center py-12 animate-fade-in">
      <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-google-blue via-google-green to-google-yellow flex items-center justify-center">
        <Bot className="w-10 h-10 text-white" />
      </div>
      <h1 className="text-2xl font-semibold text-white mb-2">Welcome to WebPull Agent</h1>
      <p className="text-gray-400 mb-8 max-w-md mx-auto">
        Your AI-powered research assistant. I can search the web, check weather, 
        fetch Wikipedia articles, and more.
      </p>
      
      <div className="flex flex-wrap justify-center gap-3">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSuggestionClick(suggestion.text)}
            className="px-4 py-2 rounded-full bg-surface-secondary border border-surface-tertiary text-gray-300 text-sm hover:bg-surface-tertiary hover:text-white transition-colors"
          >
            <span className="mr-2">{suggestion.icon}</span>
            {suggestion.text}
          </button>
        ))}
      </div>
    </div>
  )
}

function Message({ message, onCopy }) {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'

  const handleCopy = () => {
    onCopy(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className={clsx(
      'flex gap-4 animate-slide-up',
      isUser ? 'flex-row-reverse' : 'flex-row'
    )}>
      <div className={clsx(
        'flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center',
        isUser ? 'bg-google-blue' : 'bg-surface-secondary'
      )}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      <div className={clsx(
        'flex-1 max-w-3xl',
        isUser ? 'text-right' : 'text-left'
      )}>
        <div className={clsx(
          'inline-block rounded-2xl px-4 py-3',
          isUser 
            ? 'bg-google-blue text-white' 
            : message.isError
              ? 'bg-red-500/20 text-red-300 border border-red-500/30'
              : 'bg-surface-secondary text-gray-100'
        )}>
          <div className="message-content whitespace-pre-wrap">
            {message.content}
          </div>
        </div>
        
        <div className={clsx(
          'flex items-center gap-2 mt-2',
          isUser ? 'justify-end' : 'justify-start'
        )}>
          {!isUser && (
            <button
              onClick={handleCopy}
              className="p-1.5 rounded-lg text-gray-500 hover:text-white hover:bg-surface-tertiary transition-colors"
              title="Copy response"
            >
              {copied ? (
                <Check className="w-4 h-4 text-green-500" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
            </button>
          )}
          {message.link && (
            <a
              href={message.link}
              target="_blank"
              rel="noopener noreferrer"
              className="p-1.5 rounded-lg text-gray-500 hover:text-white hover:bg-surface-tertiary transition-colors"
              title="Open link"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
          <span className="text-xs text-gray-600">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  )
}

function LoadingIndicator() {
  return (
    <div className="flex gap-4 animate-slide-up">
      <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-surface-secondary flex items-center justify-center">
        <Bot className="w-5 h-5 text-white" />
      </div>
      <div className="bg-surface-secondary rounded-2xl px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="loading-dots flex gap-1">
            <span className="w-2 h-2 rounded-full bg-google-blue animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-google-green animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-google-yellow animate-bounce" />
          </div>
          <span className="text-gray-400 text-sm">Thinking...</span>
        </div>
      </div>
    </div>
  )
}
