import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'
import { useState } from 'react'

export default function Meals() {
  const qc = useQueryClient()
  const [query, setQuery] = useState('')
  const [selectedFood, setSelectedFood] = useState<any | null>(null)
  const [quantity, setQuantity] = useState(1)
  const [mealType, setMealType] = useState('breakfast')

  const foods = useQuery({
    queryKey: ['foods', query],
    queryFn: async () => unwrap<{ items: any[] }>(await api.get('/api/v1/foods', { params: { query } })),
  })

  const meals = useQuery({
    queryKey: ['meals'],
    queryFn: async () => unwrap<{ items: any[] }>(await api.get('/api/v1/meals')),
  })

  const addMeal = useMutation({
    mutationFn: async () => unwrap(await api.post('/api/v1/meals', { food_id: selectedFood.id, quantity, meal_type: mealType })),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['meals'] }) }
  })

  const delMeal = useMutation({
    mutationFn: async (id: string) => unwrap(await api.delete(`/api/v1/meals/${id}`)),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['meals'] }) }
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Meals</h1>
      <div className="bg-white border rounded p-4 space-y-3">
        <input className="w-full border rounded p-2" placeholder="Search foods" value={query} onChange={e=>setQuery(e.target.value)} />
        {foods.data?.items && (
          <div className="grid md:grid-cols-3 gap-2">
            {foods.data.items.map(f => (
              <button key={f.id} className={`border rounded p-2 text-left ${selectedFood?.id === f.id ? 'border-blue-600' : ''}`} onClick={()=>setSelectedFood(f)}>
                <div className="font-medium">{f.name}</div>
                <div className="text-xs text-gray-500">{f.calories} kcal • P {f.protein} • C {f.carbs} • F {f.fat}</div>
              </button>
            ))}
          </div>
        )}
        <div className="grid grid-cols-3 gap-2">
          <select className="border rounded p-2" value={mealType} onChange={e=>setMealType(e.target.value)}>
            <option>breakfast</option>
            <option>lunch</option>
            <option>dinner</option>
            <option>snacks</option>
          </select>
          <input className="border rounded p-2" type="number" min={0.1} step={0.1} value={quantity} onChange={e=>setQuantity(Number(e.target.value))} />
          <button className="bg-blue-600 text-white rounded px-4" disabled={!selectedFood} onClick={()=>addMeal.mutate()}>Add Meal</button>
        </div>
      </div>

      <h2 className="text-xl font-semibold mt-6 mb-2">Today's Meals</h2>
      <div className="space-y-2">
        {meals.data?.items?.map(m => (
          <div key={m.id} className="bg-white border rounded p-3 flex items-center justify-between">
            <div>
              <div className="font-medium capitalize">{m.meal_type}</div>
              <div className="text-sm text-gray-600">{m.items.map((i:any)=>i.name).join(', ')}</div>
              <div className="text-sm">{m.totals.calories} kcal • P {m.totals.protein} • C {m.totals.carbs} • F {m.totals.fat}</div>
            </div>
            <button className="text-red-600" onClick={()=>delMeal.mutate(m.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  )
}
