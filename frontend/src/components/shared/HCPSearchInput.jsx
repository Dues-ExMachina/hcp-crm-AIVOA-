import React, { useState, useRef, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchHCPs, clearResults } from '../../store/slices/hcpSlice'
import { updateField } from '../../store/slices/interactionSlice'

export default function HCPSearchInput() {
  const dispatch = useDispatch()
  const { results, isLoading } = useSelector((s) => s.hcp)
  const hcpName = useSelector((s) => s.interaction.hcpName)

  const [query, setQuery] = useState(hcpName || '')
  const [open, setOpen] = useState(false)
  const wrapRef = useRef(null)
  const debounceRef = useRef(null)

  // Sync external changes (from chat AI)
  useEffect(() => {
    setQuery(hcpName || '')
  }, [hcpName])

  const handleChange = (e) => {
    const val = e.target.value
    setQuery(val)
    dispatch(updateField({ field: 'hcpName', value: val }))
    dispatch(updateField({ field: 'hcpId', value: null }))

    clearTimeout(debounceRef.current)
    if (val.length >= 2) {
      debounceRef.current = setTimeout(() => {
        dispatch(fetchHCPs(val))
        setOpen(true)
      }, 300)
    } else {
      dispatch(clearResults())
      setOpen(false)
    }
  }

  const handleSelect = (hcp) => {
    setQuery(hcp.name)
    dispatch(updateField({ field: 'hcpName', value: hcp.name }))
    dispatch(updateField({ field: 'hcpId', value: hcp.id }))
    dispatch(clearResults())
    setOpen(false)
  }

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div className="relative" ref={wrapRef}>
      <div className="relative">
        <input
          id="hcp-search-input"
          type="text"
          className="crm-input pr-8"
          placeholder="Search HCP name..."
          value={query}
          onChange={handleChange}
          onFocus={() => results.length > 0 && setOpen(true)}
          autoComplete="off"
        />
        {isLoading && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2">
            <svg className="animate-spin h-4 w-4 text-brand-gray-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          </span>
        )}
      </div>

      {open && results.length > 0 && (
        <ul className="absolute z-50 mt-1 w-full bg-white border border-brand-gray-200 rounded-lg shadow-card-hover overflow-hidden animate-fade-in">
          {results.map((hcp) => (
            <li
              key={hcp.id}
              className="px-3 py-2.5 cursor-pointer hover:bg-brand-gray-50 transition-colors border-b border-brand-gray-100 last:border-0"
              onMouseDown={() => handleSelect(hcp)}
            >
              <div className="text-sm font-medium text-brand-black">{hcp.name}</div>
              <div className="text-xs text-brand-gray-500 mt-0.5">
                {hcp.specialty} · {hcp.territory}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
