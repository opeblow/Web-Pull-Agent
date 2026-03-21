import { Link, useLocation } from 'react-router-dom'
import { 
  Search, 
  Menu, 
  X, 
  Settings, 
  PanelRight, 
  Sparkles,
  Trash2
} from 'lucide-react'
import clsx from 'clsx'
import { useChat } from '../context/ChatContext'

export default function Header({ activeTab, setActiveTab, toggleTools, showTools }) {
  const { clearMessages } = useChat()
  const location = useLocation()

  const tabs = [
    { id: 'chat', label: 'Chat', icon: Search },
  ]

  return (
    <header className="bg-surface-secondary border-b border-surface-tertiary">
      <div className="flex items-center justify-between px-4 py-2">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-google-blue via-google-green to-google-yellow flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-white">WebPull Agent</span>
          </div>

          <nav className="hidden md:flex items-center gap-1 ml-8">
            {tabs.map(tab => {
              const Icon = tab.icon
              const isActive = location.pathname === '/'
              return (
                <Link
                  key={tab.id}
                  to="/"
                  onClick={() => setActiveTab(tab.id)}
                  className={clsx(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-surface-tertiary text-white'
                      : 'text-gray-400 hover:text-white hover:bg-surface-tertiary/50'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </Link>
              )
            })}
            <Link
              to="/settings"
              onClick={() => setActiveTab('settings')}
              className={clsx(
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                location.pathname === '/settings'
                  ? 'bg-surface-tertiary text-white'
                  : 'text-gray-400 hover:text-white hover:bg-surface-tertiary/50'
              )}
            >
              <Settings className="w-4 h-4" />
              Settings
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={clearMessages}
            className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-surface-tertiary transition-colors"
            title="Clear chat"
          >
            <Trash2 className="w-5 h-5" />
          </button>
          <button
            onClick={toggleTools}
            className={clsx(
              'p-2 rounded-lg transition-colors',
              showTools
                ? 'bg-google-blue text-white'
                : 'text-gray-400 hover:text-white hover:bg-surface-tertiary'
            )}
            title="Toggle tools panel"
          >
            {showTools ? <X className="w-5 h-5" /> : <PanelRight className="w-5 h-5" />}
          </button>
        </div>
      </div>

      <nav className="md:hidden flex items-center gap-1 px-4 pb-2 overflow-x-auto">
        {tabs.map(tab => {
          const Icon = tab.icon
          const isActive = location.pathname === '/'
          return (
            <Link
              key={tab.id}
              to="/"
              onClick={() => setActiveTab(tab.id)}
              className={clsx(
                'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors',
                isActive
                  ? 'bg-surface-tertiary text-white'
                  : 'text-gray-400 hover:text-white'
              )}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </Link>
          )
        })}
      </nav>
    </header>
  )
}
