// Multilingual Podcast Reader - logic for the multilingual parallel mode
// Loads the page-config JSON and the .translation-group elements rendered by the template,
// displaying all 6 languages' translations at once while reading aloud only the enabled languages in sequence.

import { getFilteredVoicesForLang, autoAssignDefaultVoices, buildVoiceCandidates, speakWithRetry } from './speech.js';

const config = JSON.parse(document.getElementById("page-config").textContent);
const languages = config.languages;
const speakers = config.speakers;

const RATE_STORAGE_KEY = `multilingualReader.langRates.${config.topic}`;

// Per-language state
const langStates = {};
languages.forEach(L => {
    langStates[L.code] = {
        ...L,
        rate: L.default_rate,
        enabled: true,
        speakerVoices: new Array(speakers.length).fill(undefined),
    };
});

let availableVoices = [];
let currentSynth = null;
let speechGeneration = 0;
let isPaused = false;
let isStopped = false;
let currentGroupIndex = 0;
let currentStep = 0;

let groups = [];

let playPauseBtn, stopBtn, rateSlider, rateValue;
let statusEl, textContent, speakerVoicesDiv, languageControlsContainer;

function init() {
    playPauseBtn = document.getElementById("playPauseBtn");
    stopBtn = document.getElementById("stopBtn");
    rateSlider = document.getElementById("rate");
    rateValue = document.getElementById("rateValue");
    statusEl = document.getElementById("status");
    textContent = document.getElementById("textContent");
    speakerVoicesDiv = document.getElementById("speakerVoices");
    languageControlsContainer = document.getElementById("languageControlsContainer");

    applyFontFamilies();
    loadLanguageRateSettings();
    collectGroups();
    attachLineClickHandlers();
    attachLanguageFlagHandlers();

    playPauseBtn.addEventListener("click", togglePlayPause);
    stopBtn.addEventListener("click", stopText);
    rateSlider.addEventListener("input", updateRate);

    if (!("speechSynthesis" in window)) {
        updateStatus("stopped", "Speech synthesis not supported in this browser");
        return;
    }

    loadVoices();
    speechSynthesis.onvoiceschanged = () => {
        loadVoices();
        buildLanguageControls();
    };
    buildLanguageControls();
    updateLanguageFlagDisplay();
    updatePlayPauseButton();
}

function applyFontFamilies() {
    languages.forEach(L => {
        if (!L.font_family) return;
        const family = L.font_family
            .map(f => (f.includes(" ") ? `"${f}"` : f))
            .join(", ");
        document.querySelectorAll(`.translation-line.lang-${L.code} .line-text`).forEach(el => {
            el.style.fontFamily = family;
        });
    });
}

function collectGroups() {
    const groupElements = textContent.querySelectorAll(".translation-group");
    groups = Array.from(groupElements).map(groupEl => {
        const linesByLang = {};
        groupEl.querySelectorAll(".translation-line").forEach(lineEl => {
            const lang = lineEl.getAttribute("data-lang");
            const textContainer = lineEl.querySelector(".line-text");
            const speakerEl = lineEl.querySelector(".speaker-label");
            const text = textContainer.textContent;
            textContainer.setAttribute("data-original-text", text);
            const speaker = speakerEl ? speakerEl.textContent.replace(/[:：]\s*$/, "").trim() : "";
            linesByLang[lang] = {
                element: lineEl,
                textContainer: textContainer,
                text: text,
                speaker: speaker,
            };
        });
        return linesByLang;
    });
}

function attachLineClickHandlers() {
    groups.forEach((linesByLang, groupIndex) => {
        Object.keys(linesByLang).forEach(lang => {
            linesByLang[lang].element.addEventListener("click", e => {
                if (e.target.classList.contains("language-flag")) return;
                if (!langStates[lang].enabled) {
                    langStates[lang].enabled = true;
                    updateLanguageFlagDisplay();
                }
                playFromLineInLanguage(groupIndex, lang);
            });
        });
    });
}

function attachLanguageFlagHandlers() {
    document.querySelectorAll(".translation-line .language-flag").forEach(flag => {
        const lang = flag.parentElement.getAttribute("data-lang");
        flag.addEventListener("click", e => {
            e.stopPropagation();
            toggleLanguageFlag(lang);
        });
    });
}

