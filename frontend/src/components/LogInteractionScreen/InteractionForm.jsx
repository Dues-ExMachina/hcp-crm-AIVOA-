import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { updateField, addTag, removeTag, saveInteraction, resetForm } from '../../store/slices/interactionSlice'
import HCPSearchInput from '../shared/HCPSearchInput'
import Spinner from '../shared/Spinner'

// ── Sentiment Radio ───────────────────────────────────────────────────────────
const SENTIMENTS = [
  { value: 'Positive', emoji: '😊' },
  { value: 'Neutral',  emoji: '😐' },
  { value: 'Negative', emoji: '😞' },
]

function SentimentRadio() {
  const dispatch = useDispatch()
  const sentiment = useSelector((s) => s.interaction.sentiment)
  return (
    <div className="flex items-center gap-5">
      {SENTIMENTS.map((s) => (
        <label key={s.value} className="flex items-center gap-1.5 cursor-pointer select-none">
          <input
            type="radio"
            name="sentiment"
            id={`sentiment-${s.value.toLowerCase()}`}
            value={s.value}
            checked={sentiment === s.value}
            onChange={() => dispatch(updateField({ field: 'sentiment', value: s.value }))}
            className="accent-brand-black w-3.5 h-3.5 cursor-pointer"
          />
          <span className="text-base">{s.emoji}</span>
          <span className="text-sm text-brand-gray-700">{s.value}</span>
        </label>
      ))}
    </div>
  )
}

