
// ========================================
// 1. GET HTML ELEMENTS
// ========================================

const editor = document.getElementById("editor");
const lineNumbers = document.getElementById("line-numbers");

const saveButton = document.getElementById("save-btn");
const newFileButton = document.getElementById("new-file-btn");
const newFolderButton = document.getElementById("new-folder-btn");
const historyButton = document.getElementById("history-btn");

const historyModal = document.getElementById("history-modal");
const closeHistoryButton = document.getElementById("close-history-btn");
const historyFilename = document.getElementById("history-filename");
const historyList = document.getElementById("history-list");

const workspaceHeader = document.getElementById("workspace-header");
const fileTree = document.getElementById("file-tree");

const currentFile = document.getElementById("current-file");
const editorFilename = document.getElementById("editor-filename");

const saveStatus = document.getElementById("save-status");
const cursorPosition = document.getElementById("cursor-position");
const gitStatus = document.getElementById("git-status");
const fileType = document.getElementById("file-type");


// ========================================
// 2. APPLICATION VARIABLES
// ========================================

let activeFilePath = null;
let workspacePath = null;
let currentDirectory = null;
let saveTimer = null;
let selectedFileElement = null;

const AUTO_SAVE_DELAY = 2000;


// ========================================
// 3. HELPER FUNCTIONS
// ========================================

// Send requests to Flask and handle errors.

async function apiRequest(url, body) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}


// Join Windows paths correctly.

function joinPath(directory, name) {
    const separator = directory.includes("\\") ? "\\" : "/";
    const cleanDirectory = directory.replace(/[\\/]+$/, "");

    return cleanDirectory + separator + name;
}


// Get the parent directory without accidentally
// navigating above the workspace.

function getParentPath(path) {
    const cleanPath = path.replace(/[\\/]+$/, "");
    const lastSeparator = Math.max(
        cleanPath.lastIndexOf("\\"),
        cleanPath.lastIndexOf("/")
    );

    if (lastSeparator === -1) {
        return null;
    }

    // Preserve Windows drive roots, e.g. C:\
    if (lastSeparator === 2 && cleanPath[1] === ":") {
        return cleanPath.substring(0, 3);
    }

    if (lastSeparator === 0) {
        return cleanPath.substring(0, 1);
    }

    return cleanPath.substring(0, lastSeparator);
}


// Validate names entered by the user.

