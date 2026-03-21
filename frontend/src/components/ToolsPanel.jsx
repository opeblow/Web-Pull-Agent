import { useState } from 'react'
import { 
  X, 
  Globe, 
  Search, 
  BookOpen, 
  Newspaper, 
  Cloud,
  Link2,
  Play
} from 'lucide-react'
import clsx from 'clsx'
import { useChat } from '../context/ChatContext'

const TOOLS = [
  {
    id: 'scrape_website',
    name: 'Web Scraper',
    description: 'Extract content from any URL',
    icon: Globe,
    color: 'from-blue-500 to-cyan-500',
    params: [
      { name: 'url', label: 'URL', placeholder: 'https://example.com', required: true },
    ],
    example: 'Scrape content from a news article or blog post',
  },
  {
    id: 'google_search',
    name: 'Google Search',
    description: 'Search Google and get top results',
    icon: Search,
    color: 'from-green-500 to-emerald-500',
    params: [
      { name: 'query', label: 'Search Query', placeholder: 'Python tutorials', required: true },
      { name: 'num_results', label: 'Number of Results', type: 'number', default: 5 },
    ],
    example: 'Find the best restaurants in your area',
  },
  {
    id: 'wikipedia',
    name: 'Wikipedia',
    description: 'Get Wikipedia article summaries',
    icon: BookOpen,
    color: 'from-purple-500 to-pink-500',
    params: [
      { name: 'topic', label: 'Topic', placeholder: 'Artificial Intelligence', required: true },
    ],
    example: 'Learn about any topic from Wikipedia',
  },
  {
    id: 'get_news',
    name: 'News Headlines',
    description: 'Get latest news on any topic',
    icon: Newspaper,
    color: 'from-orange-500 to-red-500',
    params: [
      { name: 'topic', label: 'Topic', placeholder: 'Technology', required: true },
    ],
    example: 'Get the latest tech news',
  },
  {
    id: 'get_weather',
    name: 'Weather',
    description: 'Get current weather for any city',
    icon: Cloud,
    color: 'from-sky-500 to-blue-500',
    params: [
      { name: 'city', label: 'City', placeholder: 'London', required: true },
    ],
    example: 'Check weather before traveling',
  },
]

export default function ToolsPanel({ onClose }) {
  const { executeTool } = useChat()
  const [activeTool, setActiveTool] = useState(null)
  const [params, setParams] = useState({})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleToolSelect = (tool) => {
    setActiveTool(tool)
    setParams({})
    setResult(null)
    setError(null)
  }

  const handleParamChange = (name, value) => {
    setParams(prev => ({ ...prev, [name]: value }))
  }

  const handleExecute = async () => {
    if (!activeTool) return

    const requiredParams = activeTool.params.filter(p => p.required)
    const missing = requiredParams.filter(p => !params[p.name]?.trim())
    
    if (missing.length > 0) {
      setError(`Missing required: ${missing.map(p => p.label).join(', ')}`)
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const result = await executeTool(activeTool.id, params)
      setResult(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const selectedTool = TOOLS.find(t => t.id === activeTool)

  return (
    <div className="w-96 border-l border-surface-tertiary bg-surface-primary sidebar flex flex-col">
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-tertiary">
        <h2 className="font-semibold text-white">Tools</h2>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-surface-tertiary transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {!activeTool ? (
          <div className="space-y-3">
            <p className="text-sm text-gray-400 mb-4">
              Select a tool to use it directly, or use the chat to let AI choose the right tool.
            </p>
            {TOOLS.map(tool => {
              const Icon = tool.icon
              return (
                <button
                  key={tool.id}
                  onClick={() => handleToolSelect(tool.id)}
                  className="tool-card w-full p-4 rounded-xl bg-surface-secondary border border-surface-tertiary text-left hover:border-gray-600 transition-all"
                >
                  <div className="flex items-start gap-3">
                    <div className={clsx(
                      'w-10 h-10 rounded-lg bg-gradient-to-br flex items-center justify-center',
                      tool.color
                    )}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-white">{tool.name}</h3>
                      <p className="text-sm text-gray-400 mt-0.5">{tool.description}</p>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={() => setActiveTool(null)}
              className="text-sm text-google-blue hover:underline"
            >
              ← Back to tools
            </button>

            <div className="p-4 rounded-xl bg-surface-secondary border border-surface-tertiary">
              <div className="flex items-center gap-3 mb-4">
                <div className={clsx(
                  'w-10 h-10 rounded-lg bg-gradient-to-br flex items-center justify-center',
                  selectedTool?.color
                )}>
                  {(() => {
                    const Tool = TOOLS.find(t => t.id === activeTool)?.icon
                    return Tool ? <Tool className="w-5 h-5 text-white" /> : null
                  })()}
                </div>
                <div>
                  <h3 className="font-medium text-white">{selectedTool?.name}</h3>
                  <p className="text-sm text-gray-400">{selectedTool?.example}</p>
                </div>
              </div>

              <div className="space-y-3">
                {selectedTool?.params.map(param => (
                  <div key={param.name}>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      {param.label}
                      {param.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    {param.type === 'number' ? (
                      <input
                        type="number"
                        value={params[param.name] || param.default || ''}
                        onChange={(e) => handleParamChange(param.name, e.target.value)}
                        className="w-full px-3 py-2 rounded-lg bg-surface-tertiary border border-surface-tertiary text-white placeholder-gray-500 focus:outline-none focus:border-google-blue"
                        placeholder={param.placeholder}
                      />
                    ) : (
                      <input
                        type="text"
                        value={params[param.name] || ''}
                        onChange={(e) => handleParamChange(param.name, e.target.value)}
                        className="w-full px-3 py-2 rounded-lg bg-surface-tertiary border border-surface-tertiary text-white placeholder-gray-500 focus:outline-none focus:border-google-blue"
                        placeholder={param.placeholder}
                      />
                    )}
                  </div>
                ))}
              </div>

              <button
                onClick={handleExecute}
                disabled={loading}
                className={clsx(
                  'w-full mt-4 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-colors',
                  loading
                    ? 'bg-surface-tertiary text-gray-400 cursor-not-allowed'
                    : 'bg-google-blue text-white hover:bg-google-blue/90'
                )}
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-gray-400 border-t-white rounded-full animate-spin" />
                    Executing...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    Execute Tool
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="p-4 rounded-lg bg-red-500/20 border border-red-500/30 text-red-300 text-sm">
                {error}
              </div>
            )}

            {result && (
              <div className="p-4 rounded-lg bg-surface-secondary border border-surface-tertiary">
                <h4 className="text-sm font-medium text-gray-300 mb-2">Result</h4>
                <pre className="text-sm text-gray-400 whitespace-pre-wrap overflow-x-auto">
                  {typeof result === 'object' 
                    ? JSON.stringify(result, null, 2)
                    : String(result)
                  }
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
