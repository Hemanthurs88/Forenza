import { useState, useEffect } from 'react'
import { listCases, createCase, getCaseHistory } from '../api/cases'
import toast from 'react-hot-toast'

export default function CaseFiles() {
  const [cases, setCases] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCase, setSelectedCase] = useState(null)
  const [caseHistory, setCaseHistory] = useState([])
  const [historyLoading, setHistoryLoading] = useState(false)

  useEffect(() => {
    loadCases()
  }, [])

  const loadCases = async () => {
    try {
      setLoading(true)
      const data = await listCases()
      setCases(data)
    } catch (err) {
      toast.error('Failed to load cases')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCase = async () => {
    const caseNumber = prompt('Enter Case Number (e.g., CAS-1234):')
    if (!caseNumber) return
    const description = prompt('Enter Description:')
    
    try {
      await createCase({ case_number: caseNumber, description })
      toast.success('Case record created')
      loadCases()
    } catch (err) {
      toast.error('Failed to create case')
    }
  }

  const viewHistory = async (c) => {
    setSelectedCase(c)
    setHistoryLoading(true)
    try {
      const data = await getCaseHistory(c.id)
      setCaseHistory(data)
    } catch (err) {
      toast.error('Failed to load case history')
    } finally {
      setHistoryLoading(false)
    }
  }

  return (
    <div className="h-full flex flex-col bg-surface-container border border-border rounded-xl overflow-hidden animate-fade-in">
      <div className="px-6 py-4 border-b border-border flex items-center justify-between">
        <div>
          <h2 className="font-display text-sm font-bold tracking-[0.08em] text-on-surface uppercase">DATABASE ARCHIVE</h2>
          <p className="text-[11px] text-on-surface-variant mt-1">Review and manage saved forensic cases</p>
        </div>
        <div className="flex gap-2">
          {selectedCase && (
            <button onClick={() => setSelectedCase(null)} className="px-4 py-2 bg-surface-container-high text-on-surface border border-outline-variant rounded-lg text-xs font-semibold hover:bg-surface-container-highest transition-colors">
              BACK TO LIST
            </button>
          )}
          <button onClick={handleCreateCase} className="px-4 py-2 bg-primary/10 text-primary border border-primary/20 rounded-lg text-xs font-semibold hover:bg-primary/20 transition-colors">
            + NEW RECORD
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6">
        {selectedCase ? (
          <div className="space-y-6">
            <div className="flex items-start justify-between bg-surface-container-low p-4 rounded-lg border border-outline-variant">
              <div>
                <h3 className="text-primary font-mono font-bold text-lg">{selectedCase.case_number}</h3>
                <p className="text-sm text-on-surface mt-1">{selectedCase.description || 'No description provided'}</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-outline uppercase font-bold">Created On</p>
                <p className="text-xs text-on-surface-variant">{new Date(selectedCase.created_at).toLocaleString()}</p>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-xs font-display font-bold text-outline tracking-widest uppercase">AUDIT TRAIL</h4>
              {historyLoading ? (
                <div className="flex justify-center p-8"><div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" /></div>
              ) : caseHistory.length === 0 ? (
                <div className="text-center py-8 text-on-surface-variant text-sm bg-surface-container-low rounded-lg border border-dashed border-outline-variant">No audit logs found for this case.</div>
              ) : (
                <div className="grid grid-cols-1 gap-3">
                  {caseHistory.map((log) => (
                    <div key={log.id} className="flex items-center gap-4 p-3 bg-surface-container-lowest border border-border/50 rounded-lg group hover:border-primary/30 transition-all">
                      <div className="w-12 h-12 rounded bg-black/5 overflow-hidden flex-shrink-0">
                        {log.image_url ? (
                          <img src={log.image_url} alt="State" className="w-full h-full object-cover" />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-[10px] text-outline">N/A</div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 bg-primary/10 text-primary rounded uppercase">{log.action}</span>
                          <span className="text-[11px] text-outline">{new Date(log.timestamp).toLocaleString()}</span>
                        </div>
                        <p className="text-xs text-on-surface-variant truncate mt-1">
                          {log.params_after ? Object.entries(log.params_after).slice(0,3).map(([k,v]) => `${k}:${(v*100).toFixed(0)}`).join(', ') + '...' : 'No parameters changed'}
                        </p>
                      </div>
                      {log.image_url && (
                        <a href={log.image_url} target="_blank" rel="noreferrer" className="opacity-0 group-hover:opacity-100 p-2 text-primary hover:bg-primary/10 rounded-full transition-all">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-border">
                  <th className="pb-3 text-xs font-display font-semibold text-outline tracking-wider uppercase">Case ID</th>
                  <th className="pb-3 text-xs font-display font-semibold text-outline tracking-wider uppercase">Date Logged</th>
                  <th className="pb-3 text-xs font-display font-semibold text-outline tracking-wider uppercase">Description</th>
                  <th className="pb-3 text-xs font-display font-semibold text-outline tracking-wider uppercase">Action</th>
                </tr>
              </thead>
              <tbody>
                {cases.map((c) => (
                  <tr key={c.id} className="border-b border-border/50 hover:bg-surface-container-high transition-colors group">
                    <td className="py-4 text-sm font-mono text-primary">{c.case_number}</td>
                    <td className="py-4 text-sm text-on-surface-variant">{new Date(c.created_at).toLocaleDateString()}</td>
                    <td className="py-4 text-sm text-on-surface">{c.description || 'No description'}</td>
                    <td className="py-4">
                      <button onClick={() => viewHistory(c)} className="text-[10px] font-display font-bold text-primary px-3 py-1 border border-primary/20 rounded bg-primary/5 hover:bg-primary/10 transition-all uppercase tracking-tighter">
                        VIEW AUDIT
                      </button>
                    </td>
                  </tr>
                ))}
                {cases.length === 0 && (
                  <tr>
                    <td colSpan="4" className="py-8 text-center text-on-surface-variant text-sm">No cases found in archive.</td>
                  </tr>
                )}
              </tbody>
            </table>
          )
        )}
      </div>
    </div>
  )
}