function isValidName(name) {
    const invalidCharacters = /[<>:"/\\|?*\x00-\x1F]/;

    return (
        name.length > 0 &&
        name.trim() === name &&
        name !== "." &&
        name !== ".." &&
        !invalidCharacters.test(name)
    );
}


// Get a suitable icon based on the file extension.

function getFileIcon(filename) {
    const extension = filename.includes(".")
        ? filename.split(".").pop().toLowerCase()
        : "";

    const icons = {
        txt: "📄",
        md: "📝",
        py: "🐍",
        html: "🌐",
        css: "🎨",
        js: "📜",
        json: "📋",
        csv: "📊",
        sql: "🗄️",
        xml: "📄",
        pdf: "📕",
        doc: "📘",
        docx: "📘",
        xlsx: "📗",
        png: "🖼️",
        jpg: "🖼️",
        jpeg: "🖼️"
    };

    return icons[extension] || "📄";
}


// ========================================
// 4. EDITOR INFORMATION
// ========================================

function updateLineNumbers() {
    const totalLines = editor.value.split("\n").length;

    lineNumbers.textContent = Array.from(
        { length: totalLines },
        (_, index) => index + 1
    ).join("\n");
}


function updateCursorPosition() {
    const cursor = editor.selectionStart;

    const textBeforeCursor = editor.value.substring(0, cursor);
    const lines = textBeforeCursor.split("\n");

    const line = lines.length;
    const column = lines[lines.length - 1].length + 1;

    cursorPosition.textContent = `Ln ${line}, Col ${column}`;
}


function updateFileInformation(path) {
    const filename = path.split(/[\\/]/).pop();

    currentFile.textContent = path;
    editorFilename.textContent = filename;

    const extension = filename.includes(".")
        ? filename.split(".").pop().toUpperCase()
        : "Plain Text";

    fileType.textContent = extension;
}


// ========================================
// 5. WORKSPACE SELECTION
// ========================================

async function selectWorkspace() {
    const path = prompt(
        "Enter the full path of your workspace folder:"
    );

    if (!path || !path.trim()) {
        return;
    }

    await loadDirectory(path.trim(), true);
}


// ========================================
// 6. LOAD DIRECTORY
// ========================================

async function loadDirectory(path, setAsWorkspace = false) {
    try {
        saveStatus.textContent = "Loading folder...";

        const data = await apiRequest(
            "/api/directory/list",
            { path }
        );

        if (!Array.isArray(data.items)) {
            throw new Error("Invalid directory response.");
        }

        currentDirectory = data.path || path;

        if (setAsWorkspace) {
            workspacePath = currentDirectory;

            workspaceHeader.title =
                `Workspace: ${workspacePath}`;
        }

        renderFileTree(data.items);

        saveStatus.textContent = "Ready";

    } catch (error) {
        saveStatus.textContent = "Folder loading failed";
        alert(error.message);
    }
}


// ========================================
// 7. RENDER FILE EXPLORER
// ========================================

function renderFileTree(items) {
    fileTree.replaceChildren();

    const hiddenFolders = [
        ".git",
        "venv",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "node_modules"
    ];

    const visibleItems = items
        .filter(item => !hiddenFolders.includes(item.name))
        .sort((a, b) => {
            if (a.type === "folder" && b.type !== "folder") {
                return -1;
            }

            if (a.type !== "folder" && b.type === "folder") {
                return 1;
            }

            return a.name.localeCompare(b.name);
        });


    // Back button

    if (currentDirectory !== workspacePath) {
        const backButton = document.createElement("button");

        backButton.type = "button";
        backButton.className = "file-tree-item back-button";
        backButton.textContent = "⬅  Back";

        backButton.addEventListener("click", async () => {
            const parent = getParentPath(currentDirectory);

            if (!parent) {
                return;
            }

            // Do not navigate outside the selected workspace.
            if (
                parent === workspacePath ||
                currentDirectory.startsWith(workspacePath + "\\") ||
                currentDirectory.startsWith(workspacePath + "/")
            ) {
                await loadDirectory(parent);
            }
        });

        fileTree.appendChild(backButton);
    }


    // Empty directory

    if (visibleItems.length === 0) {
        const message = document.createElement("div");

        message.className = "empty-message";
        message.textContent = "This folder is empty.";

        fileTree.appendChild(message);
        return;
    }


    // Create file and folder elements

    visibleItems.forEach(item => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "file-tree-item";

        button.dataset.path = item.path;

        const icon = document.createElement("span");
        icon.className = "file-item-icon";

        const name = document.createElement("span");
        name.className = "file-item-name";
        name.textContent = item.name;

        if (item.type === "folder") {
            icon.textContent = "📁";
        } else {
            icon.textContent = getFileIcon(item.name);
        }

        button.appendChild(icon);
        button.appendChild(name);


        // Highlight currently selected file.

        if (item.path === activeFilePath) {
            button.classList.add("active");
            selectedFileElement = button;
        }


        button.addEventListener("click", async () => {
            if (item.type === "folder") {
                await loadDirectory(item.path);
            } else {
                await openFile(item.path, button);
            }
        });

        fileTree.appendChild(button);
    });
}


// ========================================
// 8. OPEN FILE
// ========================================

