/**
 * CryptoGraph — Frontend Application
 * 
 * Handles all user interactions: algorithm selection, operation switching,
 * dynamic form rendering, API calls via fetch(), result display,
 * copy-to-clipboard, RSA key download, file upload, and navigation.
 * 
 * No framework dependencies — pure vanilla JavaScript.
 */

// ==========================================================================
// CONFIGURATION
// ==========================================================================

/** API base URL (empty string = same origin) */
const API_BASE = '';

/** Algorithm metadata — defines available operations and UI behavior */
const ALGORITHMS = {
    caesar: {
        name: 'Caesar Cipher',
        operations: ['encrypt', 'decrypt'],
        fields: ['text', 'shift', 'alphabet'],
        isClassic: true,
        info: 'The Caesar cipher shifts each letter by a fixed number of positions in the alphabet. It is one of the oldest and simplest encryption techniques, named after Julius Caesar.',
    },
    vigenere: {
        name: 'Vigenère Cipher',
        operations: ['encrypt', 'decrypt'],
        fields: ['text', 'keyword'],
        isClassic: true,
        info: 'The Vigenère cipher uses a keyword to apply different shifts to each letter. It was considered unbreakable for centuries, but is now easily cracked with frequency analysis.',
    },
    sha256: {
        name: 'SHA-256',
        operations: ['hash', 'hash-file'],
        fields: ['text'],
        isClassic: false,
        info: 'SHA-256 is a one-way cryptographic hash function. It produces a fixed 64-character hexadecimal fingerprint. You cannot reverse a hash back to the original input.',
    },
    rsa: {
        name: 'RSA',
        operations: ['generate-keys', 'encrypt', 'decrypt', 'sign', 'verify'],
        fields: ['text', 'public-key', 'private-key'],
        isClassic: false,
        info: 'RSA is an asymmetric encryption algorithm using a pair of keys. The public key encrypts; the private key decrypts. It can also create digital signatures for data integrity.',
    },
};

// ==========================================================================
// STATE
// ==========================================================================

let currentAlgorithm = 'caesar';
let currentOperation = 'encrypt';
let lastGeneratedKeys = null;

// ==========================================================================
// DOM REFERENCES
// ==========================================================================

const dom = {
    // Navigation
    navToggle:      document.getElementById('nav-toggle'),
    navLinks:       document.getElementById('nav-links'),

    // Algorithm tabs
    algoTabs:       document.querySelectorAll('.algo-tab'),
    algoCards:       document.querySelectorAll('.algo-card'),

    // Operation selector
    opSelector:     document.getElementById('operation-selector'),

    // Form
    form:           document.getElementById('crypto-form'),
    inputText:      document.getElementById('input-text'),
    inputShift:     document.getElementById('input-shift'),
    shiftValue:     document.getElementById('shift-value'),
    inputAlphabet:  document.getElementById('input-alphabet'),
    inputKeyword:   document.getElementById('input-keyword'),
    inputPublicKey: document.getElementById('input-public-key'),
    inputPrivateKey:document.getElementById('input-private-key'),
    inputSignature: document.getElementById('input-signature'),
    inputFile:      document.getElementById('input-file'),

    // Form groups (for show/hide)
    groupText:      document.getElementById('group-text-input'),
    groupShift:     document.getElementById('group-shift'),
    groupAlphabet:  document.getElementById('group-alphabet'),
    groupKeyword:   document.getElementById('group-keyword'),
    groupPublicKey: document.getElementById('group-public-key'),
    groupPrivateKey:document.getElementById('group-private-key'),
    groupSignature: document.getElementById('group-signature'),
    groupFileUpload:document.getElementById('group-file-upload'),

    // Buttons
    btnExecute:     document.getElementById('btn-execute'),
    btnExecuteText: document.getElementById('btn-execute-text'),
    btnSpinner:     document.getElementById('btn-spinner'),
    btnClear:       document.getElementById('btn-clear'),
    btnCopy:        document.getElementById('btn-copy'),
    btnDownloadKeys:document.getElementById('btn-download-keys'),

    // Result
    resultOutput:   document.getElementById('result-output'),

    // Info
    algoInfo:       document.getElementById('algo-info'),
    algoInfoTitle:  document.querySelector('.algo-info-title'),
    algoInfoText:   document.getElementById('algo-info-text'),

    // Error display
    textError:      document.getElementById('input-text-error'),
};

// ==========================================================================
// NAVIGATION
// ==========================================================================

/** Toggle mobile hamburger menu */
function initNavigation() {
    dom.navToggle.addEventListener('click', () => {
        const isOpen = dom.navLinks.classList.toggle('open');
        dom.navToggle.classList.toggle('active');
        dom.navToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close menu when a nav link is clicked
    dom.navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            dom.navLinks.classList.remove('open');
            dom.navToggle.classList.remove('active');
            dom.navToggle.setAttribute('aria-expanded', 'false');
        });
    });
}

