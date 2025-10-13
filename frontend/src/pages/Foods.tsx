import { useQuery } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'
import { useState } from 'react'

export default function Foods() {
  const [query, setQuery] = useState('')
  const foods = useQuery({
    queryKey: ['foods', query],
    queryFn: async () => unwrap<{ items: any[] }>(await api.get('/api/v1/foods', { params: { query } })),
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Foods</h1>
      <input className="w-full border rounded p-2 mb-4" placeholder="Search foods" value={query} onChange={e=>setQuery(e.target.value)} />
      <div className="grid md:grid-cols-3 gap-3">
        {foods.data?.items?.map(f => (
          <div key={f.id} className="bg-white border rounded p-3">
            <div className="font-medium">{f.name}</div>
            <div className="text-sm text-gray-600">{f.calories} kcal • P {f.protein} • C {f.carbs} • F {f.fat}</div>
            <div className="text-xs text-gray-500 mt-1">{f.serving_size}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
