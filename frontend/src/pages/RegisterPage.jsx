// src/pages/RegisterPage.jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { register } from '../api/auth'
import useAuthStore from '../store/authStore'
import toast from 'react-hot-toast'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const setLogin = useAuthStore((s) => s.login)
  const navigate = useNavigate()

  const handleRegister = async (e) => {
    e.preventDefault()
    if (!email || !password) { toast.error('Please fill in all fields'); return }
    if (password.length < 8) { toast.error('Password must be at least 8 characters'); return }
    if (confirmPassword && password !== confirmPassword) { toast.error('Passwords do not match'); return }
    setLoading(true)
    try {
      const data = await register(email, password)
      setLogin(data.user, data.token)
      toast.success('Clearance granted')
      navigate('/session')
    } catch (err) {
      toast.error('Registration failed. Email may already exist.')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center p-4">
      <div className="fixed inset-0 opacity-[0.03]" style={{
        backgroundImage: 'linear-gradient(rgba(59,130,246,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.3) 1px, transparent 1px)',
        backgroundSize: '40px 40px'
      }} />

      <div className="relative w-full max-w-md animate-fade-in">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-2 h-2 rounded-full bg-warning animate-pulse" />
          <span className="text-[10px] font-mono text-on-surface-variant tracking-wider">NEW OPERATIVE REGISTRATION</span>
        </div>

        <div className="bg-surface-container border border-border rounded-xl overflow-hidden">
          <div className="px-6 py-4 border-b border-border">
            <h1 className="font-display text-xl font-bold text-on-surface tracking-wide">REQUEST CLEARANCE</h1>
            <p className="text-sm text-on-surface-variant mt-1">Register as a forensic operative</p>
          </div>

          <form onSubmit={handleRegister} className="p-6 space-y-4">
            <div>
              <label className="text-[11px] font-display font-bold tracking-[0.1em] text-on-surface-variant uppercase block mb-1.5">OPERATIVE ID</label>
              <input id="register-email" type="email" value={email} onChange={e => setEmail(e.target.value)}
                placeholder="agent@forensics.gov"
                className="w-full bg-surface-container-lowest border border-outline-variant rounded-lg px-4 py-2.5 text-sm text-on-surface placeholder-outline focus:outline-none focus:border-primary focus:shadow-[0_0_0_3px_rgba(59,130,246,0.1)] transition-all font-mono" />
            </div>
            <div>
              <label className="text-[11px] font-display font-bold tracking-[0.1em] text-on-surface-variant uppercase block mb-1.5">ACCESS KEY</label>
              <div className="relative">
                <input id="register-password" type={showPassword ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)}
                  placeholder="Min 6 characters"
                  className="w-full bg-surface-container-lowest border border-outline-variant rounded-lg px-4 py-2.5 text-sm text-on-surface placeholder-outline focus:outline-none focus:border-primary focus:shadow-[0_0_0_3px_rgba(59,130,246,0.1)] transition-all" />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors">
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
            <div>
              <label className="text-[11px] font-display font-bold tracking-[0.1em] text-on-surface-variant uppercase block mb-1.5">CONFIRM KEY</label>
              <div className="relative">
                <input id="register-confirm" type={showConfirmPassword ? "text" : "password"} value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}
                  placeholder="Re-enter access key"
                  className="w-full bg-surface-container-lowest border border-outline-variant rounded-lg px-4 py-2.5 text-sm text-on-surface placeholder-outline focus:outline-none focus:border-primary focus:shadow-[0_0_0_3px_rgba(59,130,246,0.1)] transition-all" />
                <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors">
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
            <button id="register-submit-btn" type="submit" disabled={loading}
              className="w-full bg-primary text-white font-display font-semibold rounded-lg py-2.5 text-sm tracking-wider hover:bg-primary/90 disabled:opacity-50 transition-all shadow-[0_0_20px_rgba(59,130,246,0.2)]">
              {loading ? 'PROCESSING...' : 'REQUEST CLEARANCE →'}
            </button>
          </form>

          <div className="px-6 py-3 border-t border-border text-center">
            <p className="text-xs text-on-surface-variant">
              Already have clearance?{' '}
              <Link to="/login" className="text-primary hover:underline font-medium">Authenticate</Link>
            </p>
          </div>
        </div>

        <div className="flex items-center justify-center gap-3 mt-4">
          <div className="w-1.5 h-1.5 rounded-full bg-success" />
          <span className="text-[10px] font-mono text-outline">Connection Encrypted • E2EE Active</span>
        </div>
      </div>
    </div>
  )
}
