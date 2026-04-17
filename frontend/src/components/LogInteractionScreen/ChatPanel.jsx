import React, { useEffect, useRef, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { sendMessage, addUserMessage, clearChat } from '../../store/slices/chatSlice'
import Spinner from '../shared/Spinner'

function TypingIndicator() {
  return (
    <div className="flex items-end gap-1 px-3 py-2.5 bg-brand-gray-100 rounded-2xl rounded-bl-none w-fit">
      <div className="typing-dot" />
      <div className="typing-dot" />
      <div className="typing-dot" />
    </div>
  )
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user'

  const renderContent = (text) => {
    if (!text) return null
    return text.split('\n').map((line, i) => {
      const parts = line.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g)
      return (
        <span key={i}>
          {parts.map((part, j) => {
            if (part.startsWith('**') && part.endsWith('**')) return <strong key={j}>{part.slice(2, -2)}</strong>
            if (part.startsWith('*') && part.endsWith('*')) return <em key={j}>{part.slice(1, -1)}</em>
            return part
          })}
          {i < text.split('\n').length - 1 && <br />}
        </span>
      )
    })
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
      <div
        className={`
          max-w-[88%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed
          ${isUser
            ? 'bg-brand-black text-white rounded-br-none'
            : 'bg-brand-gray-100 text-brand-black rounded-bl-none'
          }
        `}
      >
        {renderContent(msg.content)}
      </div>
    </div>
  )
}

export default function ChatPanel() {
  const dispatch = useDispatch()
  const { messages, isLoading } = useSelector((s) => s.chat)
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSend = () => {
    const msg = input.trim()
    if (!msg || isLoading) return
    
    // Format chat history for backend (excluding the welcome message and trimming unnecessary data)
    const chatHistory = messages
      .filter(m => m.id !== 0) // Skip welcome message
      .map(m => ({ role: m.role, content: m.content }))

    dispatch(addUserMessage(msg))
    dispatch(sendMessage({ message: msg, chatHistory }))
    setInput('')
    textareaRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 mb-3 pb-3 border-b border-brand-gray-100">
        <div className="h-7 w-7 rounded-full bg-blue-100 flex items-center justify-center text-base">
          🤖
        </div>
        <div>
          <p className="text-sm font-semibold text-brand-black">AI Assistant</p>
          <p className="text-[11px] text-brand-gray-400">Log interaction via chat</p>
        </div>
        <button
          id="clear-chat-btn"
          type="button"
          onClick={() => dispatch(clearChat())}
          className="ml-auto text-[11px] text-brand-gray-400 hover:text-brand-black transition-colors"
        >
          Clear
        </button>
      </div>

      {/* ── Messages ───────────────────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto space-y-2.5 pr-0.5 min-h-0">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} msg={msg} />
        ))}
        {isLoading && (
          <div className="flex justify-start animate-fade-in">
            <TypingIndicator />
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* ── Input ──────────────────────────────────────────────────────── */}
      <div className="mt-3 border-t border-brand-gray-100 pt-3 flex gap-2 items-center">
        <input
          id="chat-input"
          ref={textareaRef}
          type="text"
          className="crm-input flex-1 text-sm"
          placeholder="Describe interaction..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          id="chat-send-btn"
          type="button"
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className="flex-shrink-0 flex items-center gap-1.5 bg-brand-black text-white text-xs font-semibold 
                     px-4 py-2.5 rounded-lg hover:bg-brand-gray-800 disabled:opacity-40 
                     disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? <Spinner size="sm" /> : <span>⚡</span>}
          Log
        </button>
      </div>
    </div>
  )
}
