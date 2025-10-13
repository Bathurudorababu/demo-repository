import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import App from '../App'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

it('renders app shell', () => {
  const qc = new QueryClient()
  const { getByText } = render(
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  )
  expect(getByText('Calorie Tracker')).toBeInTheDocument()
})
