import { useQuery } from '@tanstack/react-query'
import { api, unwrap } from '../api/client'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function Analytics() {
  const { data } = useQuery({
    queryKey: ['trends'],
    queryFn: async () => unwrap<{ series: any[] }>(await api.get('/api/v1/analytics/trends', { params: { range: 7 } }))
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Analytics</h1>
      <div className="bg-white border rounded p-4 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data?.series || []}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="calories" stroke="#2563eb" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
