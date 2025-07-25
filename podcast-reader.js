// Text data is loaded from external files
let texts = datasets && datasets[0] ? datasets[0] : [];

// Language codes for speech synthesis
const langCodes = {
    fr: 'fr-FR',
    en: 'en-US',
    ja: 'ja-JP'
};

let currentSynth = null;
let isPaused = false;
let isStopped = false; // Firefox対応：停止状態を明確に管理
let currentLineIndex = 0;
let dialogueLines = [];
// Removed: currentWordIndex and currentLineWords are no longer needed for dynamic highlighting
let availableVoices = [];
let speakers = [];
let speakerVoicesByLanguage = {
    fr: [],
    en: [],
    ja: []
}; // Store voice settings per language by speaker index
let isMultiLanguageMode = false;
let multiLangCurrentStep = 0; // 0: fr, 1: en, 2: ja
let datasetConfigMapping = {}; // Store dataset name to index mapping

// Language-specific speed settings
let languageRates = {
    fr: 1.0,
    en: 1.0,
    ja: 1.5
};

// DOM elements
const languageSelect = document.getElementById('language');
const datasetSelect = document.getElementById('dataset');
const playPauseBtn = document.getElementById('playPauseBtn');
const stopBtn = document.getElementById('stopBtn');
const rateSlider = document.getElementById('rate');
const rateValue = document.getElementById('rateValue');

// Language-specific rate controls
const rateFrSlider = document.getElementById('rateFr');
const rateEnSlider = document.getElementById('rateEn');
const rateJaSlider = document.getElementById('rateJa');
const rateValueFr = document.getElementById('rateValueFr');
const rateValueEn = document.getElementById('rateValueEn');
const rateValueJa = document.getElementById('rateValueJa');
const status = document.getElementById('status');
const textContent = document.getElementById('textContent');
const speakerVoicesDiv = document.getElementById('speakerVoices');

// Initialize
function init(datasetConfig) {
    // Store dataset config for later use
    datasetConfigMapping = datasetConfig;
    
    // Initialize multi-language mode based on default selection
    isMultiLanguageMode = (languageSelect.value === 'multi');
    
    // Initialize dataset based on provided config
    const selectedDataset = datasetSelect.value;
    if (datasets && datasetConfig) {
        if (datasetConfig[selectedDataset] !== undefined && datasets[datasetConfig[selectedDataset]]) {
            texts = datasets[datasetConfig[selectedDataset]];
        }
    }
    
    loadVoices();
    loadLanguageRateSettings();
    loadText();
    
    // Initialize button state
    updatePlayPauseButton();
    
    // Event listeners
    languageSelect.addEventListener('change', onLanguageChange);
    datasetSelect.addEventListener('change', onDatasetChange);
    playPauseBtn.addEventListener('click', togglePlayPause);
    stopBtn.addEventListener('click', stopText);
    rateSlider.addEventListener('input', updateRate);
    
    // Language-specific rate controls
    rateFrSlider.addEventListener('input', updateLanguageRate);
    rateEnSlider.addEventListener('input', updateLanguageRate);
    rateJaSlider.addEventListener('input', updateLanguageRate);
    
    
    // Load voices when they become available
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = () => {
            loadVoices();
            createAllLanguageVoiceAssignments();
        };
    } else {
        status.textContent = 'Speech synthesis not supported in this browser';
        status.className = 'status stopped';
    }
}

function onLanguageChange() {
    // Update multi-language mode based on selection
    isMultiLanguageMode = (languageSelect.value === 'multi');
    
    // Update status message
    if (isMultiLanguageMode) {
        updateStatus('stopped', 'Multi-language mode enabled');
    } else {
        updateStatus('stopped', 'Single language mode');
    }
    
    // Stop current playback when switching modes
    stopText();
    
    // Load text content
    loadText();
}