// ==========================================================================
// ALGORITHM SELECTION
// ==========================================================================

/** Switch the active algorithm and update the UI */
function selectAlgorithm(algorithm) {
    currentAlgorithm = algorithm;
    const config = ALGORITHMS[algorithm];

    // Update tab active states
    dom.algoTabs.forEach(tab => {
        const isActive = tab.dataset.algorithm === algorithm;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });

    // Update card active states
    dom.algoCards.forEach(card => {
        card.classList.toggle('selected', card.dataset.algorithm === algorithm);
    });

    // Set default operation for this algorithm
    currentOperation = config.operations[0];

    // Render operation buttons
    renderOperations(config.operations);

    // Update form fields visibility
    updateFormFields();
    updateShiftValue();

    // Update info panel
    dom.algoInfoTitle.textContent = `About ${config.name}`;
    dom.algoInfoText.textContent = config.info;

    // Update button text
    updateExecuteButton();

    // Show/hide download keys button
    dom.btnDownloadKeys.style.display = 'none';
}

/** Render operation selector buttons */
function renderOperations(operations) {
    dom.opSelector.innerHTML = '';

    operations.forEach(op => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `op-btn ${op === currentOperation ? 'active' : ''}`;
        btn.textContent = formatOperationName(op);
        btn.dataset.operation = op;
        btn.addEventListener('click', () => selectOperation(op));
        dom.opSelector.appendChild(btn);
    });
}

/** Switch the active operation */
function selectOperation(operation) {
    currentOperation = operation;

    // Update button active states
    dom.opSelector.querySelectorAll('.op-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.operation === operation);
    });

    updateFormFields();
    updateExecuteButton();
}

/** Format operation name for display */
function formatOperationName(op) {
    const names = {
        'encrypt': 'Encrypt',
        'decrypt': 'Decrypt',
        'hash': 'Hash Text',
        'hash-file': 'Hash File',
        'generate-keys': 'Generate Keys',
        'sign': 'Sign',
        'verify': 'Verify',
    };
    return names[op] || op;
}

// ==========================================================================
// FORM FIELD MANAGEMENT
// ==========================================================================

/** Show/hide form fields based on current algorithm + operation */
function updateFormFields() {
    // Hide all optional groups
    const allGroups = [
        dom.groupShift, dom.groupAlphabet, dom.groupKeyword,
        dom.groupPublicKey, dom.groupPrivateKey,
        dom.groupSignature, dom.groupFileUpload,
    ];
    allGroups.forEach(g => g.style.display = 'none');

    // Determine which fields to show
    const algo = currentAlgorithm;
    const op = currentOperation;

    // Text input: always shown except for generate-keys and hash-file
    dom.groupText.style.display = (op === 'generate-keys' || op === 'hash-file') ? 'none' : 'flex';

    // Algorithm-specific fields
    if (algo === 'caesar') {
        dom.groupShift.style.display = 'flex';
        dom.groupAlphabet.style.display = 'flex';
    } else if (algo === 'vigenere') {
        dom.groupKeyword.style.display = 'flex';
    } else if (algo === 'sha256' && op === 'hash-file') {
        dom.groupFileUpload.style.display = 'flex';
    } else if (algo === 'rsa') {
        if (op === 'encrypt') {
            dom.groupPublicKey.style.display = 'flex';
        } else if (op === 'decrypt') {
            dom.groupPrivateKey.style.display = 'flex';
        } else if (op === 'sign') {
            dom.groupPrivateKey.style.display = 'flex';
        } else if (op === 'verify') {
            dom.groupPublicKey.style.display = 'flex';
            dom.groupSignature.style.display = 'flex';
        }
    }

    // Clear any previous errors
    clearErrors();
}

/** Update the execute button label */
function updateExecuteButton() {
    dom.btnExecuteText.textContent = formatOperationName(currentOperation);
}

// ==========================================================================
// FORM VALIDATION
// ==========================================================================

