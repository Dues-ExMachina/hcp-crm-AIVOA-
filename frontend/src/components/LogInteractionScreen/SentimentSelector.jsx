import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { updateField } from '../../store/slices/interactionSlice'

const OPTIONS = [
  {
    value: 'Positive',
    label: 'Positive',
    icon: '😊',
    cls: 'sentiment-positive',
    activeCls: 'ring-2 ring-emerald-400',
  },
  {
    value: 'Neutral',
    label: 'Neutral',
    icon: '😐',
    cls: 'sentiment-neutral',
    activeCls: 'ring-2 ring-amber-400',
  },
  {
    value: 'Negative',
    label: 'Negative',
    icon: '😞',
    cls: 'sentiment-negative',
    activeCls: 'ring-2 ring-red-400',
  },
]

export default function SentimentSelector() {
  const dispatch = useDispatch()
  const sentiment = useSelector((s) => s.interaction.sentiment)

  return (
    <div className="flex gap-2">
      {OPTIONS.map((opt) => {
        const isActive = sentiment === opt.value
        return (
          <button
            key={opt.value}
            id={`sentiment-${opt.value.toLowerCase()}`}
            type="button"
            onClick={() => dispatch(updateField({ field: 'sentiment', value: opt.value }))}
            className={`
              flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg 
              text-xs font-medium border transition-all duration-150 cursor-pointer
              ${opt.cls}
              ${isActive ? opt.activeCls + ' shadow-sm' : 'opacity-60 hover:opacity-100'}
            `}
          >
            <span>{opt.icon}</span>
            <span>{opt.label}</span>
          </button>
        )
      })}
    </div>
  )
}