function onDatasetChange() {
    // Update texts based on dataset selection
    const selectedDataset = datasetSelect.value;
    
    if (datasets && datasetConfigMapping) {
        if (datasetConfigMapping[selectedDataset] !== undefined && datasets[datasetConfigMapping[selectedDataset]]) {
            texts = datasets[datasetConfigMapping[selectedDataset]];
        } else {
            console.error(`Dataset '${selectedDataset}' not found in config`);
            return;
        }
    } else {
        console.error('Datasets or config not loaded');
        return;
    }
    
    // データセット変更時にステータスを更新
    updateStatus('stopped', `Ready to play - ${selectedDataset} dataset loaded`);
    
    // Reset voice assignments when switching datasets
    speakerVoicesByLanguage = {
        fr: [],
        en: [],
        ja: []
    };
    
    // Stop current playback when switching datasets
    stopText();
    
    // Load text content with new dataset
    loadText();
}

function loadText() {
    // Parse dialogue lines for all languages using shared logic
    const allLanguageLines = parseAllLanguageTexts();
    
    // Use the first available language for line count if multi-language mode
    let selectedLang;
    if (isMultiLanguageMode || languageSelect.value === 'multi') {
        selectedLang = 'fr'; // Use French as base for multi-language mode
    } else {
        selectedLang = languageSelect.value;
    }
    dialogueLines = allLanguageLines[selectedLang];
    
    // Ensure dialogueLines is not undefined
    if (!dialogueLines) {
        dialogueLines = [];
    }
    
    // Identify unique speakers
    identifySpeakers();
    
    displayTranslationText(allLanguageLines);
    createAllLanguageVoiceAssignments();
}

// Removed displayText function - no longer needed with dynamic highlighting and translation mode

function displayTranslationText(allLanguageLines) {
    textContent.innerHTML = '';
    
    const maxLines = Math.max(...Object.values(allLanguageLines).map(lines => lines.length));
    
    for (let i = 0; i < maxLines; i++) {
        const translationGroup = document.createElement('div');
        translationGroup.className = 'translation-group';
        translationGroup.setAttribute('data-group-index', i);
        
        // Add each language version of this line
        Object.keys(langCodes).forEach(lang => {
            const langLines = allLanguageLines[lang];
            const line = langLines && langLines[i];
            
            if (line) {
                const translationLine = document.createElement('div');
                translationLine.className = 'translation-line';
                translationLine.setAttribute('data-line-index', i);
                translationLine.setAttribute('data-lang', lang);
                translationLine.addEventListener('click', () => playFromLineInLanguage(i, lang));
                
                const langFlag = document.createElement('div');
                langFlag.className = `language-flag ${lang}`;
                langFlag.textContent = lang.toUpperCase();
                
                const translationContent = document.createElement('div');
                translationContent.className = 'translation-content';
                
                const lineNumber = document.createElement('span');
                lineNumber.className = 'translation-line-number';
                lineNumber.textContent = `${i + 1}.`;
                
                const speaker = document.createElement('span');
                speaker.className = `speaker ${line.speaker.toLowerCase()}`;
                speaker.textContent = line.speaker + ':';
                
                const textContainer = document.createElement('span');
                textContainer.className = 'text-container';
                textContainer.setAttribute('data-lang', lang);
                
                // Store the original text without splitting into spans for dynamic highlighting
                textContainer.textContent = line.text;
                textContainer.setAttribute('data-original-text', line.text);
                
                translationContent.appendChild(lineNumber);
                translationContent.appendChild(speaker);
                translationContent.appendChild(textContainer);
                
                translationLine.appendChild(langFlag);
                translationLine.appendChild(translationContent);
                translationGroup.appendChild(translationLine);
            }
        });
        
        textContent.appendChild(translationGroup);
    }
}

function updateRate() {
    const rate = parseFloat(rateSlider.value);
    rateValue.textContent = rate.toFixed(1) + 'x';
    
    if (currentSynth) {
        // Cancel current speech and restart if playing
        const wasPlaying = !currentSynth.paused;
        if (wasPlaying) {
            currentSynth.cancel();
            setTimeout(() => {
                if (!isPaused && !isStopped) {
                    speakLine(currentLineIndex);
                }
            }, 100);
        }
    }
}

