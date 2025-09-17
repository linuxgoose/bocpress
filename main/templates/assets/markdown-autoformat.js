// get textarea element
var bodyElem = document.querySelector('textarea[name="body"]');

// --- Paste handler: convert selection + pasted URL into Markdown link ---
function markdownAutoFormat(event) {
    const clipboardData = event.clipboardData || window.clipboardData;
    const pastedData = clipboardData.getData('text');

    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;

    if (start !== end) {
        event.preventDefault();

        const selectedText = bodyElem.value.substring(start, end);
        const before = bodyElem.value.substring(0, start);
        const after = bodyElem.value.substring(end);

        const markdownLink = `[${selectedText}](${pastedData})`;

        bodyElem.value = before + markdownLink + after;

        const newCursorPosition = before.length + markdownLink.length;
        bodyElem.setSelectionRange(newCursorPosition, newCursorPosition);
    }
}

// --- Keyboard shortcuts for formatting ---
function handleKeyDown(event) {
    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;
    const selectedText = bodyElem.value.substring(start, end);

    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const ctrlKey = isMac ? event.metaKey : event.ctrlKey;

    // --- Inline code: Ctrl/Cmd+Shift+C (Mac-safe) ---
    if (ctrlKey && event.shiftKey && event.key.toLowerCase() === 'c') {
        event.preventDefault();
        wrapSelection('`', '`');
        return;
    }

    // --- Bold: Ctrl/Cmd+B ---
    if (ctrlKey && event.key.toLowerCase() === 'b') {
        event.preventDefault();
        wrapSelection('**', '**');
        return;
    }

    // --- Italics: Ctrl/Cmd+I ---
    if (ctrlKey && event.key.toLowerCase() === 'i') {
        event.preventDefault();
        wrapSelection('*', '*');
        return;
    }

    // --- Strikethrough: Ctrl+Shift+S ---
    if (ctrlKey && event.shiftKey && event.key.toLowerCase() === 's') {
        event.preventDefault();
        wrapSelection('~~', '~~');
        return;
    }

    // --- Headings: Ctrl/Cmd+1..6 ---
    if (ctrlKey && !event.shiftKey) {
        const headingLevel = parseInt(event.key);
        if (headingLevel >= 1 && headingLevel <= 6) {
            event.preventDefault();
            insertAtLineStart('#'.repeat(headingLevel) + ' ');
            return;
        }
    }

    // --- Insert link: Ctrl/Cmd+K ---
    if (ctrlKey && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        const url = prompt('Enter URL:');
        if (url) wrapSelection('[', `](${url})`);
        return;
    }

    // --- Insert image: Ctrl/Cmd+Shift+L ---
    if (ctrlKey && event.shiftKey && event.key.toLowerCase() === 'l') {
        event.preventDefault();
        const url = prompt('Enter image URL:');
        if (url) wrapSelection('![', `](${url})`);
        return;
    }

    // --- Insert footnote: Ctrl/Cmd+Shift+F ---
    if (ctrlKey && event.shiftKey && event.key.toLowerCase() === 'f') {
        event.preventDefault();
        const footnoteId = prompt('Enter footnote label or number:');
        if (footnoteId) wrapSelection(`[^${footnoteId}]`, '');
        return;
    }

    // --- Insert table template: Ctrl/Cmd+Shift+T ---
    if (ctrlKey && event.shiftKey && event.key.toLowerCase() === 't') {
        event.preventDefault();
        const tableTemplate = '| Header 1 | Header 2 |\n| --- | --- |\n| Cell 1 | Cell 2 |\n';
        insertAtCursor(tableTemplate);
        return;
    }

    // --- Blockquote / list indentation ---
    if (event.key === 'Tab') {
        event.preventDefault();
        const lines = getSelectedLines();
        if (event.shiftKey) {
            // remove >
            replaceLines(lines, line => line.replace(/^>\s?/, ''));
            // remove list indentation
            replaceLines(lines, line => line.replace(/^ {1,2}/, ''));
        } else {
            // add >
            replaceLines(lines, line => '> ' + line);
            // add list indentation
            replaceLines(lines, line => '  ' + line);
        }
        return;
    }
}

// --- Helper to wrap selection with prefix/suffix ---
function wrapSelection(prefix, suffix) {
    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;
    const selectedText = bodyElem.value.substring(start, end);

    const before = bodyElem.value.substring(0, start);
    const after = bodyElem.value.substring(end);

    bodyElem.value = before + prefix + selectedText + suffix + after;

    bodyElem.setSelectionRange(
        start + prefix.length,
        end + prefix.length
    );
}

// --- Insert text at cursor (no selection) ---
function insertAtCursor(text) {
    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;

    const before = bodyElem.value.substring(0, start);
    const after = bodyElem.value.substring(end);

    bodyElem.value = before + text + after;

    const cursorPos = start + text.length;
    bodyElem.setSelectionRange(cursorPos, cursorPos);
}

// --- Insert at start of selected lines ---
function insertAtLineStart(prefix) {
    const lines = getSelectedLines();
    replaceLines(lines, line => prefix + line);
}

// --- Helper to get selected lines ---
function getSelectedLines() {
    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;
    const value = bodyElem.value;

    const before = value.substring(0, start);
    const after = value.substring(end);

    const startLineIndex = before.lastIndexOf('\n') + 1;
    const endLineIndex = end + after.indexOf('\n');
    const selectedText = value.substring(startLineIndex, endLineIndex === -1 ? value.length : endLineIndex);

    return { startLineIndex, endLineIndex: endLineIndex === -1 ? value.length : endLineIndex, text: selectedText };
}

// --- Helper to replace each line in a selection ---
function replaceLines(linesObj, fn) {
    const { startLineIndex, endLineIndex, text } = linesObj;
    const before = bodyElem.value.substring(0, startLineIndex);
    const after = bodyElem.value.substring(endLineIndex);

    const newText = text.split('\n').map(fn).join('\n');
    bodyElem.value = before + newText + after;

    bodyElem.setSelectionRange(startLineIndex, startLineIndex + newText.length);
}

// --- Event listeners for Undo/Redo ---
bodyElem.addEventListener('paste', markdownAutoFormat);
bodyElem.addEventListener('keydown', handleKeyDown);

function wrapSelection(prefix, suffix) {
    const start = bodyElem.selectionStart;
    const end = bodyElem.selectionEnd;
    const selectedText = bodyElem.value.substring(start, end);

    const wrapped = prefix + selectedText + suffix;

    // Use execCommand to keep undo stack
    bodyElem.focus();
    bodyElem.setSelectionRange(start, end);
    if (document.queryCommandSupported('insertText')) {
        document.execCommand('insertText', false, wrapped);
    } else {
        // fallback
        const before = bodyElem.value.substring(0, start);
        const after = bodyElem.value.substring(end);
        bodyElem.value = before + wrapped + after;
        bodyElem.setSelectionRange(start + prefix.length, end + prefix.length);
    }
}
