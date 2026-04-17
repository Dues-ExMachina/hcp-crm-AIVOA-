import React from 'react'
import { useSelector } from 'react-redux'

export default function AISuggestedFollowups() {
  const { aiSuggestedFollowups, aiSummary } = useSelector((s) => s.interaction)

  if (!aiSuggestedFollowups?.length && !aiSummary) return null

  return (
    <div className="animate-slide-up space-y-4">
      {/* AI Summary */}
      {aiSummary && (
        <div className="rounded-lg border border-brand-gray-200 bg-brand-gray-50 p-3">
          <div className="flex items-center gap-1.5 mb-2">
            <span className="text-sm">✨</span>
            <span className="text-xs font-semibold text-brand-gray-700 uppercase tracking-wide">
              AI Summary
            </span>
          </div>
          <p className="text-xs text-brand-gray-600 leading-relaxed">{aiSummary}</p>
        </div>
      )}

      {/* Suggested Follow-ups */}
      {aiSuggestedFollowups?.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 mb-2.5">
            <span className="text-sm">💡</span>
            <span className="text-xs font-semibold text-brand-gray-700 uppercase tracking-wide">
              AI Suggested Follow-ups
            </span>
          </div>
          <ul className="space-y-1.5">
            {aiSuggestedFollowups.map((item, i) => (
              <li
                key={i}
                className="flex items-start gap-2 rounded-lg border border-brand-gray-100 
                           bg-white px-3 py-2 text-xs text-brand-gray-700 shadow-card"
              >
                <span className="mt-0.5 flex-shrink-0 h-4 w-4 rounded-full bg-brand-black 
                                 text-white text-[10px] flex items-center justify-center font-semibold">
                  {i + 1}
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