function updateLanguageRate(event) {
    const sliderId = event.target.id;
    const rate = parseFloat(event.target.value);
    
    // Update corresponding display value
    if (sliderId === 'rateFr') {
        languageRates.fr = rate;
        rateValueFr.textContent = rate.toFixed(1) + 'x';
    } else if (sliderId === 'rateEn') {
        languageRates.en = rate;
        rateValueEn.textContent = rate.toFixed(1) + 'x';
    } else if (sliderId === 'rateJa') {
        languageRates.ja = rate;
        rateValueJa.textContent = rate.toFixed(1) + 'x';
    }
    
    // Save settings to localStorage
    saveLanguageRateSettings();
    
    // Cancel current speech and restart if playing
    if (currentSynth) {
        const wasPlaying = !currentSynth.paused;
        if (wasPlaying) {
            currentSynth.cancel();
            setTimeout(() => {
                if (!isPaused && !isStopped) {
                    if (isMultiLanguageMode) {
                        speakLineMultiLanguage(currentLineIndex);
                    } else {
                        speakLine(currentLineIndex);
                    }
                }
            }, 100);
        }
    }
}


function togglePlayPause() {
    if (isPaused && currentSynth) {
        // Resume paused playback
        speechSynthesis.resume();
        isPaused = false;
        isStopped = false; // Resume時にもリセット
        updateStatus('playing', 'Playing...');
        updatePlayPauseButton();
    } else if (currentSynth && !isPaused) {
        // Pause current playback
        pauseText();
    } else {
        // Start new playback
        isStopped = false; // 再生開始時にリセット
        playText();
    }
}

function playText() {
    currentLineIndex = 0;
    multiLangCurrentStep = 0;
    isStopped = false; // 再生開始時にリセット
    
    if (isMultiLanguageMode) {
        speakLineMultiLanguage(currentLineIndex);
    } else {
        speakLine(currentLineIndex);
    }
    updatePlayPauseButton();
}

function playFromLine(lineIndex) {
    stopText();
    currentLineIndex = lineIndex;
    isStopped = false; // 再生開始時にリセット
    const selectedLang = languageSelect.value;
    speakLineInLanguage(currentLineIndex, selectedLang);
    updatePlayPauseButton();
}

function playFromLineInLanguage(lineIndex, lang) {
    stopText();
    
    // stopText()でリセットされた後に正しい値を設定
    currentLineIndex = lineIndex;
    isPaused = false; // 確実にfalseに設定
    isStopped = false; // 再生開始時にリセット
    
    // Multilingualモードの場合、クリックした言語から開始
    if (isMultiLanguageMode) {
        // クリックした言語に応じてmultiLangCurrentStepを設定
        if (lang === 'fr') {
            multiLangCurrentStep = 0;
        } else if (lang === 'en') {
            multiLangCurrentStep = 1;
        } else if (lang === 'ja') {
            multiLangCurrentStep = 2;
        } else {
            multiLangCurrentStep = 0; // デフォルトはフランス語から
        }
        speakLineMultiLanguage(currentLineIndex);
    } else {
        // 単一言語モードの場合
        speakLineInLanguage(currentLineIndex, lang);
    }
    updatePlayPauseButton();
}

function speakLineMultiLanguage(lineIndex) {
    const languages = ['fr', 'en', 'ja'];
    const currentLang = languages[multiLangCurrentStep];
    
    // Get the dialogue lines for all languages using shared logic
    const allLanguageLines = parseAllLanguageTexts();
    
    const langLines = allLanguageLines[currentLang];
    if (!langLines || lineIndex >= langLines.length) {
        stopText();
        return;
    }
    
    const line = langLines[lineIndex];
    
    // Create completion callback for multi-language mode
    const onSpeechComplete = () => {
        multiLangCurrentStep++;
        
        // If we've completed all 3 languages for this line
        if (multiLangCurrentStep >= 3) {
            multiLangCurrentStep = 0;
            currentLineIndex++;
            
            // Short pause between lines, then move to next line
            setTimeout(() => {
                if (isMultiLanguageMode && !isPaused && !isStopped) {
                    speakLineMultiLanguage(currentLineIndex);
                }
            }, 800); // Longer pause between lines
        } else {
            // Continue with next language for the same line
            setTimeout(() => {
                if (isMultiLanguageMode && !isPaused && !isStopped) {
                    speakLineMultiLanguage(currentLineIndex);
                }
            }, 400); // Short pause between languages
        }
    };
    
    // Use shared speech synthesis function
    const langNames = { fr: 'Français', en: 'English', ja: '日本語' };
    const statusMessage = `Playing line ${lineIndex + 1} in ${langNames[currentLang]} (${multiLangCurrentStep + 1}/3)`;
    
    speakLineWithUtterance(lineIndex, currentLang, line, statusMessage, onSpeechComplete);
}