/** Validate form before submission. Returns true if valid. */
function validateForm() {
    clearErrors();
    const op = currentOperation;

    // Text input required for most operations
    if (op !== 'generate-keys' && op !== 'hash-file') {
        if (!dom.inputText.value.trim()) {
            showError(dom.textError, 'Please enter some text.');
            dom.inputText.focus();
            return false;
        }
    }

    // File required for hash-file
    if (op === 'hash-file') {
        if (!dom.inputFile.files || !dom.inputFile.files[0]) {
            showError(dom.textError, 'Please select a file to hash.');
            return false;
        }
    }

    // RSA: require appropriate keys
    if (currentAlgorithm === 'rsa') {
        if ((op === 'encrypt') && !dom.inputPublicKey.value.trim()) {
            showError(dom.textError, 'Please provide a public key. Generate keys first.');
            return false;
        }
        if ((op === 'decrypt' || op === 'sign') && !dom.inputPrivateKey.value.trim()) {
            showError(dom.textError, 'Please provide a private key. Generate keys first.');
            return false;
        }
        if (op === 'verify') {
            if (!dom.inputPublicKey.value.trim()) {
                showError(dom.textError, 'Please provide a public key.');
                return false;
            }
            if (!dom.inputSignature.value.trim()) {
                showError(dom.textError, 'Please provide a signature to verify.');
                return false;
            }
        }
    }

    // Vigenère: keyword must be letters only
    if (currentAlgorithm === 'vigenere') {
        const kw = dom.inputKeyword.value.trim();
        if (kw && !/^[a-zA-Z]+$/.test(kw)) {
            showError(dom.textError, 'Keyword must contain only letters.');
            return false;
        }
    }

    return true;
}

function showError(element, message) {
    element.textContent = message;
}

function clearErrors() {
    dom.textError.textContent = '';
}

function updateShiftValue(value = dom.inputShift.value) {
    dom.shiftValue.value = String(value);
    dom.shiftValue.textContent = String(value);
}

// ==========================================================================
// API CALLS
// ==========================================================================

/** Execute the current operation by calling the API */
async function executeOperation() {
    if (!validateForm()) return;

    setLoading(true);

    try {
        let result;
        const algo = currentAlgorithm;
        const op = currentOperation;

        if (algo === 'caesar') {
            result = await callCaesarAPI(op);
        } else if (algo === 'vigenere') {
            result = await callVigenereAPI(op);
        } else if (algo === 'sha256') {
            result = op === 'hash-file' ? await callHashFileAPI() : await callHashAPI();
        } else if (algo === 'rsa') {
            result = await callRSAAPI(op);
        }

        displayResult(result);
    } catch (error) {
        displayError(error.message || 'An unexpected error occurred.');
    } finally {
        setLoading(false);
    }
}

/** Caesar cipher API call */
async function callCaesarAPI(operation) {
    const body = {
        text: dom.inputText.value,
        shift: parseInt(dom.inputShift.value) || 3,
    };

    const alphabet = dom.inputAlphabet.value.trim();
    if (alphabet) body.alphabet = alphabet;

    const response = await fetch(`${API_BASE}/api/classical/caesar/${operation}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    return handleResponse(response);
}

/** Vigenère cipher API call */
async function callVigenereAPI(operation) {
    const body = {
        text: dom.inputText.value,
        keyword: dom.inputKeyword.value.trim() || 'cryptolab',
    };

    const response = await fetch(`${API_BASE}/api/classical/vigenere/${operation}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    return handleResponse(response);
}

/** SHA-256 text hash API call */
async function callHashAPI() {
    const response = await fetch(`${API_BASE}/api/modern/hash/sha256`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: dom.inputText.value }),
    });

    return handleResponse(response);
}

/** SHA-256 file hash API call */
async function callHashFileAPI() {
    const formData = new FormData();
    formData.append('file', dom.inputFile.files[0]);

    const response = await fetch(`${API_BASE}/api/files/hash`, {
        method: 'POST',
        body: formData,
    });

    return handleResponse(response);
}

