import { useState, useEffect } from 'react'
import { listCases, createCase } from '../api/cases'
import toast from 'react-hot-toast'

export default function CaseFiles() {
  const [cases, setCases] = useState([])
  const [loading, setLoading] = useState(true)

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

  return (
    <div className="h-full flex flex-col bg-surface-container border border-border rounded-xl overflow-hidden animate-fade-in">
      <div className="px-6 py-4 border-b border-border flex items-center justify-between">
        <div>
          <h2 className="font-display text-sm font-bold tracking-[0.08em] text-on-surface uppercase">DATABASE ARCHIVE</h2>
          <p className="text-[11px] text-on-surface-variant mt-1">Review and manage saved forensic cases</p>
        </div>
        <button onClick={handleCreateCase} className="px-4 py-2 bg-primary/10 text-primary border border-primary/20 rounded-lg text-xs font-semibold hover:bg-primary/20 transition-colors">
          + NEW RECORD
        </button>
      </div>

      <div className="flex-1 overflow-auto p-6">
        {loading ? (
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
              </tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <tr key={c.id} className="border-b border-border/50 hover:bg-surface-container-high transition-colors cursor-pointer group">
                  <td className="py-4 text-sm font-mono text-primary group-hover:underline">{c.case_number}</td>
                  <td className="py-4 text-sm text-on-surface-variant">{new Date(c.created_at).toLocaleDateString()}</td>
                  <td className="py-4 text-sm text-on-surface">{c.description || 'No description'}</td>
                </tr>
              ))}
              {cases.length === 0 && (
                <tr>
                  <td colSpan="3" className="py-8 text-center text-on-surface-variant text-sm">No cases found in archive.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
