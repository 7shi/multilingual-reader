// Multilingual Podcast Reader - 多言語並列モード用ロジック
// page-config の JSON とテンプレートでレンダリングされた .translation-group 要素を読み込み、
// 全 6 言語の対訳を同時表示しながら、有効化された言語のみを順次読み上げる。

(function () {
    "use strict";

    const config = JSON.parse(document.getElementById("page-config").textContent);
    const languages = config.languages;
    const speakers = config.speakers;

    const RATE_STORAGE_KEY = `multilingualReader.langRates.${config.topic}`;

    // 言語別状態
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
        const ls = langStates[langKey];
        const targetBase = ls.lang_code.split("-")[0].toLowerCase();
        const matches = availableVoices.filter(v => v.lang.split("-")[0].toLowerCase() === targetBase);
        return prioritizeVoicesByRegion(matches, ls.lang_code);
    }

    function prioritizeVoicesByRegion(voices, target) {
        if (voices.length === 0) return voices;
        const nonMulti = voices.filter(v => !v.name.toLowerCase().includes("multilingual"));
        const pool = nonMulti.length > 0 ? nonMulti : voices;
        const t = target.toLowerCase();
        return pool.slice().sort((a, b) => {
            const aE = a.lang.toLowerCase() === t;
            const bE = b.lang.toLowerCase() === t;
            if (aE !== bE) return bE - aE;
            const aO = a.localService === false;
            const bO = b.localService === false;
            if (aO !== bO) return bO - aO;
            if (a.default !== b.default) return b.default - a.default;
            return a.name.localeCompare(b.name);
        });
    }

    function autoAssignDefaultVoices(langKey, filteredVoices) {
        const ls = langStates[langKey];
        if (ls.speakerVoices.some(v => v !== undefined) || filteredVoices.length === 0) return;

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

        const isMale = v => {
            const n = v.name.toLowerCase();
            return n.includes("male") || n.includes("man") ||
                n.includes("homme") || n.includes("masculine") ||
                maleNames.some(x => n.includes(x));
        };
        const isFemale = v => {
            const n = v.name.toLowerCase();
            return n.includes("female") || n.includes("woman") ||
                n.includes("femme") || n.includes("feminine") ||
                femaleNames.some(x => n.includes(x));
        };

        const males = filteredVoices.filter(isMale);
        const females = filteredVoices.filter(isFemale);

        if (speakers.length >= 2 && males.length > 0 && females.length > 0) {
            let mi = 0, fi = 0;
            speakers.forEach((_, i) => {
                if (i % 2 === 0 && fi < females.length) ls.speakerVoices[i] = females[fi++];
                else if (mi < males.length) ls.speakerVoices[i] = males[mi++];
            });
        } else {
            speakers.forEach((_, i) => {
                if (i < filteredVoices.length) ls.speakerVoices[i] = filteredVoices[i];
            });
        }
    }

    function buildLanguageControls() {
        if (speakers.length === 0) {
            speakerVoicesDiv.style.display = "none";
            return;
        }
        speakerVoicesDiv.style.display = "block";

        languages.forEach(L => {
            const fv = getFilteredVoices(L.code);
            autoAssignDefaultVoices(L.code, fv);
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

    function speakLine(lineEntry, lang, enabled) {
        clearAllHighlights();

        document.querySelectorAll(".translation-line").forEach(el => el.classList.remove("current"));
        lineEntry.element.classList.add("current");

        const groupEl = lineEntry.element.closest(".translation-group");
        if (groupEl) groupEl.scrollIntoView({ behavior: "smooth", block: "center" });

        const utterance = new SpeechSynthesisUtterance(lineEntry.text);
        const ls = langStates[lang];
        utterance.lang = ls.lang_code;
        utterance.rate = parseFloat(rateSlider.value) * ls.rate;

        const speakerIndex = speakers.indexOf(lineEntry.speaker);
        if (speakerIndex >= 0 && ls.speakerVoices[speakerIndex]) {
            utterance.voice = ls.speakerVoices[speakerIndex];
        }

        utterance.onstart = () => {
            updateStatus(
                "playing",
                `Playing line ${currentGroupIndex + 1}/${groups.length} in ${ls.name} (${currentStep + 1}/${enabled.length})`
            );
        };
        utterance.onboundary = e => {
            if (e.name === "word" && e.charLength) {
                highlightWord(lineEntry, e.charIndex, e.charLength);
            }
        };
        utterance.onend = () => {
            clearAllHighlights();
            if (!isPaused && !isStopped) {
                currentStep++;
                const delay = currentStep >= enabled.length ? 800 : 400;
                setTimeout(() => {
                    if (!isPaused && !isStopped) speakNext();
                }, delay);
            }
        };
        utterance.onerror = e => {
            if (isStopped || e.error === "canceled" || e.error === "interrupted") {
                clearAllHighlights();
                return;
            }
            console.error("Speech synthesis error:", e);
            updateStatus("stopped", "Error occurred during playback");
            clearAllHighlights();
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
})();