function loadVoices() {
    availableVoices = speechSynthesis.getVoices();
}

function getFilteredVoices(langKey) {
    return getFilteredVoicesForLang(availableVoices, langStates[langKey].lang_code);
}

function buildLanguageControls() {
    if (speakers.length === 0) {
        speakerVoicesDiv.style.display = "none";
        return;
    }
    speakerVoicesDiv.style.display = "block";

    languages.forEach(L => {
        const fv = getFilteredVoices(L.code);
        autoAssignDefaultVoices(langStates[L.code].speakerVoices, speakers, fv);
    });

    languageControlsContainer.innerHTML = "";
    const table = document.createElement("table");
    table.className = "language-controls-table";

    const head = document.createElement("tr");
    const langHeader = document.createElement("th"); langHeader.textContent = "Language"; head.appendChild(langHeader);
    const speedHeader = document.createElement("th"); speedHeader.textContent = "Speed"; head.appendChild(speedHeader);
    speakers.forEach((s, i) => {
        const th = document.createElement("th");
        th.textContent = `Speaker ${i + 1}`;
        head.appendChild(th);
    });
    table.appendChild(head);

    languages.forEach(L => {
        const ls = langStates[L.code];
        const row = document.createElement("tr");
        row.setAttribute("data-lang", L.code);

        const langCell = document.createElement("td");
        langCell.textContent = `${L.name} (${L.lang_code})`;
        row.appendChild(langCell);

        const speedCell = document.createElement("td");
        const speedDiv = document.createElement("div");
        speedDiv.className = "speed-control-container";
        const slider = document.createElement("input");
        slider.type = "range";
        slider.min = "0.5"; slider.max = "2"; slider.step = "0.1";
        slider.value = ls.rate;
        slider.setAttribute("data-lang", L.code);
        const valueSpan = document.createElement("span");
        valueSpan.textContent = ls.rate.toFixed(1) + "x";
        slider.addEventListener("input", e => {
            const lang = e.target.getAttribute("data-lang");
            const r = parseFloat(e.target.value);
            langStates[lang].rate = r;
            valueSpan.textContent = r.toFixed(1) + "x";
            saveLanguageRateSettings();
            restartIfPlaying();
        });
        speedDiv.appendChild(slider);
        speedDiv.appendChild(valueSpan);
        speedCell.appendChild(speedDiv);
        row.appendChild(speedCell);

        const fv = getFilteredVoices(L.code);
        speakers.forEach((_, speakerIndex) => {
            const cell = document.createElement("td");
            cell.className = "speaker-cell";
            cell.appendChild(createVoiceSelect(L.code, speakerIndex, fv));
            row.appendChild(cell);
        });

        table.appendChild(row);
    });

    languageControlsContainer.appendChild(table);
}

function createVoiceSelect(langKey, speakerIndex, filteredVoices) {
    const select = document.createElement("select");
    select.className = "speaker-voice-select";
    select.dataset.lang = langKey;
    select.dataset.speakerIndex = speakerIndex;

    const def = document.createElement("option");
    def.value = ""; def.textContent = "Default";
    select.appendChild(def);

    const ls = langStates[langKey];
    const current = ls.speakerVoices[speakerIndex];
    let selectedIdx = "";
    filteredVoices.forEach((v, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.textContent = `${v.name} (${v.lang})`;
        if (v.default) opt.textContent += " - Default";
        if (current && v.name === current.name && v.lang === current.lang) selectedIdx = idx;
        select.appendChild(opt);
    });
    select.value = selectedIdx;

    select.addEventListener("change", e => {
        const v = e.target.value;
        ls.speakerVoices[speakerIndex] = v === "" ? undefined : filteredVoices[parseInt(v, 10)];
    });
    return select;
}

function getEnabledLanguages() {
    return languages.filter(L => langStates[L.code].enabled).map(L => L.code);
}

