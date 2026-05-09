// Multilingual Podcast Reader - 単一言語ページ用ロジック
// page-config の JSON とテンプレートでレンダリングされた .line 要素を読み込み、
// Web Speech API による読み上げ・話者別音声選択・動的ハイライトを提供する。

(function () {
    "use strict";

    const config = JSON.parse(document.getElementById("page-config").textContent);
    const lang = config.lang;
    const langCode = config.lang_code;
    const langName = config.lang_name;
    const speakers = config.speakers;
    const fontFamily = config.font_family;

    let availableVoices = [];
    let speakerVoices = new Array(speakers.length).fill(undefined);
    let currentSynth = null;
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
        const targetBase = langCode.split("-")[0].toLowerCase();
        const matches = availableVoices.filter(voice => {
            const base = voice.lang.split("-")[0].toLowerCase();
            return base === targetBase;
        });
        return prioritizeVoicesByRegion(matches, langCode);
    }

    function prioritizeVoicesByRegion(voices, targetLangCode) {
        if (voices.length === 0) return voices;
        const nonMultilingual = voices.filter(
            v => !v.name.toLowerCase().includes("multilingual")
        );
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

    function autoAssignDefaultVoices(filteredVoices) {
        const hasExisting = speakerVoices.some(v => v !== undefined);
        if (hasExisting || filteredVoices.length === 0) return;

        const maleNames = [
            "gerard", "thierry", "antoine", "jean", "remy", "henri", "fabrice",
            "david", "guy", "mark", "richard", "ryan", "brian", "christopher",
            "eric", "jacob", "benjamin", "ichiro", "keita", "yunjian",
        ];
        const femaleNames = [
            "charline", "sylvie", "vivienne", "denise", "eloise", "ariane",
            "aria", "jenny", "nancy", "sara", "jane", "michelle", "emma",
            "elizabeth", "amber", "ayumi", "haruka", "sayaka", "nanami",
            "xiaoxiao",
        ];

        const isMale = voice => {
            const name = voice.name.toLowerCase();
            return name.includes("male") || name.includes("man") ||
                name.includes("homme") || name.includes("masculine") ||
                maleNames.some(n => name.includes(n));
        };
        const isFemale = voice => {
            const name = voice.name.toLowerCase();
            return name.includes("female") || name.includes("woman") ||
                name.includes("femme") || name.includes("feminine") ||
                femaleNames.some(n => name.includes(n));
        };

        const males = filteredVoices.filter(isMale);
        const females = filteredVoices.filter(isFemale);

        if (speakers.length >= 2 && males.length > 0 && females.length > 0) {
            let mi = 0, fi = 0;
            speakers.forEach((_, i) => {
                if (i % 2 === 0 && fi < females.length) {
                    speakerVoices[i] = females[fi++];
                } else if (mi < males.length) {
                    speakerVoices[i] = males[mi++];
                }
            });
        } else {
            speakers.forEach((_, i) => {
                if (i < filteredVoices.length) {
                    speakerVoices[i] = filteredVoices[i];
                }
            });
        }
    }

    function buildSpeakerControls() {
        if (speakers.length === 0) {
            speakerVoicesDiv.style.display = "none";
            return;
        }
        speakerVoicesDiv.style.display = "block";

        const filteredVoices = getFilteredVoices();
        autoAssignDefaultVoices(filteredVoices);

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

    function speakLine(index) {
        if (index >= lines.length) {
            stopText();
            updateStatus("stopped", "Finished");
            return;
        }
        const line = lines[index];
        clearDynamicHighlight();

        lines.forEach(l => l.element.classList.remove("current"));
        line.element.classList.add("current");
        line.element.scrollIntoView({ behavior: "smooth", block: "center" });

        const utterance = new SpeechSynthesisUtterance(line.text);
        utterance.lang = langCode;
        utterance.rate = parseFloat(rateSlider.value);

        const speakerIndex = speakers.indexOf(line.speaker);
        const voice = speakerVoices[speakerIndex];
        if (voice) utterance.voice = voice;

        utterance.onstart = () => {
            updateStatus("playing", `Playing line ${index + 1}/${lines.length}`);
        };
        utterance.onboundary = e => {
            if (e.name === "word" && e.charLength) {
                highlightWord(line, e.charIndex, e.charLength);
            }
        };
        utterance.onend = () => {
            clearDynamicHighlight();
            if (!isPaused && !isStopped) {
                currentLineIndex++;
                setTimeout(() => {
                    if (!isPaused && !isStopped) speakLine(currentLineIndex);
                }, 400);
            }
        };
        utterance.onerror = e => {
            // stopText / rate 変更による cancel は意図的なものなのでエラー表示しない
            if (isStopped || e.error === "canceled" || e.error === "interrupted") {
                clearDynamicHighlight();
                return;
            }
            console.error("Speech synthesis error:", e);
            updateStatus("stopped", "Error occurred during playback");
            clearDynamicHighlight();
        };

        currentSynth = utterance;
        speechSynthesis.speak(utterance);
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
            speechSynthesis.cancel();
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
})();
