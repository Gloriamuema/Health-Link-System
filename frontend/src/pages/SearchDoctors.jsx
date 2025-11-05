import React, { useEffect, useState } from 'react'
import api from '../api'
import { Link } from 'react-router-dom'

export default function SearchDoctors(){
  const [q, setQ] = useState('')
  const [results, setResults] = useState([])

  const search = async () => {
    try {
      const res = await api.get('/doctors', { params: { q } })
      setResults(res.data)
    } catch (e) {
      console.error(e)
      alert('Search failed')
    }
  }

  useEffect(() => { search() }, [])

  return (
    <div>
      <div className="mb-4 flex gap-2">
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search by name or specialty" className="flex-1 p-2 border" />
        <button onClick={search} className="px-4 py-2 bg-blue-600 text-white rounded">Search</button>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        {results.map(d => (
          <div key={d.id} className="p-4 bg-white rounded shadow">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold">{d.name}</h3>
                <p className="text-sm text-gray-600">{d.specialties}</p>
                <p className="text-xs text-gray-500">{d.location}</p>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold">${d.fee?.toFixed(2) || '0.00'}</div>
                <div className="text-xs text-gray-500">Rating: {d.rating || '—'}</div>
              </div>
            </div>
            <div className="mt-3 flex gap-2">
              <Link to={`/doctor/${d.id}`} className="px-3 py-2 bg-white border rounded">View</Link>
              <a href={`/doctor/${d.id}`} className="px-3 py-2 bg-blue-600 text-white rounded">Book</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