function togglePlayPause() {
    if (isPaused && currentSynth) {
        speechSynthesis.resume();
        isPaused = false;
        isStopped = false;
        updateStatus("playing", "Playing...");
        updatePlayPauseButton();
    } else if (currentSynth && !isPaused) {
        pauseText();
    } else {
        isStopped = false;
        const enabled = getEnabledLanguages();
        if (enabled.length === 0) {
            updateStatus("stopped", "No language enabled");
            return;
        }
        playFromLineInLanguage(0, enabled[0]);
    }
}

function playFromLineInLanguage(groupIndex, lang) {
    stopText();
    currentGroupIndex = groupIndex;
    const enabled = getEnabledLanguages();
    if (enabled.length === 0) {
        updateStatus("stopped", "No language enabled");
        return;
    }
    const idx = enabled.indexOf(lang);
    currentStep = idx >= 0 ? idx : 0;
    isPaused = false;
    isStopped = false;
    speakNext();
    updatePlayPauseButton();
}

function speakNext() {
    const enabled = getEnabledLanguages();
    if (enabled.length === 0) {
        stopText();
        return;
    }
    if (currentStep >= enabled.length) {
        currentStep = 0;
        currentGroupIndex++;
    }
    if (currentGroupIndex >= groups.length) {
        stopText();
        updateStatus("stopped", "Finished");
        return;
    }

    const lang = enabled[currentStep];
    const group = groups[currentGroupIndex];
    if (!group[lang]) {
        currentStep++;
        speakNext();
        return;
    }

    speakLine(group[lang], lang, enabled);
}

async function speakLine(lineEntry, lang, enabled) {
    const gen = speechGeneration;
    clearAllHighlights();

    document.querySelectorAll(".translation-line").forEach(el => el.classList.remove("current"));
    lineEntry.element.classList.add("current");

    const groupEl = lineEntry.element.closest(".translation-group");
    if (groupEl) groupEl.scrollIntoView({ behavior: "smooth", block: "center" });

    const ls = langStates[lang];
    const speakerIndex = speakers.indexOf(lineEntry.speaker);
    const candidates = buildVoiceCandidates(ls.speakerVoices, speakers, speakerIndex, getFilteredVoices(lang));
    const rate = parseFloat(rateSlider.value) * ls.rate;

    const result = await speakWithRetry(lineEntry.text, ls.lang_code, rate, candidates, {
        onstart: () => updateStatus(
            "playing",
            `Playing line ${currentGroupIndex + 1}/${groups.length} in ${ls.name} (${currentStep + 1}/${enabled.length})`
        ),
        onboundary: e => { if (e.name === "word" && e.charLength) highlightWord(lineEntry, e.charIndex, e.charLength); },
        onUtterance: utt => { currentSynth = utt; },
        onVoiceSuccess: voice => { ls.speakerVoices[speakerIndex] = voice; updateVoiceSelect(lang, speakerIndex, voice); },
    });

    if (gen !== speechGeneration) return;
    currentSynth = null;
    clearAllHighlights();

    if (result === "ended" && !isPaused && !isStopped) {
        currentStep++;
        const delay = currentStep >= enabled.length ? 800 : 400;
        setTimeout(() => {
            if (!isPaused && !isStopped) speakNext();
        }, delay);
    } else if (result === "error") {
        console.error("Speech synthesis error");
        updateStatus("stopped", "Error occurred during playback");
    }
}

function updateVoiceSelect(lang, speakerIndex, voice) {
    const select = languageControlsContainer.querySelector(
        `select[data-lang="${lang}"][data-speaker-index="${speakerIndex}"]`
    );
    if (!select) return;
    const idx = getFilteredVoices(lang).findIndex(v => v.name === voice.name && v.lang === voice.lang);
    if (idx >= 0) select.value = String(idx);
}

function pauseText() {
    if (currentSynth && !isPaused) {
        speechSynthesis.pause();
        isPaused = true;
        updateStatus("paused", "Paused");
        updatePlayPauseButton();
    }
}