async function openFile(path, selectedButton = null) {
    try {
        // Save pending changes before switching files.
        if (activeFilePath && editor.value !== lastSavedContent) {
            clearTimeout(saveTimer);
            const saved = await saveFile();
            if (!saved) {
                saveStatus.textContent = "Save before opening another file";
                return;
            }
            if (editor.value !== lastSavedContent) {
                saveStatus.textContent = "Save before opening another file";
                return;
            }
        }

        clearTimeout(saveTimer);

        saveStatus.textContent = "Opening...";

        const data = await apiRequest(
            "/api/files/open",
            { path }
        );

        activeFilePath = data.path;

        editor.value = data.content;
        editor.disabled = false;

        lastSavedContent = data.content;

        updateFileInformation(data.path);
        updateLineNumbers();
        updateCursorPosition();

        // Remove previous selection.
        if (selectedFileElement) {
            selectedFileElement.classList.remove("active");
        }

        // Highlight the newly opened file.
        if (selectedButton) {
            selectedButton.classList.add("active");
            selectedFileElement = selectedButton;
        }

        saveStatus.textContent = "File opened";
        gitStatus.textContent = "Git: Ready";

        editor.focus();

    } catch (error) {
        saveStatus.textContent = "Open failed";
        alert(error.message);
    }
}


// ========================================
// 9. SAVE FILE
// ========================================

let lastSavedContent = "";
let saveInProgress = false;

async function saveFile() {
    if (!activeFilePath) {
        alert("Please create or open a file first.");
        return;
    }

    if (saveInProgress) {
        return false;
    }

    const contentToSave = editor.value;

    try {
        saveInProgress = true;
        saveStatus.textContent = "Saving...";

        const data = await apiRequest(
            "/api/files/save",
            {
                path: activeFilePath,
                content: contentToSave
            }
        );

        lastSavedContent = contentToSave;

        if (data.git_committed) {
            gitStatus.textContent = "Git: Changes committed";
        } else if (data.git_error) {
            gitStatus.textContent = "Git: Commit failed – " + data.git_error;
        } else {
            gitStatus.textContent = "Git: No new changes";
        }

        // Check whether the user typed while saving.
        if (editor.value !== contentToSave) {
            scheduleAutoSave();
        } else {
            saveStatus.textContent = "All changes saved";
        }

        return true;

    } catch (error) {
        saveStatus.textContent = "Save failed";
        alert(error.message);
        return false;

    } finally {
        saveInProgress = false;
    }
}


// ========================================
// 10. AUTOMATIC SAVING
// ========================================

function scheduleAutoSave() {
    clearTimeout(saveTimer);

    saveStatus.textContent = "Unsaved changes";

    saveTimer = setTimeout(() => {
        saveFile();
    }, AUTO_SAVE_DELAY);
}


// ========================================
// 11. CREATE NEW FILE
// ========================================

async function createNewFile() {
    if (!currentDirectory) {
        alert("Please select a workspace first.");
        return;
    }

    const filename = prompt("Enter the new filename:");

    if (!filename) {
        return;
    }

    if (!isValidName(filename)) {
        alert("Please enter a valid filename.");
        return;
    }

    const path = joinPath(currentDirectory, filename);

    try {
        saveStatus.textContent = "Creating file...";

        const data = await apiRequest(
            "/api/files/create",
            { path }
        );

        await loadDirectory(currentDirectory);
        await openFile(data.path);

    } catch (error) {
        saveStatus.textContent = "File creation failed";
        alert(error.message);
    }
}


// ========================================
// 12. CREATE NEW FOLDER
// ========================================

async function createNewFolder() {
    if (!currentDirectory) {
        alert("Please select a workspace first.");
        return;
    }

    const folderName = prompt("Enter the new folder name:");

    if (!folderName) {
        return;
    }

    if (!isValidName(folderName)) {
        alert("Please enter a valid folder name.");
        return;
    }

    const path = joinPath(currentDirectory, folderName);

    try {
        saveStatus.textContent = "Creating folder...";

        await apiRequest(
            "/api/folders/create",
            { path }
        );

        await loadDirectory(currentDirectory);

        saveStatus.textContent = "Folder created";

    } catch (error) {
        saveStatus.textContent = "Folder creation failed";
        alert(error.message);
    }
}


