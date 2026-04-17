import React from 'react'
import InteractionForm from './InteractionForm'
import ChatPanel from './ChatPanel'

export default function LogInteractionScreen() {
  return (
    <div className="min-h-screen bg-[#F0F2F5]" style={{ fontFamily: "'Inter', sans-serif" }}>

      {/* ── Page Content ─────────────────────────────────────────────────── */}
      <div className="max-w-screen-xl mx-auto px-6 py-6">

        {/* ── Page Title ───────────────────────────────────────────────── */}
        <h1 className="text-xl font-bold text-brand-black mb-5">Log HCP Interaction</h1>

        {/* ── Two column layout ────────────────────────────────────────── */}
        <div className="flex gap-5 items-start">

          {/* ── Left: Interaction Details Form ───────────────────────── */}
          <div className="flex-1 min-w-0 bg-white rounded-xl border border-brand-gray-200 shadow-card">
            {/* Card Header */}
            <div className="px-5 pt-4 pb-3 border-b border-brand-gray-100">
              <h2 className="text-sm font-semibold text-brand-black">Interaction Details</h2>
            </div>
            {/* Card Body */}
            <div className="px-5 py-4">
              <InteractionForm />
            </div>
          </div>

          {/* ── Right: AI Chat Panel ──────────────────────────────────── */}
          <div
            className="w-[300px] flex-shrink-0 bg-white rounded-xl border border-brand-gray-200 
                       shadow-card flex flex-col"
            style={{ height: 'calc(100vh - 110px)', maxHeight: '860px', minHeight: '500px' }}
          >
            <div className="flex flex-col h-full p-4">
              <ChatPanel />
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