/** RSA API calls (keygen, encrypt, decrypt, sign, verify) */
async function callRSAAPI(operation) {
    if (operation === 'generate-keys') {
        const response = await fetch(`${API_BASE}/api/modern/rsa/generate-keys`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key_size: 2048 }),
        });
        const data = await handleResponse(response);

        // Store keys and auto-fill key fields
        lastGeneratedKeys = {
            privateKey: data.private_key,
            publicKey: data.public_key,
        };
        dom.inputPublicKey.value = data.public_key;
        dom.inputPrivateKey.value = data.private_key;
        dom.btnDownloadKeys.style.display = 'inline-flex';

        return data;
    }

    if (operation === 'encrypt') {
        const response = await fetch(`${API_BASE}/api/modern/rsa/encrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: dom.inputText.value,
                public_key: dom.inputPublicKey.value,
            }),
        });
        return handleResponse(response);
    }

    if (operation === 'decrypt') {
        const response = await fetch(`${API_BASE}/api/modern/rsa/decrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ciphertext: dom.inputText.value,
                private_key: dom.inputPrivateKey.value,
            }),
        });
        return handleResponse(response);
    }

    if (operation === 'sign') {
        const response = await fetch(`${API_BASE}/api/modern/rsa/sign`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: dom.inputText.value,
                private_key: dom.inputPrivateKey.value,
            }),
        });
        return handleResponse(response);
    }

    if (operation === 'verify') {
        const response = await fetch(`${API_BASE}/api/modern/rsa/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: dom.inputText.value,
                signature: dom.inputSignature.value,
                public_key: dom.inputPublicKey.value,
            }),
        });
        return handleResponse(response);
    }
}

/** Handle API response — parse JSON or throw error */
async function handleResponse(response) {
    const data = await response.json();

    if (!response.ok) {
        const detail = data.detail || JSON.stringify(data);
        throw new Error(`API Error (${response.status}): ${detail}`);
    }

    return data;
}

// ==========================================================================
// RESULT DISPLAY
// ==========================================================================

/** Display a successful result in the output panel */
function displayResult(data) {
    let output = '';

    if (data.private_key && data.public_key) {
        // RSA key generation result
        output = `🔑 RSA Key Pair Generated (${data.key_size}-bit)\n\n`;
        output += `━━━ Public Key ━━━\n${data.public_key}\n`;
        output += `━━━ Private Key ━━━\n${data.private_key}`;
    } else if (data.valid !== undefined) {
        // Signature verification result
        const icon = data.valid ? '✅' : '❌';
        output = `${icon} ${data.message}`;
    } else if (data.result) {
        // Standard crypto result
        output = data.result;
    } else {
        output = JSON.stringify(data, null, 2);
    }

    dom.resultOutput.textContent = output;
    dom.resultOutput.classList.remove('result-placeholder');
}

/** Display an error in the output panel */
function displayError(message) {
    dom.resultOutput.textContent = `❌ Error: ${message}`;
    dom.resultOutput.style.color = 'var(--color-error)';

    // Reset color after next successful result
    setTimeout(() => {
        dom.resultOutput.style.color = '';
    }, 0);
}

// ==========================================================================
// UTILITY ACTIONS
// ==========================================================================

/** Copy result to clipboard */
async function copyResult() {
    const text = dom.resultOutput.textContent;
    if (!text || text.includes('Select an algorithm')) return;

    try {
        await navigator.clipboard.writeText(text);

        // Visual feedback
        dom.btnCopy.classList.add('copied');
        setTimeout(() => dom.btnCopy.classList.remove('copied'), 1500);
    } catch {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        dom.btnCopy.classList.add('copied');
        setTimeout(() => dom.btnCopy.classList.remove('copied'), 1500);
    }
}

/** Download RSA keys as .pem files */
function downloadKeys() {
    if (!lastGeneratedKeys) return;

    downloadFile('public_key.pem', lastGeneratedKeys.publicKey);
    downloadFile('private_key.pem', lastGeneratedKeys.privateKey);
}

/** Helper: trigger a file download */
function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/** Clear all form fields and results */
function clearAll() {
    dom.inputText.value = '';
    dom.inputShift.value = '3';
    updateShiftValue();
    dom.inputAlphabet.value = '';
    dom.inputKeyword.value = 'cryptolab';
    dom.inputPublicKey.value = '';
    dom.inputPrivateKey.value = '';
    dom.inputSignature.value = '';
    dom.inputFile.value = '';

    dom.resultOutput.innerHTML = '<p class="result-placeholder">Select an algorithm and operation, then enter your text to see results here.</p>';
    dom.btnDownloadKeys.style.display = 'none';
    lastGeneratedKeys = null;

    clearErrors();
}

/** Toggle loading state on the execute button */
function setLoading(loading) {
    if (loading) {
        dom.btnExecute.classList.add('loading');
        dom.btnExecute.disabled = true;
    } else {
        dom.btnExecute.classList.remove('loading');
        dom.btnExecute.disabled = false;
    }
}

// ==========================================================================
// EVENT LISTENERS
// ==========================================================================

function initEventListeners() {
    // Algorithm tabs
    dom.algoTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            selectAlgorithm(tab.dataset.algorithm);
        });
    });

    // Algorithm cards → select + scroll to workspace
    dom.algoCards.forEach(card => {
        card.addEventListener('click', () => {
            selectAlgorithm(card.dataset.algorithm);
            document.getElementById('workspace').scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Form submission
    dom.form.addEventListener('submit', (e) => {
        e.preventDefault();
        executeOperation();
    });

    // Clear button
    dom.btnClear.addEventListener('click', clearAll);

    // Copy button
    dom.btnCopy.addEventListener('click', copyResult);

    // Download keys button
    dom.btnDownloadKeys.addEventListener('click', downloadKeys);

    // Shift slider value
    dom.inputShift.addEventListener('input', (event) => {
        updateShiftValue(event.target.value);
    });
    dom.inputShift.addEventListener('change', (event) => {
        updateShiftValue(event.target.value);
    });
}

// ==========================================================================
// INITIALIZATION
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initEventListeners();
    updateShiftValue();

    // Set initial state
    selectAlgorithm('caesar');
});
