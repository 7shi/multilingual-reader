// Web Speech API shared utilities
// Voice filtering, automatic assignment, and asynchronous speech logic shared by reader.js / reader-multi.js

const MALE_NAMES = [
    "gerard", "thierry", "antoine", "jean", "remy", "henri", "fabrice",
    "david", "guy", "mark", "richard", "ryan", "brian", "christopher",
    "eric", "jacob", "benjamin", "ichiro", "keita", "yunjian",
];
const FEMALE_NAMES = [
    "charline", "sylvie", "vivienne", "denise", "eloise", "ariane",
    "aria", "jenny", "nancy", "sara", "jane", "michelle", "emma",
    "elizabeth", "amber", "ayumi", "haruka", "sayaka", "nanami",
    "xiaoxiao",
];

function isMaleVoice(voice) {
    const n = voice.name.toLowerCase();
    return n.includes("male") || n.includes("man") ||
        n.includes("homme") || n.includes("masculine") ||
        MALE_NAMES.some(x => n.includes(x));
}

function isFemaleVoice(voice) {
    const n = voice.name.toLowerCase();
    return n.includes("female") || n.includes("woman") ||
        n.includes("femme") || n.includes("feminine") ||
        FEMALE_NAMES.some(x => n.includes(x));
}

// Filters availableVoices down to those matching langCode, sorted by priority.
export function getFilteredVoicesForLang(availableVoices, langCode) {
    const targetBase = langCode.split("-")[0].toLowerCase();
    const matches = availableVoices.filter(v => v.lang.split("-")[0].toLowerCase() === targetBase);
    return prioritizeVoicesByRegion(matches, langCode);
}

// Excludes multilingual voices and orders by exact match → online → default → name.
function prioritizeVoicesByRegion(voices, targetLangCode) {
    if (voices.length === 0) return voices;
    const nonMultilingual = voices.filter(v => !v.name.toLowerCase().includes("multilingual"));
    const pool = nonMultilingual.length > 0 ? nonMultilingual : voices;
    const target = targetLangCode.toLowerCase();
    return pool.slice().sort((a, b) => {
        const aExact = a.lang.toLowerCase() === target;
        const bExact = b.lang.toLowerCase() === target;
        if (aExact !== bExact) return bExact - aExact;
        const aOnline = a.localService === false;
        const bOnline = b.localService === false;
        if (aOnline !== bOnline) return bOnline - aOnline;
        if (a.default !== b.default) return b.default - a.default;
        return a.name.localeCompare(b.name);
    });
}

// Auto-assigns voices, balancing male/female, only when speakerVoices has no assignments at all.
export function autoAssignDefaultVoices(speakerVoices, speakers, filteredVoices) {
    if (speakerVoices.some(v => v !== undefined) || filteredVoices.length === 0) return;

    const males = filteredVoices.filter(isMaleVoice);
    const females = filteredVoices.filter(isFemaleVoice);

    if (speakers.length >= 2 && males.length > 0 && females.length > 0) {
        let mi = 0, fi = 0;
        speakers.forEach((_, i) => {
            if (i % 2 === 0 && fi < females.length) speakerVoices[i] = females[fi++];
            else if (mi < males.length) speakerVoices[i] = males[mi++];
        });
    } else {
        speakers.forEach((_, i) => {
            if (i < filteredVoices.length) speakerVoices[i] = filteredVoices[i];
        });
    }
}

// Builds the candidate voice list for speakerIndex.
// Skips voices already used by other speakers, and puts the assigned voice first.
export function buildVoiceCandidates(speakerVoices, speakers, speakerIndex, filteredVoices) {
    const usedNames = new Set(
        speakerVoices.filter((v, i) => i !== speakerIndex && v).map(v => v.name)
    );
    const preferred = speakerVoices[speakerIndex];
    const rest = filteredVoices.filter(v => !usedNames.has(v.name) && (!preferred || v.name !== preferred.name));
    return preferred ? [preferred, ...rest] : rest;
}

// Speaks a single utterance and returns the result as a Promise.
// options: { onstart, onboundary, onUtterance }
// resolve: "ended" | "cancelled" | "synthesis-failed" | "error"
function speakOne(text, langCode, rate, voice, options) {
    const { onstart, onboundary, onUtterance } = options || {};
    return new Promise(resolve => {
        const utt = new SpeechSynthesisUtterance(text);
        utt.lang = langCode;
        utt.rate = rate;
        if (voice) utt.voice = voice;
        if (onstart) utt.onstart = onstart;
        if (onboundary) utt.onboundary = onboundary;
        utt.onend = () => resolve("ended");
        utt.onerror = e => {
            if (e.error === "canceled" || e.error === "interrupted") resolve("cancelled");
            else if (e.error === "synthesis-failed") resolve("synthesis-failed");
            else resolve("error");
        };
        if (onUtterance) onUtterance(utt);
        speechSynthesis.speak(utt);
    });
}

// Tries candidates in order starting from index vi, automatically retrying the next one on synthesis-failed.
// options: { vi, onstart, onboundary, onUtterance, onVoiceSuccess }
// onVoiceSuccess(voice) is called on speech start (once success is confirmed); the caller should update speakerVoices there.
// resolve: "ended" | "cancelled" | "error"
export async function speakWithRetry(text, langCode, rate, candidates, options) {
    const { vi = 0, onstart, onboundary, onUtterance, onVoiceSuccess } = options || {};

    const tryVoice = (voice) => {
        const wrappedOnstart = (onstart || onVoiceSuccess) ? () => {
            if (onVoiceSuccess && voice) onVoiceSuccess(voice);
            if (onstart) onstart();
        } : undefined;
        return speakOne(text, langCode, rate, voice, { onstart: wrappedOnstart, onboundary, onUtterance });
    };

    if (candidates.length === 0) {
        const r = await tryVoice(null);
        return r === "synthesis-failed" ? "error" : r;
    }
    for (let i = Math.max(0, vi); i < candidates.length; i++) {
        const r = await tryVoice(candidates[i]);
        if (r !== "synthesis-failed") return r;
    }
    return "error";
}
