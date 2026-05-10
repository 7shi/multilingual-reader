// Multilingual Podcast Reader - 単一言語ページ用ロジック
// page-config の JSON とテンプレートでレンダリングされた .line 要素を読み込み、
// Web Speech API による読み上げ・話者別音声選択・動的ハイライトを提供する。

import { getFilteredVoicesForLang, autoAssignDefaultVoices, buildVoiceCandidates, speakWithRetry } from './speech.js';

const config = JSON.parse(document.getElementById("page-config").textContent);
const lang = config.lang;
const langCode = config.lang_code;
const langName = config.lang_name;
const speakers = config.speakers;
const fontFamily = config.font_family;

let availableVoices = [];
let speakerVoices = new Array(speakers.length).fill(undefined);
let currentSynth = null;
let speechGeneration = 0;
let isPaused = false;
let isStopped = false;
let currentLineIndex = 0;
let lines = [];

let playPauseBtn, stopBtn, rateSlider, rateValue;
let statusEl, textContent, speakerVoicesDiv, speakerControlsContainer;

function init() {
    playPauseBtn = document.getElementById("playPauseBtn");
    stopBtn = document.getElementById("stopBtn");
    rateSlider = document.getElementById("rate");
    rateValue = document.getElementById("rateValue");
    statusEl = document.getElementById("status");
    textContent = document.getElementById("textContent");
    speakerVoicesDiv = document.getElementById("speakerVoices");
    speakerControlsContainer = document.getElementById("speakerControlsContainer");

    if (fontFamily) {
        const family = fontFamily
            .map(f => (f.includes(" ") ? `"${f}"` : f))
            .join(", ");
        textContent.style.fontFamily = family;
    }

    collectLines();
    attachLineClickHandlers();

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
        buildSpeakerControls();
    };
    buildSpeakerControls();
    updatePlayPauseButton();
}

function collectLines() {
    const elements = textContent.querySelectorAll(".line");
    lines = Array.from(elements).map(el => ({
        element: el,
        speaker: el.getAttribute("data-speaker"),
        text: el.querySelector(".line-text").textContent,
        textContainer: el.querySelector(".line-text"),
    }));
    lines.forEach(line => {
        line.textContainer.setAttribute("data-original-text", line.text);
    });
}

function attachLineClickHandlers() {
    lines.forEach((line, index) => {
        line.element.addEventListener("click", () => playFromLine(index));
    });
}

function loadVoices() {
    availableVoices = speechSynthesis.getVoices();
}

function getFilteredVoices() {
    return getFilteredVoicesForLang(availableVoices, langCode);
}

function buildSpeakerControls() {
    if (speakers.length === 0) {
        speakerVoicesDiv.style.display = "none";
        return;
    }
    speakerVoicesDiv.style.display = "block";

    const filteredVoices = getFilteredVoices();
    autoAssignDefaultVoices(speakerVoices, speakers, filteredVoices);

    speakerControlsContainer.innerHTML = "";

    const table = document.createElement("table");
    table.className = "speaker-controls-table";

    const head = document.createElement("tr");
    const langHeader = document.createElement("th");
    langHeader.textContent = `${langName} (${langCode})`;
    head.appendChild(langHeader);
    speakers.forEach((speaker, i) => {
        const th = document.createElement("th");
        th.textContent = `Speaker ${i + 1}: ${speaker}`;
        head.appendChild(th);
    });
    table.appendChild(head);

    const row = document.createElement("tr");
    const labelCell = document.createElement("td");
    labelCell.textContent = "Voice";
    row.appendChild(labelCell);
    speakers.forEach((_, speakerIndex) => {
        const cell = document.createElement("td");
        cell.appendChild(createVoiceSelect(speakerIndex, filteredVoices));
        row.appendChild(cell);
    });
    table.appendChild(row);

    speakerControlsContainer.appendChild(table);
}