function speakLine(lineIndex) {
    if (isMultiLanguageMode) {
        speakLineMultiLanguage(lineIndex);
    } else {
        const selectedLang = languageSelect.value;
        speakLineInLanguage(lineIndex, selectedLang);
    }
}

function speakLineInLanguage(lineIndex, lang) {
    // Get the dialogue lines for all languages using shared logic
    const allLanguageLines = parseAllLanguageTexts();
    
    const langLines = allLanguageLines[lang];
    if (!langLines || lineIndex >= langLines.length) {
        stopText();
        return;
    }
    
    const line = langLines[lineIndex];
    
    // Create completion callback for single language mode
    const onSpeechComplete = () => {
        currentLineIndex++;
        // Continue with the same language
        setTimeout(() => {
            if (!isStopped) {
                speakLineInLanguage(currentLineIndex, lang);
            }
        }, 500); // Short pause between lines
    };
    
    // Use shared speech synthesis function
    const statusMessage = `Playing line ${lineIndex + 1} in ${lang.toUpperCase()}`;
    
    speakLineWithUtterance(lineIndex, lang, line, statusMessage, onSpeechComplete);
}

function pauseText() {
    if (currentSynth && !isPaused) {
        speechSynthesis.pause();
        isPaused = true;
        updateStatus('paused', 'Paused');
        updatePlayPauseButton();
    }
}

function stopText() {
    const wasPlaying = currentSynth !== null;
    
    // Firefox対応：明確に停止状態を設定
    isStopped = true;
    
    if (currentSynth) {
        speechSynthesis.cancel();
        currentSynth = null;
    }
    isPaused = false;
    currentLineIndex = 0;
    multiLangCurrentStep = 0;
    
    // Remove all highlighting
    document.querySelectorAll('.dialogue-line').forEach(el => {
        el.classList.remove('current');
    });
    document.querySelectorAll('.translation-line').forEach(el => {
        el.classList.remove('current');
    });
    // Clear any dynamic highlighting
    clearDynamicHighlight();
    
    // Only update status to "Stopped" if we were actually playing
    if (wasPlaying) {
        updateStatus('stopped', 'Stopped');
    }
    updatePlayPauseButton();
}

function updateStatus(type, message) {
    status.className = `status ${type}`;
    status.textContent = message;
}

function updatePlayPauseButton() {
    if (currentSynth && !isPaused) {
        // Currently playing
        playPauseBtn.textContent = '⏸️ Pause';
        playPauseBtn.className = 'pause-btn';
    } else {
        // Stopped or paused
        playPauseBtn.textContent = '▶️ Play';
        playPauseBtn.className = 'play-btn';
    }
}

// Speaker identification - creates a unified list across all languages
function identifySpeakers() {
    const allLanguageLines = parseAllLanguageTexts();
    const speakerMapping = new Map(); // Map to track speaker equivalences across languages
    let speakerIndex = 0;
    
    // Process each text entry to build speaker mapping
    texts.forEach((textObj, index) => {
        const speakers_fr = textObj.fr ? extractSpeakerFromLine(textObj.fr) : null;
        const speakers_en = textObj.en ? extractSpeakerFromLine(textObj.en) : null;
        const speakers_ja = textObj.ja ? extractSpeakerFromLine(textObj.ja) : null;
        
        // Use French as the primary language for speaker identification
        if (speakers_fr && !speakerMapping.has(speakers_fr)) {
            speakerMapping.set(speakers_fr, speakerIndex);
            if (speakers_en) speakerMapping.set(speakers_en, speakerIndex);
            if (speakers_ja) speakerMapping.set(speakers_ja, speakerIndex);
            speakerIndex++;
        }
    });
    
    // Create speakers array from French speakers (primary language)
    speakers = [];
    speakerMapping.forEach((index, speakerName) => {
        // Only add French speakers to maintain consistent indexing
        if (allLanguageLines.fr.some(line => line.speaker === speakerName)) {
            speakers[index] = speakerName;
        }
    });
    
    // Remove undefined entries and compact array
    speakers = speakers.filter(speaker => speaker !== undefined);
}

