// Text data is loaded from external file
const texts = podcastTexts;

// Language codes for speech synthesis
const langCodes = {
    fr: 'fr-FR',
    en: 'en-US',
    ja: 'ja-JP'
};

let currentSynth = null;
let isPaused = false;
let currentLineIndex = 0;
let dialogueLines = [];
// Removed: currentWordIndex and currentLineWords are no longer needed for dynamic highlighting
let availableVoices = [];
let speakers = [];
let speakerVoicesByLanguage = {
    fr: {},
    en: {},
    ja: {}
}; // Store voice settings per language
let isMultiLanguageMode = false;
let multiLangCurrentStep = 0; // 0: fr, 1: en, 2: ja

// Language-specific speed settings
let languageRates = {
    fr: 1.0,
    en: 1.0,
    ja: 1.5
};

// DOM elements
const languageSelect = document.getElementById('language');
const playBtn = document.getElementById('playBtn');
const pauseBtn = document.getElementById('pauseBtn');
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
function init() {
    // Initialize multi-language mode based on default selection
    isMultiLanguageMode = (languageSelect.value === 'multi');
    
    loadVoices();
    loadLanguageRateSettings();
    loadText();
    
    // Event listeners
    languageSelect.addEventListener('change', onLanguageChange);
    playBtn.addEventListener('click', playText);
    pauseBtn.addEventListener('click', pauseText);
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
                if (!isPaused) {
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
                if (!isPaused) {
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


function playText() {
    if (isPaused && currentSynth) {
        speechSynthesis.resume();
        isPaused = false;
        updateStatus('playing', 'Playing...');
        return;
    }
    
    currentLineIndex = 0;
    multiLangCurrentStep = 0;
    
    if (isMultiLanguageMode) {
        speakLineMultiLanguage(currentLineIndex);
    } else {
        speakLine(currentLineIndex);
    }
}

function playFromLine(lineIndex) {
    stopText();
    currentLineIndex = lineIndex;
    const selectedLang = languageSelect.value;
    speakLineInLanguage(currentLineIndex, selectedLang);
}

function playFromLineInLanguage(lineIndex, lang) {
    stopText();
    currentLineIndex = lineIndex;
    
    if (lang === 'multi' || isMultiLanguageMode) {
        multiLangCurrentStep = 0;
        speakLineMultiLanguage(currentLineIndex);
    } else {
        speakLineInLanguage(currentLineIndex, lang);
    }
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
                if (isMultiLanguageMode && !isPaused) {
                    speakLineMultiLanguage(currentLineIndex);
                }
            }, 800); // Longer pause between lines
        } else {
            // Continue with next language for the same line
            setTimeout(() => {
                if (isMultiLanguageMode && !isPaused) {
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
        setTimeout(() => speakLineInLanguage(currentLineIndex, lang), 500); // Short pause between lines
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
    }
}

function stopText() {
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
    
    updateStatus('stopped', 'Stopped');
}

function updateStatus(type, message) {
    status.className = `status ${type}`;
    status.textContent = message;
}

// Speaker identification
function identifySpeakers() {
    const uniqueSpeakers = new Set();
    if (dialogueLines && Array.isArray(dialogueLines)) {
        dialogueLines.forEach(line => {
            if (line && line.speaker && line.text) { // Only count lines with both speaker and text
                uniqueSpeakers.add(line.speaker);
            }
        });
    }
    speakers = Array.from(uniqueSpeakers);
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
    const hasExistingVoices = speakers.some(speaker => currentVoices[speaker]);
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
        // Assign female voice to Camille, male voice to Luc
        if (speakers.includes('Camille')) {
            currentVoices['Camille'] = femaleVoices[0];
        }
        if (speakers.includes('Luc')) {
            currentVoices['Luc'] = maleVoices[0];
        }
        
        // Handle additional speakers with alternating pattern
        let maleIndex = speakers.includes('Luc') ? 1 : 0;
        let femaleIndex = speakers.includes('Camille') ? 1 : 0;
        
        speakers.forEach((speaker, index) => {
            if (speaker !== 'Camille' && speaker !== 'Luc' && !currentVoices[speaker]) {
                if (index % 2 === 0 && femaleIndex < femaleVoices.length) {
                    currentVoices[speaker] = femaleVoices[femaleIndex++];
                } else if (maleIndex < maleVoices.length) {
                    currentVoices[speaker] = maleVoices[maleIndex++];
                }
            }
        });
    } else {
        // Fallback: assign different voices sequentially
        speakers.forEach((speaker, index) => {
            if (index < filteredVoices.length) {
                currentVoices[speaker] = filteredVoices[index];
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
    
    speakers.forEach(speaker => {
        const assignment = document.createElement('div');
        assignment.className = 'speaker-voice-assignment';
        
        const speakerNameSpan = document.createElement('span');
        speakerNameSpan.className = `speaker-name ${speaker.toLowerCase()}`;
        speakerNameSpan.textContent = speaker + ':';
        
        const voiceSelect = document.createElement('select');
        voiceSelect.className = 'speaker-voice-select';
        voiceSelect.setAttribute('data-speaker', speaker);
        voiceSelect.setAttribute('data-lang', lang);
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Use Default Voice';
        voiceSelect.appendChild(defaultOption);
        
        // Find the previously selected voice for this speaker in this language
        let selectedVoiceIndex = '';
        const currentSpeakerVoice = speakerVoicesByLanguage[lang][speaker];
        
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
            const speakerName = e.target.getAttribute('data-speaker');
            const targetLang = e.target.getAttribute('data-lang');
            const selectedIndex = e.target.value;
            
            if (selectedIndex === '') {
                delete speakerVoicesByLanguage[targetLang][speakerName];
            } else {
                speakerVoicesByLanguage[targetLang][speakerName] = filteredVoices[parseInt(selectedIndex)];
            }
        });
        
        assignment.appendChild(speakerNameSpan);
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

// Shared text parsing function
function parseAllLanguageTexts() {
    const allLanguageLines = {};
    Object.keys(texts).forEach(lang => {
        const text = texts[lang];
        allLanguageLines[lang] = text.split('\n').filter(line => line.trim() !== '').map((line, index) => {
            // Find the first occurrence of ': ' to separate speaker from text
            const colonIndex = line.indexOf(': ');
            if (colonIndex !== -1) {
                return {
                    index: index,
                    speaker: line.substring(0, colonIndex),
                    text: line.substring(colonIndex + 2), // +2 to skip ': '
                    fullLine: line
                };
            } else {
                // If no ': ' found, treat the entire line as text with unknown speaker
                return {
                    index: index,
                    speaker: 'Unknown',
                    text: line,
                    fullLine: line
                };
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
        const speakerVoice = currentSpeakerVoices[line.speaker];
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
            
            if (onComplete && !isPaused) {
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

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);