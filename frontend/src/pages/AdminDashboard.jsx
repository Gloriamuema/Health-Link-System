import React, { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import api from '../api'

export default function AdminDashboard(){
  const [summary, setSummary] = useState(null)

  useEffect(()=>{
    const fetch = async ()=>{
      try {
        const res = await api.get('/admin/reports')  // you'll implement this endpoint
        setSummary(res.data)
      } catch(e) {
        console.error(e)
      }
    }
    fetch()
  }, [])

  if (!summary) return <div>Loading...</div>

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold">Overview</h3>
        <div className="grid grid-cols-3 gap-4 mt-2">
          <div className="p-3 bg-gray-50 rounded">Appointments: {summary.appointments_count}</div>
          <div className="p-3 bg-gray-50 rounded">Revenue: ${summary.revenue.toFixed(2)}</div>
          <div className="p-3 bg-gray-50 rounded">Doctors: {summary.doctors_count}</div>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Appointments trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={summary.appointments_series || []}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#3182ce" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}