function extractSpeakerFromLine(line) {
    const colonIndex = line.indexOf(': ');
    return colonIndex !== -1 ? line.substring(0, colonIndex) : null;
}

function getSpeakerIndex(speakerName, lang, lineIndex) {
    // For languages other than French, we need to map the speaker to the French equivalent
    // by looking at the same line index in the French version
    if (lang === 'fr') {
        return speakers.indexOf(speakerName);
    }
    
    // For non-French languages, find the equivalent French speaker at the same line index
    if (lineIndex < texts.length && texts[lineIndex].fr) {
        const frenchSpeaker = extractSpeakerFromLine(texts[lineIndex].fr);
        return speakers.indexOf(frenchSpeaker);
    }
    
    // Fallback: try direct mapping
    return speakers.indexOf(speakerName);
}

// Voice management functions
function loadVoices() {
    availableVoices = speechSynthesis.getVoices();
}

function getFilteredVoices() {
    const selectedLang = languageSelect.value;
    const langCode = langCodes[selectedLang];
    
    // First try to get exact language match (e.g., fr-FR, en-US, ja-JP)
    let exactMatches = availableVoices.filter(voice => 
        voice.lang.toLowerCase() === langCode.toLowerCase()
    );
    
    // If we have exact matches, prioritize them
    if (exactMatches.length > 0) {
        return prioritizeVoices(exactMatches);
    }
    
    // Fallback to language base matching (fr, en, ja)
    const targetLangBase = langCode.split('-')[0].toLowerCase();
    const fallbackMatches = availableVoices.filter(voice => {
        const voiceLangBase = voice.lang.split('-')[0].toLowerCase();
        return voiceLangBase === targetLangBase;
    });
    
    return prioritizeVoices(fallbackMatches);
}

function prioritizeVoices(voices) {
    // Filter out Multilingual voices
    const nonMultilingualVoices = voices.filter(voice => 
        !voice.name.toLowerCase().includes('multilingual')
    );
    
    // Use filtered voices if available, otherwise use all voices
    const voicesToSort = nonMultilingualVoices.length > 0 ? nonMultilingualVoices : voices;
    
    // Sort voices with priority:
    // 1. localService = false (online voices)
    // 2. Non-multilingual voices
    // 3. Default voices
    // 4. Alphabetical order
    return voicesToSort.sort((a, b) => {
        // Priority 1: localService = false (online voices first)
        const aIsOnline = a.localService === false;
        const bIsOnline = b.localService === false;
        if (aIsOnline !== bIsOnline) {
            return bIsOnline - aIsOnline; // false (online) comes first
        }
        
        // Priority 2: Non-multilingual voices first
        const aIsMultilingual = a.name.toLowerCase().includes('multilingual');
        const bIsMultilingual = b.name.toLowerCase().includes('multilingual');
        if (aIsMultilingual !== bIsMultilingual) {
            return aIsMultilingual - bIsMultilingual; // false (non-multilingual) comes first
        }
        
        // Priority 3: Default voices first
        if (a.default !== b.default) {
            return b.default - a.default; // true comes first
        }
        
        // Priority 4: Alphabetical order
        return a.name.localeCompare(b.name);
    });
}


