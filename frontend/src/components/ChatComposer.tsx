import { useState, useRef, type KeyboardEvent } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

interface Props {
    onSend: (message: string) => void
    disabled?: boolean
}

export function ChatComposer({ onSend, disabled }: Props) {
    const [input, setInput] = useState('')
    const textareaRef = useRef<HTMLTextAreaElement>(null)

    const handleSend = () => {
        if (!input.trim() || disabled) return
        onSend(input.trim())
        setInput('')
        textareaRef.current?.focus()
    }

    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
    return (
        <div className="flex gap-3">
            <div className="flex-1 relative">
                <Textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about Indian dishes, ingredients, or get recommendations..."
                    disabled={disabled}
                    className="min-h-[56px] max-h-32 resize-none bg-slate-800/60 border-slate-700/50 focus:border-orange-500/50 focus:ring-orange-500/20 text-white placeholder:text-slate-500 rounded-xl pr-4"
                    rows={1}
                />
            </div>
            <Button
                onClick={handleSend}
                disabled={disabled || !input.trim()}
                className="h-14 w-14 rounded-xl bg-gradient-to-br from-orange-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 text-white shadow-lg shadow-orange-500/20 disabled:opacity-50 disabled:shadow-none"
            >
                {disabled ? (
                    <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                )}
            </Button>
            )
}
