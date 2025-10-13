import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'
import { useState } from 'react'

export default function Profile() {
  const qc = useQueryClient()
  const user = useQuery({ queryKey: ['me'], queryFn: async ()=> unwrap(await api.get('/api/v1/auth/me')) })
  const [form, setForm] = useState<any>({})

  const save = useMutation({
    mutationFn: async () => unwrap(await api.patch('/api/v1/auth/update', form)),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['me'] })
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Profile</h1>
      <div className="bg-white border rounded p-4 space-y-3 max-w-md">
        <input className="border rounded p-2 w-full" placeholder="Name" defaultValue={user.data?.name} onChange={e=>setForm({ ...form, name: e.target.value })} />
        <div className="grid grid-cols-2 gap-2">
          <select className="border rounded p-2" defaultValue={user.data?.gender} onChange={e=>setForm({ ...form, gender: e.target.value })}>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          <input className="border rounded p-2" type="date" defaultValue={user.data?.dob} onChange={e=>setForm({ ...form, dob: e.target.value })} />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <input className="border rounded p-2" type="number" placeholder="Height (cm)" defaultValue={user.data?.height_cm} onChange={e=>setForm({ ...form, height_cm: Number(e.target.value) })} />
          <input className="border rounded p-2" type="number" placeholder="Weight (kg)" defaultValue={user.data?.weight_kg} onChange={e=>setForm({ ...form, weight_kg: Number(e.target.value) })} />
        </div>
        <select className="border rounded p-2 w-full" defaultValue={user.data?.activity_level} onChange={e=>setForm({ ...form, activity_level: e.target.value })}>
          <option value="sedentary">Sedentary</option>
          <option value="light">Light</option>
          <option value="moderate">Moderate</option>
          <option value="active">Active</option>
          <option value="very_active">Very Active</option>
        </select>
        <button className="bg-blue-600 text-white rounded px-4 py-2" onClick={()=>save.mutate()}>Save</button>
      </div>
    </div>
  )
}