function autoAssignDefaultVoicesForLanguage(lang, filteredVoices) {
    // Only auto-assign if no voices are currently set for any speaker in this language
    const currentVoices = speakerVoicesByLanguage[lang];
    const hasExistingVoices = currentVoices.some(voice => voice !== undefined);
    if (hasExistingVoices || filteredVoices.length === 0) {
        return;
    }
    
    // Try to find gender-specific voices based on Microsoft voice naming patterns
    const maleVoices = filteredVoices.filter(voice => {
        const name = voice.name.toLowerCase();
        // French male names
        const frenchMaleNames = ['gerard', 'thierry', 'antoine', 'jean', 'remy', 'henri', 'fabrice'];
        // English male names  
        const englishMaleNames = ['david', 'guy', 'mark', 'richard', 'ryan', 'brian', 'christopher', 'eric', 'jacob', 'benjamin'];
        // Japanese male names
        const japaneseMaleNames = ['ichiro', 'keita'];
        
        const allMaleNames = [...frenchMaleNames, ...englishMaleNames, ...japaneseMaleNames];
        
        return name.includes('male') || name.includes('man') || name.includes('homme') || 
               name.includes('masculine') || allMaleNames.some(maleName => name.includes(maleName));
    });
    
    const femaleVoices = filteredVoices.filter(voice => {
        const name = voice.name.toLowerCase();
        // French female names
        const frenchFemaleNames = ['charline', 'sylvie', 'vivienne', 'denise', 'eloise', 'ariane'];
        // English female names
        const englishFemaleNames = ['aria', 'jenny', 'nancy', 'sara', 'jane', 'michelle', 'emma', 'elizabeth', 'amber'];
        // Japanese female names
        const japaneseFemaleNames = ['ayumi', 'haruka', 'sayaka', 'nanami'];
        
        const allFemaleNames = [...frenchFemaleNames, ...englishFemaleNames, ...japaneseFemaleNames];
        
        return name.includes('female') || name.includes('woman') || name.includes('femme') || 
               name.includes('feminine') || allFemaleNames.some(femaleName => name.includes(femaleName));
    });
    
    // Try to assign different gender voices if available
    if (speakers.length >= 2 && maleVoices.length > 0 && femaleVoices.length > 0) {
        // Alternate between female and male voices by speaker index
        let maleIndex = 0;
        let femaleIndex = 0;
        
        speakers.forEach((speaker, index) => {
            if (index % 2 === 0 && femaleIndex < femaleVoices.length) {
                currentVoices[index] = femaleVoices[femaleIndex++];
            } else if (maleIndex < maleVoices.length) {
                currentVoices[index] = maleVoices[maleIndex++];
            }
        });
    } else {
        // Fallback: assign different voices sequentially by index
        speakers.forEach((speaker, index) => {
            if (index < filteredVoices.length) {
                currentVoices[index] = filteredVoices[index];
            }
        });
    }
}

function createAllLanguageVoiceAssignments() {
    if (speakers.length === 0) {
        speakerVoicesDiv.style.display = 'none';
        return;
    }
    
    speakerVoicesDiv.style.display = 'block';
    
    // Create voice assignments for each language
    Object.keys(langCodes).forEach(lang => {
        createVoiceAssignmentsForLanguage(lang);
    });
}

function createVoiceAssignmentsForLanguage(lang) {
    const column = document.getElementById(`voiceAssignment-${lang}`);
    const speakerList = column.querySelector('.speaker-voice-list');
    speakerList.innerHTML = '';
    
    const filteredVoices = getFilteredVoicesForLanguage(lang);
    
    // Auto-assign different voices if no voices are currently set
    autoAssignDefaultVoicesForLanguage(lang, filteredVoices);
    
    speakers.forEach((speaker, speakerIndex) => {
        const assignment = document.createElement('div');
        assignment.className = 'speaker-voice-assignment';
        
        const voiceSelect = document.createElement('select');
        voiceSelect.className = 'speaker-voice-select';
        voiceSelect.setAttribute('data-speaker-index', speakerIndex);
        voiceSelect.setAttribute('data-lang', lang);
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = `Speaker ${speakerIndex + 1} - Default Voice`;
        voiceSelect.appendChild(defaultOption);
        
        // Find the previously selected voice for this speaker index in this language
        let selectedVoiceIndex = '';
        const currentSpeakerVoice = speakerVoicesByLanguage[lang][speakerIndex];
        
        // Add voice options
        filteredVoices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            if (voice.default) {
                option.textContent += ' - Default';
            }
            
            // Check if this was the previously selected voice
            if (currentSpeakerVoice && voice.name === currentSpeakerVoice.name && voice.lang === currentSpeakerVoice.lang) {
                selectedVoiceIndex = index;
            }
            
            voiceSelect.appendChild(option);
        });
        
        // Restore the previously selected voice
        voiceSelect.value = selectedVoiceIndex;
        
        // Add event listener for voice selection
        voiceSelect.addEventListener('change', (e) => {
            const speakerIndex = parseInt(e.target.getAttribute('data-speaker-index'));
            const targetLang = e.target.getAttribute('data-lang');
            const selectedIndex = e.target.value;
            
            if (selectedIndex === '') {
                speakerVoicesByLanguage[targetLang][speakerIndex] = undefined;
            } else {
                speakerVoicesByLanguage[targetLang][speakerIndex] = filteredVoices[parseInt(selectedIndex)];
            }
        });
        
        assignment.appendChild(voiceSelect);
        speakerList.appendChild(assignment);
    });
}