function createVoiceSelect(speakerIndex, filteredVoices) {
    const select = document.createElement("select");
    select.className = "speaker-voice-select";
    select.dataset.speakerIndex = speakerIndex;

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Default";
    select.appendChild(defaultOption);

    const current = speakerVoices[speakerIndex];
    let selectedIndex = "";
    filteredVoices.forEach((voice, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.textContent = `${voice.name} (${voice.lang})`;
        if (voice.default) opt.textContent += " - Default";
        if (current && voice.name === current.name && voice.lang === current.lang) {
            selectedIndex = idx;
        }
        select.appendChild(opt);
    });
    select.value = selectedIndex;

    select.addEventListener("change", e => {
        const v = e.target.value;
        speakerVoices[speakerIndex] = v === "" ? undefined : filteredVoices[parseInt(v, 10)];
    });
    return select;
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
        playFromLine(0);
    }
}

function playFromLine(index) {
    stopText();
    currentLineIndex = index;
    isPaused = false;
    isStopped = false;
    speakLine(currentLineIndex);
    updatePlayPauseButton();
}

async function speakLine(index) {
    if (index >= lines.length) {
        stopText();
        updateStatus("stopped", "Finished");
        return;
    }
    const gen = speechGeneration;
    const line = lines[index];
    clearDynamicHighlight();

    lines.forEach(l => l.element.classList.remove("current"));
    line.element.classList.add("current");
    line.element.scrollIntoView({ behavior: "smooth", block: "center" });

    const speakerIndex = speakers.indexOf(line.speaker);
    const candidates = buildVoiceCandidates(speakerVoices, speakers, speakerIndex, getFilteredVoices());
    const rate = parseFloat(rateSlider.value);

    const result = await speakWithRetry(line.text, langCode, rate, candidates, {
        onstart: () => updateStatus("playing", `Playing line ${index + 1}/${lines.length}`),
        onboundary: e => { if (e.name === "word" && e.charLength) highlightWord(line, e.charIndex, e.charLength); },
        onUtterance: utt => { currentSynth = utt; },
        onVoiceSuccess: voice => { speakerVoices[speakerIndex] = voice; updateVoiceSelect(speakerIndex, voice); },
    });

    if (gen !== speechGeneration) return;
    currentSynth = null;
    clearDynamicHighlight();

    if (result === "ended" && !isPaused && !isStopped) {
        currentLineIndex++;
        setTimeout(() => {
            if (!isPaused && !isStopped) speakLine(currentLineIndex);
        }, 400);
    } else if (result === "error") {
        console.error("Speech synthesis error");
        updateStatus("stopped", "Error occurred during playback");
    }
}

function updateVoiceSelect(speakerIndex, voice) {
    const select = speakerControlsContainer.querySelector(`select[data-speaker-index="${speakerIndex}"]`);
    if (!select) return;
    const idx = getFilteredVoices().findIndex(v => v.name === voice.name && v.lang === voice.lang);
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
    currentLineIndex = 0;
    lines.forEach(l => l.element.classList.remove("current"));
    clearDynamicHighlight();
    if (wasPlaying) updateStatus("stopped", "Stopped");
    updatePlayPauseButton();
}

function updateRate() {
    const rate = parseFloat(rateSlider.value);
    rateValue.textContent = rate.toFixed(1) + "x";
    if (currentSynth && !currentSynth.paused) {
        const resumeIndex = currentLineIndex;
        speechGeneration++;
        speechSynthesis.cancel();
        currentSynth = null;
        setTimeout(() => {
            if (!isPaused && !isStopped) speakLine(resumeIndex);
        }, 100);
    }
}

function highlightWord(line, charIndex, charLength) {
    const container = line.textContainer;
    const text = container.getAttribute("data-original-text") || line.text;
    clearDynamicHighlight();

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

function clearDynamicHighlight() {
    lines.forEach(line => {
        const original = line.textContainer.getAttribute("data-original-text");
        if (original) line.textContainer.textContent = original;
    });
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
    const container = document.getElementById("voiceAssignmentContainer");
    const icon = document.getElementById("toggleIcon");
    if (container.classList.contains("collapsed")) {
        container.classList.remove("collapsed");
        icon.classList.add("expanded");
        icon.textContent = "▲";
    } else {
        container.classList.add("collapsed");
        icon.classList.remove("expanded");
        icon.textContent = "▼";
    }
};

document.addEventListener("DOMContentLoaded", init);
