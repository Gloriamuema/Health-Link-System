import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'
import { loadStripe } from '@stripe/stripe-js'

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || '')

export default function DoctorProfile(){
  const { id } = useParams()
  const [doc, setDoc] = useState(null)
  const [slotId, setSlotId] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchDoctor = async () => {
    try {
      const res = await api.get(`/doctors/${id}`)
      setDoc(res.data)
    } catch (e) {
      console.error(e)
      alert('Failed to load doctor')
    }
  }

  useEffect(()=>{ fetchDoctor() }, [id])

  const book = async (pay=false) => {
    if (!slotId) {
      alert('Select a slot to book')
      return
    }
    setLoading(true)
    try {
      const body = { doctor_id: doc.id, slot_id: slotId, pay }
      const token = localStorage.getItem('token')
      // Book appointment (requires auth)
      const res = await api.post('/appointments/book', body)
      if (res.data.payment_id && pay) {
        // create checkout session
        const checkout = await api.post('/payments/create-checkout-session', {
          appointment_id: res.data.appointment_id,
          amount: res.data.amount || doc.fee || doc.consultation_fee
        })
        // redirect to Stripe Checkout
        const stripe = await stripePromise
        const sessionId = checkout.data.sessionId
        await stripe.redirectToCheckout({ sessionId })
      } else {
        alert('Appointment created')
        fetchDoctor()
      }
    } catch (err) {
      console.error(err)
      alert(err?.response?.data?.message || 'Booking failed')
    } finally {
      setLoading(false)
    }
  }

  if (!doc) return <div>Loading...</div>

  return (
    <div>
      <div className="bg-white p-4 rounded shadow mb-4">
        <h2 className="text-xl font-semibold">{doc.name}</h2>
        <p className="text-sm text-gray-600">{doc.specialties}</p>
        <p className="mt-2">{doc.bio}</p>
        <div className="mt-3">
          <span className="text-lg font-bold">${doc.fee?.toFixed(2) || '0.00'}</span>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Available slots</h3>
        <div className="grid gap-2">
          {doc.slots && doc.slots.length ? doc.slots.map(s => (
            <label key={s.id} className={`p-2 border rounded cursor-pointer ${slotId===s.id ? 'bg-blue-50 border-blue-400' : ''}`}>
              <input type="radio" name="slot" value={s.id} onChange={()=>setSlotId(s.id)} className="mr-2" />
              {new Date(s.start).toLocaleString()} — {new Date(s.end).toLocaleTimeString()}
            </label>
          )) : <div className="text-sm text-gray-500">No slots available</div>}
        </div>

        <div className="mt-4 flex gap-2">
          <button onClick={()=>book(false)} className="px-4 py-2 bg-green-600 text-white rounded" disabled={loading}>Book (Free)</button>
          <button onClick={()=>book(true)} className="px-4 py-2 bg-blue-600 text-white rounded" disabled={loading}>
            Book & Pay ${doc.fee?.toFixed(2) || '0.00'}
          </button>
        </div>
      </div>
    </div>
  )
}
