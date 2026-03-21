const API_BASE = '/api'

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  return response.json()
}

export const api = {
  async chat(message, sessionId = 'default') {
    return request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, session_id: sessionId }),
    })
  },

  async executeTool(toolName, params = {}, sessionId = 'default') {
    return request('/tool', {
      method: 'POST',
      body: JSON.stringify({ tool_name: toolName, params, session_id: sessionId }),
    })
  },

  async getStatus(sessionId) {
    return request(`/status/${sessionId}`)
  },

  async deleteSession(sessionId) {
    return request(`/session/${sessionId}`, { method: 'DELETE' })
  },

  async health() {
    return request('/health')
  },
}