function getFilteredVoicesForLanguage(lang) {
    const langCode = langCodes[lang];
    
    // First try to get exact language match
    let exactMatches = availableVoices.filter(voice => 
        voice.lang.toLowerCase() === langCode.toLowerCase()
    );
    
    if (exactMatches.length > 0) {
        return prioritizeVoices(exactMatches);
    }
    
    // Fallback to language base matching
    const targetLangBase = langCode.split('-')[0].toLowerCase();
    const fallbackMatches = availableVoices.filter(voice => {
        const voiceLangBase = voice.lang.split('-')[0].toLowerCase();
        return voiceLangBase === targetLangBase;
    });
    
    return prioritizeVoices(fallbackMatches);
}

// Shared text parsing function - updated for new JSON array format
function parseAllLanguageTexts() {
    const allLanguageLines = {};
    const languages = ['fr', 'en', 'ja']; // サポートされている言語
    
    // 各言語のライン配列を初期化
    languages.forEach(lang => {
        allLanguageLines[lang] = [];
    });
    
    // 新形式のJSONデータを処理
    texts.forEach((textObj, index) => {
        languages.forEach(lang => {
            if (textObj[lang]) {
                const line = textObj[lang];
                // スピーカーとテキストを分離するために最初の ': ' を検索
                const colonIndex = line.indexOf(': ');
                if (colonIndex !== -1) {
                    allLanguageLines[lang].push({
                        index: index,
                        speaker: line.substring(0, colonIndex),
                        text: line.substring(colonIndex + 2), // +2 to skip ': '
                        fullLine: line
                    });
                } else {
                    // ': 'が見つからない場合、行全体をUnknownスピーカーのテキストとして扱う
                    allLanguageLines[lang].push({
                        index: index,
                        speaker: 'Unknown',
                        text: line,
                        fullLine: line
                    });
                }
            }
        });
    });
    
    return allLanguageLines;
}