// ========================================
// 13. EDITOR EVENT LISTENERS
// ========================================

editor.addEventListener("input", () => {
    updateLineNumbers();
    updateCursorPosition();
    scheduleAutoSave();
});

editor.addEventListener("click", updateCursorPosition);
editor.addEventListener("keyup", updateCursorPosition);
editor.addEventListener("select", updateCursorPosition);

editor.addEventListener("scroll", () => {
    lineNumbers.scrollTop = editor.scrollTop;
});


// ========================================
// 14. BUTTON EVENT LISTENERS
// ========================================

saveButton.addEventListener("click", async () => {
    clearTimeout(saveTimer);
    await saveFile();
});
document.addEventListener("keydown", async (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        clearTimeout(saveTimer);
        await saveFile();
    }
});
newFileButton.addEventListener("click", createNewFile);
newFolderButton.addEventListener("click", createNewFolder);
workspaceHeader.addEventListener("click", selectWorkspace);

window.addEventListener("beforeunload", (event) => {
    if (activeFilePath && editor.value !== lastSavedContent) {
        event.preventDefault();
        event.returnValue = "";
    }
});
// ========================================
// 15. FILE HISTORY
// ========================================

async function showFileHistory() {
    if (!activeFilePath) {
        alert("Please open a file first to view its history.");
        return;
    }

    historyModal.classList.remove("hidden");
    historyFilename.textContent = activeFilePath;
    historyList.replaceChildren();

    const loadingMessage = document.createElement("p");
    loadingMessage.className = "history-empty";
    loadingMessage.textContent = "Loading file history...";

    historyList.appendChild(loadingMessage);

    try {
        const data = await apiRequest(
            "/api/files/history",
            {
                path: activeFilePath,
                limit: 20
            }
        );

        historyList.replaceChildren();

        if (!Array.isArray(data.history) || data.history.length === 0) {
            const message = document.createElement("p");
            message.className = "history-empty";
            message.textContent = "No Git history found for this file.";

            historyList.appendChild(message);
            return;
        }

        data.history.forEach(commit => {
            const item = document.createElement("div");
            item.className = "history-item";

            const title = document.createElement("h3");
            title.textContent = commit.message || "No commit message";

            const author = document.createElement("p");
            author.textContent = `Author: ${commit.author}`;

            const date = document.createElement("p");
            const parsedDate = new Date(commit.date);

            date.textContent = `Date: ${
                Number.isNaN(parsedDate.getTime())
                    ? commit.date
                    : parsedDate.toLocaleString()
            }`;

            const hash = document.createElement("span");
            hash.className = "history-hash";
            hash.textContent = commit.short_hash;

            item.appendChild(title);
            item.appendChild(author);
            item.appendChild(date);
            item.appendChild(hash);

            historyList.appendChild(item);
        });

    } catch (error) {
        historyList.replaceChildren();

        const message = document.createElement("p");
        message.className = "history-empty";
        message.textContent = `Could not load history: ${error.message}`;

        historyList.appendChild(message);
    }
}


function closeFileHistory() {
    historyModal.classList.add("hidden");
}


historyButton.addEventListener("click", showFileHistory);
closeHistoryButton.addEventListener("click", closeFileHistory);


// Close the history panel when clicking outside it.
historyModal.addEventListener("click", (event) => {
    if (event.target === historyModal) {
        closeFileHistory();
    }
});


// Close history panel using the Escape key.
document.addEventListener("keydown", (event) => {
    if (
        event.key === "Escape" &&
        !historyModal.classList.contains("hidden")
    ) {
        closeFileHistory();
    }
});

// ========================================
// 16. INITIAL SETUP
// ========================================

updateLineNumbers();
updateCursorPosition();