function stopText() {
    const wasPlaying = currentSynth !== null;
    speechGeneration++;
    isStopped = true;
    if (currentSynth) {
        speechSynthesis.cancel();
        currentSynth = null;
    }
    isPaused = false;
    currentGroupIndex = 0;
    currentStep = 0;
    document.querySelectorAll(".translation-line").forEach(el => el.classList.remove("current"));
    clearAllHighlights();
    if (wasPlaying) updateStatus("stopped", "Stopped");
    updatePlayPauseButton();
}

function updateRate() {
    const r = parseFloat(rateSlider.value);
    rateValue.textContent = r.toFixed(1) + "x";
    restartIfPlaying();
}

function restartIfPlaying() {
    if (currentSynth && !isPaused && !isStopped) {
        const g = currentGroupIndex;
        const s = currentStep;
        speechGeneration++;
        speechSynthesis.cancel();
        currentSynth = null;
        setTimeout(() => {
            if (!isPaused && !isStopped) {
                currentGroupIndex = g;
                currentStep = s;
                speakNext();
            }
        }, 100);
    }
}

function highlightWord(lineEntry, charIndex, charLength) {
    const container = lineEntry.textContainer;
    const text = container.getAttribute("data-original-text") || lineEntry.text;
    clearAllHighlights();

    const before = text.substring(0, charIndex);
    const target = text.substring(charIndex, charIndex + charLength);
    const after = text.substring(charIndex + charLength);

    container.innerHTML = "";
    if (before) {
        const span = document.createElement("span");
        span.textContent = before;
        container.appendChild(span);
    }
    if (target) {
        const span = document.createElement("span");
        span.className = "word speaking";
        span.textContent = target;
        container.appendChild(span);
    }
    if (after) {
        const span = document.createElement("span");
        span.textContent = after;
        container.appendChild(span);
    }
}

function clearAllHighlights() {
    groups.forEach(g => {
        Object.values(g).forEach(entry => {
            const orig = entry.textContainer.getAttribute("data-original-text");
            if (orig) entry.textContainer.textContent = orig;
        });
    });
}

function toggleLanguageFlag(lang) {
    if (!langStates[lang]) return;
    langStates[lang].enabled = !langStates[lang].enabled;
    updateLanguageFlagDisplay();
    if (currentSynth) stopText();
    const status = langStates[lang].enabled ? "enabled" : "disabled";
    updateStatus("stopped", `${langStates[lang].name} ${status}`);
}

function updateLanguageFlagDisplay() {
    document.querySelectorAll(".translation-line").forEach(line => {
        const lang = line.getAttribute("data-lang");
        const flag = line.querySelector(".language-flag");
        if (!flag || !langStates[lang]) return;
        flag.classList.toggle("enabled", langStates[lang].enabled);
        line.classList.toggle("disabled", !langStates[lang].enabled);
    });
}

function saveLanguageRateSettings() {
    const rates = {};
    Object.keys(langStates).forEach(k => { rates[k] = langStates[k].rate; });
    try { localStorage.setItem(RATE_STORAGE_KEY, JSON.stringify(rates)); } catch (e) {}
}

function loadLanguageRateSettings() {
    try {
        const saved = localStorage.getItem(RATE_STORAGE_KEY);
        if (!saved) return;
        const rates = JSON.parse(saved);
        Object.keys(rates).forEach(k => {
            if (langStates[k]) langStates[k].rate = rates[k];
        });
    } catch (e) {}
}

function updateStatus(type, message) {
    statusEl.className = `status ${type}`;
    statusEl.textContent = message;
}

function updatePlayPauseButton() {
    if (currentSynth && !isPaused) {
        playPauseBtn.textContent = "⏸️ Pause";
        playPauseBtn.className = "pause-btn";
    } else {
        playPauseBtn.textContent = "▶️ Play";
        playPauseBtn.className = "play-btn";
    }
}

window.toggleSpeakerVoices = function () {
    const c = document.getElementById("voiceAssignmentContainer");
    const i = document.getElementById("toggleIcon");
    if (c.classList.contains("collapsed")) {
        c.classList.remove("collapsed");
        i.classList.add("expanded");
        i.textContent = "▲";
    } else {
        c.classList.add("collapsed");
        i.classList.remove("expanded");
        i.textContent = "▼";
    }
};

document.addEventListener("DOMContentLoaded", init);
