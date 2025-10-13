import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'
import { useState } from 'react'

export default function Goals() {
  const qc = useQueryClient()
  const goal = useQuery({ queryKey: ['goal'], queryFn: async ()=> unwrap(await api.get('/api/v1/goals')) })
  const [goalType, setGoalType] = useState('maintain')
  const [target, setTarget] = useState<number | ''>('')

  const save = useMutation({
    mutationFn: async () => unwrap(await api.post('/api/v1/goals', { goal_type: goalType, target_calories: target === '' ? undefined : Number(target) })),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['goal'] })
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Goals</h1>
      <div className="bg-white border rounded p-4 space-y-3 max-w-md">
        <select className="border rounded p-2 w-full" value={goalType} onChange={e=>setGoalType(e.target.value)}>
          <option value="loss">Lose weight</option>
          <option value="maintain">Maintain</option>
          <option value="gain">Gain weight</option>
        </select>
        <input className="border rounded p-2 w-full" type="number" placeholder="Target calories (optional)" value={target} onChange={e=>setTarget(e.target.value === '' ? '' : Number(e.target.value))} />
        <button className="bg-blue-600 text-white rounded px-4 py-2" onClick={()=>save.mutate()}>Save</button>
      </div>
      {goal.data && (
        <div className="mt-6">
          <div className="text-sm text-gray-600">Current target: {goal.data.target_calories ?? '—'}</div>
        </div>
      )}
    </div>
  )
}