// ── Materials Row ─────────────────────────────────────────────────────────────
function MaterialsRow({ field, label, buttonLabel, buttonIcon, placeholder, id }) {
  const dispatch = useDispatch()
  const tags = useSelector((s) => s.interaction[field])
  const [input, setInput] = useState('')
  const [adding, setAdding] = useState(false)

  const handleAdd = () => {
    if (input.trim()) {
      dispatch(addTag({ field, value: input.trim() }))
      setInput('')
      setAdding(false)
    }
  }

  return (
    <div className="border border-brand-gray-200 rounded-lg p-3 bg-white">
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium text-brand-black">{label}</span>
        <button
          type="button"
          id={id}
          onClick={() => setAdding(true)}
          className="flex items-center gap-1.5 text-xs font-medium text-brand-gray-600 
                     border border-brand-gray-200 rounded-md px-2.5 py-1 hover:border-brand-gray-400 
                     hover:bg-brand-gray-50 transition-all"
        >
          <span className="text-sm">{buttonIcon}</span>
          {buttonLabel}
        </button>
      </div>

      {tags.length === 0 && !adding && (
        <p className="text-xs text-brand-gray-400 italic">{placeholder}</p>
      )}

      {tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-1.5">
          {tags.map((tag, i) => (
            <span key={i} className="inline-flex items-center gap-1 rounded-full bg-brand-gray-100 
                                     px-2.5 py-0.5 text-xs font-medium text-brand-gray-700">
              {tag}
              <button
                type="button"
                onClick={() => dispatch(removeTag({ field, index: i }))}
                className="text-brand-gray-400 hover:text-brand-black"
              >×</button>
            </span>
          ))}
        </div>
      )}

      {adding && (
        <div className="flex gap-2 mt-2">
          <input
            autoFocus
            type="text"
            className="crm-input flex-1 text-sm"
            placeholder={`Add ${label.toLowerCase()}...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAdd() } }}
          />
          <button type="button" onClick={handleAdd} className="btn-primary px-3 py-1.5 text-xs">Add</button>
          <button type="button" onClick={() => { setAdding(false); setInput('') }} 
                  className="btn-secondary px-3 py-1.5 text-xs">Cancel</button>
        </div>
      )}
    </div>
  )
}

// ── Main Form ────────────────────────────────────────────────────────────────
export default function InteractionForm() {
  const dispatch = useDispatch()
  const form = useSelector((s) => s.interaction)

  const handleSubmit = (e) => {
    e.preventDefault()
    dispatch(saveInteraction(form))
  }

  const isLoading = form.status === 'loading'
  const isSuccess = form.status === 'success'
  const aiFollowups = form.aiSuggestedFollowups || []

  return (
    <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in">

      {/* ── Success Banner ───────────────────────────────────────────────── */}
      {isSuccess && (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 flex items-center gap-2 animate-slide-up">
          <span className="text-emerald-500">✅</span>
          <p className="text-sm font-medium text-emerald-800">Interaction saved successfully!</p>
          <button type="button" onClick={() => dispatch(resetForm())}
                  className="ml-auto text-xs text-emerald-600 underline">
            Log another
          </button>
        </div>
      )}

      {form.status === 'error' && (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3">
          <p className="text-sm text-red-800">⚠️ {form.error}</p>
        </div>
      )}

      {/* ── Row 1: HCP Name + Interaction Type ──────────────────────────── */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-brand-gray-800 mb-1">HCP Name</label>
          <HCPSearchInput />
        </div>
        <div>
          <label className="block text-sm font-medium text-brand-gray-800 mb-1">Interaction Type</label>
          <select
            id="interaction-type"
            className="crm-input"
            value={form.interactionType}
            onChange={(e) => dispatch(updateField({ field: 'interactionType', value: e.target.value }))}
          >
            {['Meeting', 'Call', 'Email', 'Conference'].map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </div>
      </div>

      {/* ── Row 2: Date + Time ───────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-brand-gray-800 mb-1">Date</label>
          <input
            id="interaction-date"
            type="date"
            className="crm-input"
            value={form.date}
            onChange={(e) => dispatch(updateField({ field: 'date', value: e.target.value }))}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-brand-gray-800 mb-1">Time</label>
          <input
            id="interaction-time"
            type="time"
            className="crm-input"
            value={form.time}
            onChange={(e) => dispatch(updateField({ field: 'time', value: e.target.value }))}
          />
        </div>
      </div>

      {/* ── Row 3: Attendees ─────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-1">Attendees</label>
        <input
          id="attendees-input"
          type="text"
          className="crm-input"
          placeholder="Enter names or search..."
          value={Array.isArray(form.attendees) ? form.attendees.join(', ') : form.attendees}
          onChange={(e) => dispatch(updateField({ field: 'attendees', value: e.target.value.split(',').map(s => s.trim()).filter(Boolean) }))}
        />
      </div>

      {/* ── Row 4: Topics Discussed ──────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-1">Topics Discussed</label>
        <div className="relative">
          <textarea
            id="topics-discussed"
            className="crm-input min-h-[90px] resize-y pr-8"
            placeholder="Enter key discussion points..."
            value={form.topicsDiscussed}
            onChange={(e) => dispatch(updateField({ field: 'topicsDiscussed', value: e.target.value }))}
          />
          <span className="absolute bottom-2.5 right-2.5 text-brand-gray-400 pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
              <line x1="12" y1="19" x2="12" y2="23"/>
              <line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
          </span>
        </div>
      </div>

      {/* ── Voice Note Button ────────────────────────────────────────────── */}
      <div>
        <button
          type="button"
          id="voice-note-btn"
          className="flex items-center gap-2 text-xs font-medium text-brand-gray-600 border border-brand-gray-200 
                     rounded-lg px-4 py-2 hover:border-brand-gray-400 hover:bg-brand-gray-50 transition-all"
        >
          <span className="text-sm">🔊</span>
          Summarize from Voice Note (Requires Consent)
        </button>
      </div>

      {/* ── Materials Shared / Samples Distributed ───────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-2">
          Materials Shared / Samples Distributed
        </label>
        <div className="space-y-2">
          <MaterialsRow
            field="materialsShared"
            label="Materials Shared"
            buttonLabel="Search/Add"
            buttonIcon="🔍"
            placeholder="No materials added."
            id="materials-add-btn"
          />
          <MaterialsRow
            field="samplesDistributed"
            label="Samples Distributed"
            buttonLabel="Add Sample"
            buttonIcon="💊"
            placeholder="No samples added."
            id="samples-add-btn"
          />
        </div>
      </div>

      {/* ── Sentiment ────────────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-2">
          Observed/Inferred HCP Sentiment
        </label>
        <SentimentRadio />
      </div>

      {/* ── Outcomes ─────────────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-1">Outcomes</label>
        <div className="relative">
          <textarea
            id="outcomes"
            className="crm-input min-h-[80px] resize-y"
            placeholder="Key outcomes or agreements..."
            value={form.outcomes}
            onChange={(e) => dispatch(updateField({ field: 'outcomes', value: e.target.value }))}
          />
        </div>
      </div>

      {/* ── Follow-up Actions ────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-brand-gray-800 mb-1">Follow-up Actions</label>
        <div className="relative">
          <textarea
            id="follow-up-actions"
            className="crm-input min-h-[80px] resize-y"
            placeholder="Enter next steps or tasks..."
            value={form.followUpActions}
            onChange={(e) => dispatch(updateField({ field: 'followUpActions', value: e.target.value }))}
          />
        </div>
      </div>

      {/* ── AI Suggested Follow-ups ──────────────────────────────────────── */}
      {aiFollowups.length > 0 && (
        <div className="animate-slide-up">
          <p className="text-sm font-semibold text-brand-gray-800 mb-1">AI Suggested Follow-ups:</p>
          <ul className="space-y-0.5">
            {aiFollowups.map((item, i) => (
              <li key={i} className="flex items-baseline gap-1">
                <span className="text-blue-500 text-xs font-bold flex-shrink-0">+</span>
                <span className="text-xs text-blue-600 hover:text-blue-800 hover:underline cursor-pointer leading-snug">
                  {item}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── AI Summary ───────────────────────────────────────────────────── */}
      {form.aiSummary && (
        <div className="rounded-lg border border-brand-gray-200 bg-brand-gray-50 p-3 animate-slide-up">
          <p className="text-xs font-semibold text-brand-gray-600 mb-1">✨ AI Summary</p>
          <p className="text-xs text-brand-gray-600 leading-relaxed">{form.aiSummary}</p>
        </div>
      )}

      {/* ── Save Button ──────────────────────────────────────────────────── */}
      <div className="flex gap-3 pt-2 border-t border-brand-gray-100">
        <button
          id="save-interaction-btn"
          type="submit"
          className="btn-primary flex-1"
          disabled={isLoading || !form.date}
        >
          {isLoading ? <><Spinner size="sm" /> Saving...</> : <>✓ Save Interaction</>}
        </button>
        <button
          id="reset-form-btn"
          type="button"
          className="btn-secondary"
          onClick={() => dispatch(resetForm())}
        >
          Reset
        </button>
      </div>
    </form>
  )
}
