import { FormEvent, useState } from 'react'
import { api, unwrap } from '../api/client'
import { Link, useNavigate } from 'react-router-dom'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '', email: '', password: '', gender: 'other', dob: '1990-01-01', height_cm: 175, weight_kg: 75, activity_level: 'moderate'
  })
  const [error, setError] = useState<string | null>(null)

  function update<K extends keyof typeof form>(k: K, v: any) { setForm({ ...form, [k]: v }) }

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await api.post('/api/v1/auth/register', form)
      navigate('/login')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Register</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded p-2" placeholder="Name" value={form.name} onChange={e=>update('name', e.target.value)} />
        <input className="w-full border rounded p-2" placeholder="Email" value={form.email} onChange={e=>update('email', e.target.value)} />
        <input className="w-full border rounded p-2" placeholder="Password" type="password" value={form.password} onChange={e=>update('password', e.target.value)} />
        <div className="grid grid-cols-2 gap-2">
          <select className="border rounded p-2" value={form.gender} onChange={e=>update('gender', e.target.value)}>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          <input className="border rounded p-2" type="date" value={form.dob} onChange={e=>update('dob', e.target.value)} />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <input className="border rounded p-2" type="number" placeholder="Height (cm)" value={form.height_cm} onChange={e=>update('height_cm', Number(e.target.value))} />
          <input className="border rounded p-2" type="number" placeholder="Weight (kg)" value={form.weight_kg} onChange={e=>update('weight_kg', Number(e.target.value))} />
        </div>
        <select className="border rounded p-2 w-full" value={form.activity_level} onChange={e=>update('activity_level', e.target.value)}>
          <option value="sedentary">Sedentary</option>
          <option value="light">Light</option>
          <option value="moderate">Moderate</option>
          <option value="active">Active</option>
          <option value="very_active">Very Active</option>
        </select>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button className="bg-blue-600 text-white rounded px-4 py-2">Create account</button>
      </form>
      <p className="text-sm mt-3">Already have an account? <Link className="text-blue-600" to="/login">Login</Link></p>
    </div>
  )
}
