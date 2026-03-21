import { useState } from 'react'
import { Settings as SettingsIcon, Key, Globe, Info, ExternalLink } from 'lucide-react'
import clsx from 'clsx'

export default function Settings() {
  const [apiKey, setApiKey] = useState('')
  const [saved, setSaved] = useState(false)

  const handleSaveApiKey = () => {
    if (apiKey.trim()) {
      localStorage.setItem('openai_api_key', apiKey.trim())
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    }
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 rounded-xl bg-surface-secondary flex items-center justify-center">
            <SettingsIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-white">Settings</h1>
            <p className="text-gray-400">Configure your WebPull Agent</p>
          </div>
        </div>

        <div className="space-y-6">
          <section className="p-6 rounded-2xl bg-surface-secondary border border-surface-tertiary">
            <div className="flex items-center gap-3 mb-4">
              <Key className="w-5 h-5 text-google-blue" />
              <h2 className="text-lg font-medium text-white">API Configuration</h2>
            </div>
            
            <p className="text-sm text-gray-400 mb-4">
              Enter your OpenAI API key to enable AI-powered features. Your key is stored locally 
              and never sent to our servers.
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">
                  OpenAI API Key
                </label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full px-4 py-2.5 rounded-lg bg-surface-tertiary border border-surface-tertiary text-white placeholder-gray-500 focus:outline-none focus:border-google-blue"
                />
              </div>
              
              <button
                onClick={handleSaveApiKey}
                disabled={!apiKey.trim()}
                className={clsx(
                  'px-4 py-2 rounded-lg font-medium transition-colors',
                  apiKey.trim()
                    ? 'bg-google-blue text-white hover:bg-google-blue/90'
                    : 'bg-surface-tertiary text-gray-500 cursor-not-allowed'
                )}
              >
                {saved ? 'Saved!' : 'Save API Key'}
              </button>
            </div>
          </section>

          <section className="p-6 rounded-2xl bg-surface-secondary border border-surface-tertiary">
            <div className="flex items-center gap-3 mb-4">
              <Globe className="w-5 h-5 text-google-green" />
              <h2 className="text-lg font-medium text-white">Available Tools</h2>
            </div>

            <ul className="space-y-3">
              {[
                { name: 'Web Scraper', desc: 'Extract content from any URL' },
                { name: 'Google Search', desc: 'Search and get top results' },
                { name: 'Wikipedia', desc: 'Fetch article summaries' },
                { name: 'News Headlines', desc: 'Get latest news' },
                { name: 'Weather', desc: 'Current weather for any city' },
              ].map((tool, i) => (
                <li key={i} className="flex items-center gap-3 p-3 rounded-lg bg-surface-tertiary/50">
                  <div className="w-2 h-2 rounded-full bg-google-blue" />
                  <div>
                    <span className="font-medium text-white">{tool.name}</span>
                    <span className="text-gray-400 text-sm ml-2">— {tool.desc}</span>
                  </div>
                </li>
              ))}
            </ul>
          </section>

          <section className="p-6 rounded-2xl bg-surface-secondary border border-surface-tertiary">
            <div className="flex items-center gap-3 mb-4">
              <Info className="w-5 h-5 text-google-yellow" />
              <h2 className="text-lg font-medium text-white">About</h2>
            </div>

            <div className="space-y-3 text-sm text-gray-400">
              <p>
                <strong className="text-white">WebPull Agent</strong> is an AI-powered research 
                assistant that helps you find information on the web.
              </p>
              <p>
                Built with FastAPI backend and React frontend, powered by GPT-4o for intelligent 
                tool selection and natural language responses.
              </p>
              <div className="pt-2">
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-google-blue hover:underline"
                >
                  View on GitHub
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
