import type { Preferences } from '@/types'

interface Props {
    preferences: Preferences
}

const SPICE_LABELS: Record<string, string> = {
    mild: 'Mild',
    medium: 'Medium',
    spicy: 'Spicy',
    extra_spicy: 'Extra Hot',
}

const CUISINE_LABELS: Record<string, string> = {
    south_indian: 'South Indian',
    north_indian: 'North Indian',
    gujarati: 'Gujarati',
    bengali: 'Bengali',
    rajasthani: 'Rajasthani',
    maharashtrian: 'Maharashtrian',
}

export function PreferencesSummary({ preferences }: Props) {
    const hasPreferences =
        preferences.allergies.length > 0 ||
        preferences.health_goals.length > 0 ||
        preferences.preferred_cuisines.length > 0

    if (!hasPreferences && preferences.spice_level === 'medium') {
        return null
    }

    return (
        <div className="px-6 py-3 bg-slate-900/50 border-b border-slate-800/50">
            <div className="max-w-3xl mx-auto flex flex-wrap items-center gap-2 text-xs">
                <span className="text-slate-500">Active filters:</span>

                {/* Spice Level */}
                <span className="px-2 py-1 rounded-md bg-orange-500/10 text-orange-400 border border-orange-500/20">
                    {SPICE_LABELS[preferences.spice_level] || preferences.spice_level} spice
                </span>

                {/* Cuisines */}
                {preferences.preferred_cuisines.slice(0, 2).map(c => (
                    <span key={c} className="px-2 py-1 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {CUISINE_LABELS[c] || c}
                    </span>
                ))}
                {preferences.preferred_cuisines.length > 2 && (
                    <span className="px-2 py-1 rounded-md bg-slate-800 text-slate-400">
                        +{preferences.preferred_cuisines.length - 2} more
                    </span>
                )}

                {/* Allergies */}
                {preferences.allergies.map(a => (
                    <span key={a} className="px-2 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20 flex items-center gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                        </svg>
                        No {a}
                    </span>
                ))}

                {/* Health Goals */}
                {preferences.health_goals.slice(0, 2).map(g => (
                    <span key={g} className="px-2 py-1 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20">
                        {g.replace('_', ' ')}
                    </span>
                ))}
            </div>
        </div>
    )
}
