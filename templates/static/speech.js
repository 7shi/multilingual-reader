// Web Speech API 共通ユーティリティ
// reader.js / reader-multi.js で共有する音声フィルタリング・自動割り当て・非同期発話ロジック

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

// availableVoices から langCode に対応する音声を絞り込み、優先順に並べて返す。
export function getFilteredVoicesForLang(availableVoices, langCode) {
    const targetBase = langCode.split("-")[0].toLowerCase();
    const matches = availableVoices.filter(v => v.lang.split("-")[0].toLowerCase() === targetBase);
    return prioritizeVoicesByRegion(matches, langCode);
}

// multilingual 音声を除外し、完全一致 → オンライン → デフォルト → 名前順で並べる。
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

// speakerVoices に未割り当てがある場合のみ、男女バランスを考慮して自動割り当てする。
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

// speakerIndex の候補音声リストを構築する。
// 他スピーカーが使用中の音声はスキップし、割り当て済み音声を先頭に配置する。
export function buildVoiceCandidates(speakerVoices, speakers, speakerIndex, filteredVoices) {
    const usedNames = new Set(
        speakerVoices.filter((v, i) => i !== speakerIndex && v).map(v => v.name)
    );
    const preferred = speakerVoices[speakerIndex];
    const rest = filteredVoices.filter(v => !usedNames.has(v.name) && (!preferred || v.name !== preferred.name));
    return preferred ? [preferred, ...rest] : rest;
}

// 単一の utterance を発話し、結果を Promise で返す非同期関数。
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

// candidates を vi 番目から順に試し、synthesis-failed の場合は自動的に次へリトライする。
// options: { vi, onstart, onboundary, onUtterance, onVoiceSuccess }
// onVoiceSuccess(voice) は発話開始時（成功確定時）に呼ばれる。呼び出し元で speakerVoices を更新すること。
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
