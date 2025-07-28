import { Button } from '@/components/ui/button'
import { PreferencesDialog } from '@/components/PreferencesDialog'
import type { Preferences } from '@/types'

interface HeaderProps {
    preferences: Preferences
    onUpdatePreferences: (prefs: Preferences) => void
    onClearChat: () => void
    hasMessages: boolean
}

export function Header({ preferences, onUpdatePreferences, onClearChat, hasMessages }: HeaderProps) {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-slate-950/80 backdrop-blur-xl supports-[backdrop-filter]:bg-slate-950/60 transition-all duration-200">
            <div className="flex h-16 items-center justify-between px-6 max-w-7xl mx-auto w-full">
                {/* Logo Section */}
                <div className="flex items-center gap-4 group">
                    <div className="relative w-9 h-9">
                        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-orange-500 to-amber-600 opacity-90 group-hover:opacity-100 transition-opacity duration-300 shadow-[0_0_15px_-3px_rgba(249,115,22,0.4)]" />
                        <div className="absolute inset-[1px] rounded-[11px] bg-slate-950/90 flex items-center justify-center">
                            <span className="text-lg font-bold bg-gradient-to-br from-orange-400 to-amber-200 bg-clip-text text-transparent">M</span>
                        </div>
                    </div>
                    <div className="flex flex-col">
                        <h1 className="text-base font-semibold text-white tracking-tight leading-none group-hover:text-orange-100 transition-colors">
                            Maanasa
                        </h1>
                        <span className="text-[10px] uppercase tracking-wider font-medium text-slate-500 group-hover:text-slate-400 transition-colors">
                            Indian Food Expert
                        </span>
                    </div>
                </div>

                {/* Actions Section */}
                <div className="flex items-center gap-3">
                    <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/50 border border-white/5 mx-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-xs font-medium text-slate-400">System Online</span>
                    </div>

                    <div className="h-6 w-px bg-white/10 mx-2" />

                    <PreferencesDialog preferences={preferences} onUpdate={onUpdatePreferences} />

                    {hasMessages && (
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={onClearChat}
                            className="text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors duration-200 text-xs font-medium"
                        >
                            Clear Chat
                        </Button>
                    )}
                </div>
            </div>
        </header>
    )
}