// Shared speech synthesis function
function speakLineWithUtterance(lineIndex, lang, line, statusMessage, onComplete) {
    // Clear any dynamic highlighting
    clearDynamicHighlight();
    
    // Highlight current line in the specified language
    document.querySelectorAll('.translation-line').forEach(el => {
        const elLineIndex = parseInt(el.getAttribute('data-line-index'));
        const elLang = el.getAttribute('data-lang');
        el.classList.toggle('current', elLineIndex === lineIndex && elLang === lang);
    });
    
    // Get current line element for highlighting
    const currentLineElement = document.querySelector(`[data-line-index="${lineIndex}"][data-lang="${lang}"]`);
    
    // Scroll to current line
    if (currentLineElement) {
        const translationGroup = currentLineElement.closest('.translation-group');
        if (translationGroup) {
            translationGroup.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    if ('speechSynthesis' in window) {
        // Use only the text part (exclude speaker name)
        const speechText = line.text;
        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.lang = langCodes[lang];
        // Apply both global and language-specific rate
        const globalRate = parseFloat(rateSlider.value);
        const languageRate = languageRates[lang] || 1.0;
        utterance.rate = globalRate * languageRate;
        
        // Set speaker-specific voice for current language
        const currentSpeakerVoices = speakerVoicesByLanguage[lang];
        const speakerIndex = getSpeakerIndex(line.speaker, lang, lineIndex);
        const speakerVoice = currentSpeakerVoices[speakerIndex];
        if (speakerVoice) {
            utterance.voice = speakerVoice;
        }
        
        utterance.onstart = () => {
            updateStatus('playing', statusMessage);
        };
        
        // Add boundary event listener for dynamic highlighting
        utterance.onboundary = (event) => {
            if (event.name === 'word' && event.charLength) {
                highlightTextDynamically(currentLineElement, speechText, event.charIndex, event.charLength);
            }
        };
        
        utterance.onend = () => {
            // Clear dynamic highlighting when speech ends
            clearDynamicHighlight();
            
            if (onComplete && !isPaused && !isStopped) {
                onComplete();
            }
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            updateStatus('stopped', 'Error occurred during playback');
            // Clear dynamic highlighting on error
            clearDynamicHighlight();
        };
        
        currentSynth = utterance;
        speechSynthesis.speak(utterance);
    }
}

// Dynamic highlighting functions
function highlightTextDynamically(lineElement, originalText, charIndex, charLength) {
    if (!lineElement || !charLength || charLength <= 0) return;
    
    const textContainer = lineElement.querySelector('.text-container');
    if (!textContainer) return;
    
    const text = textContainer.getAttribute('data-original-text') || originalText;
    
    // Clear previous highlighting
    clearDynamicHighlight();
    
    // Calculate the end position using charLength
    const endIndex = charIndex + charLength;
    
    // Create highlighted version of text
    const beforeText = text.substring(0, charIndex);
    const highlightedText = text.substring(charIndex, endIndex);
    const afterText = text.substring(endIndex);
    
    // Replace text content with highlighted version
    textContainer.innerHTML = '';
    
    if (beforeText) {
        const beforeSpan = document.createElement('span');
        beforeSpan.textContent = beforeText;
        textContainer.appendChild(beforeSpan);
    }
    
    if (highlightedText) {
        const highlightSpan = document.createElement('span');
        highlightSpan.className = 'word speaking';
        highlightSpan.textContent = highlightedText;
        textContainer.appendChild(highlightSpan);
    }
    
    if (afterText) {
        const afterSpan = document.createElement('span');
        afterSpan.textContent = afterText;
        textContainer.appendChild(afterSpan);
    }
}

// Removed findWordEnd and getJapaneseScriptType functions - no longer needed since we only highlight when charLength is available

function clearDynamicHighlight() {
    // Remove all dynamic highlighting by restoring original text
    document.querySelectorAll('.text-container').forEach(container => {
        const originalText = container.getAttribute('data-original-text');
        if (originalText) {
            container.textContent = originalText;
        }
    });
}

// Settings management functions
function saveLanguageRateSettings() {
    localStorage.setItem('languageRates', JSON.stringify(languageRates));
}

function loadLanguageRateSettings() {
    try {
        const saved = localStorage.getItem('languageRates');
        if (saved) {
            const savedRates = JSON.parse(saved);
            languageRates = { ...languageRates, ...savedRates };
        }
        
        // Update UI to reflect loaded settings
        updateLanguageRateUI();
    } catch (error) {
        console.warn('Failed to load language rate settings:', error);
    }
}

function updateLanguageRateUI() {
    rateFrSlider.value = languageRates.fr;
    rateValueFr.textContent = languageRates.fr.toFixed(1) + 'x';
    
    rateEnSlider.value = languageRates.en;
    rateValueEn.textContent = languageRates.en.toFixed(1) + 'x';
    
    rateJaSlider.value = languageRates.ja;
    rateValueJa.textContent = languageRates.ja.toFixed(1) + 'x';
}

// Collapsible functionality for Speaker Voice Assignment
function toggleSpeakerVoices() {
    const container = document.getElementById('voiceAssignmentContainer');
    const icon = document.getElementById('toggleIcon');
    
    if (container.classList.contains('collapsed')) {
        container.classList.remove('collapsed');
        icon.classList.add('expanded');
        icon.textContent = '▲';
    } else {
        container.classList.add('collapsed');
        icon.classList.remove('expanded');
        icon.textContent = '▼';
    }
}
