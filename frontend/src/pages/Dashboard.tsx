import { useQuery } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'

export default function Dashboard() {
  const { data } = useQuery({
    queryKey: ['summary'],
    queryFn: async () => unwrap<{ date: string, period: string, totals: any, target_calories?: number, progress?: number }>(
      await api.get('/api/v1/analytics/summary')
    )
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Calories Today</div>
          <div className="text-3xl font-bold">{data?.totals?.calories ?? 0}</div>
          <div className="text-sm">Target: {data?.target_calories ?? '—'}</div>
        </div>
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Macros (g)</div>
          <div>Protein: {data?.totals?.protein ?? 0}</div>
          <div>Carbs: {data?.totals?.carbs ?? 0}</div>
          <div>Fat: {data?.totals?.fat ?? 0}</div>
        </div>
        <div className="bg-white border rounded p-4">
          <div className="text-sm text-gray-500">Progress</div>
          <div className="w-full bg-gray-200 rounded h-3 overflow-hidden">
            <div className="bg-blue-600 h-3" style={{ width: `${Math.min(data?.progress ?? 0, 100)}%` }} />
          </div>
          <div className="text-sm mt-1">{data?.progress ? `${data.progress}%` : '—'}</div>
        </div>
      </div>
    </div>
  )
}
