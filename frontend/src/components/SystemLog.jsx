import { useState, useEffect } from 'react'
import { getGlobalAuditLog } from '../api/audit'

export default function SystemLog() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = await getGlobalAuditLog()
        setLogs(data)
      } catch (err) {
        console.error('Failed to fetch system logs', err)
      } finally {
        setLoading(false)
      }
    }
    fetchLogs()
    const interval = setInterval(fetchLogs, 10000) // Refresh every 10s
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="h-full flex flex-col bg-surface-container-lowest border border-border rounded-xl overflow-hidden animate-fade-in font-mono">
      <div className="px-6 py-3 border-b border-border bg-surface-container flex items-center justify-between">
        <h2 className="text-xs font-bold tracking-[0.1em] text-on-surface uppercase flex items-center gap-2">
          <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
          System Diagnostic Output
        </h2>
        <span className="text-[10px] text-outline">Terminal View</span>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto space-y-1 text-[11px]">
        {loading && logs.length === 0 ? (
          <div className="text-outline animate-pulse">Initializing diagnostic stream...</div>
        ) : logs.map((log, i) => (
          <div key={log.id || i} className="flex gap-4 hover:bg-surface-container-high px-2 py-1 rounded">
            <span className="text-outline shrink-0">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
            <span className="shrink-0 w-12 text-success">
              INFO
            </span>
            <span className="text-on-surface-variant truncate">{log.summary}</span>
          </div>
        ))}
        <div className="flex gap-4 px-2 py-1 animate-pulse">
          <span className="text-primary">_</span>
        </div>
      </div>
    </div>
  )
}
