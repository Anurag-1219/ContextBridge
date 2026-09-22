const BACKEND_URL = "https://contextbridge-f6fv.onrender.com/compress-conversation";

const compressBtn = document.getElementById("compressBtn");
const copyBtn = document.getElementById("copyBtn");

const status = document.getElementById("status");
const stats = document.getElementById("stats");
const resultContainer = document.getElementById("resultContainer");

const messageCount = document.getElementById("messageCount");
const qualityScore = document.getElementById("qualityScore");
const compressionRatio = document.getElementById("compressionRatio");

const contextStatus = document.getElementById("contextStatus");
const result = document.getElementById("result");


async function ensureContentScript(tabId) {
    try {
        await chrome.tabs.sendMessage(tabId, {
            action: "ping"
        });

        return;
    } catch (error) {
        console.log("Content script not responding. Injecting content.js...");
    }

    await chrome.scripting.executeScript({
        target: {
            tabId: tabId
        },
        files: ["content.js"]
    });

    await new Promise(resolve => setTimeout(resolve, 100));

    const pingResponse = await chrome.tabs.sendMessage(tabId, {
        action: "ping"
    });

    if (!pingResponse || !pingResponse.success) {
        throw new Error("ContextBridge content script is not responding.");
    }
}


compressBtn.addEventListener("click", async () => {
    status.textContent = "Extracting conversation...";
    compressBtn.disabled = true;

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (!tab || !tab.id) {
            throw new Error("Active tab not found.");
        }

        if (
            !tab.url ||
            (
                !tab.url.startsWith("https://chatgpt.com/") &&
                !tab.url.startsWith("https://chat.openai.com/")
            )
        ) {
            throw new Error(
                "Please open a ChatGPT conversation before using ContextBridge."
            );
        }

        await ensureContentScript(tab.id);

        const response = await chrome.tabs.sendMessage(
            tab.id,
            {
                action: "extractConversation"
            }
        );

        if (!response || !response.success) {
            throw new Error("Conversation extraction failed.");
        }

        if (!response.messages || response.messages.length === 0) {
            throw new Error("No conversation messages found.");
        }

        status.textContent =
            `Sending ${response.messages.length} messages...`;

        const backendResponse = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: response.messages
            })
        });

        if (!backendResponse.ok) {
            throw new Error(
                `Backend error: ${backendResponse.status}`
            );
        }

        const data = await backendResponse.json();

        console.log("CONTEXTBRIDGE BACKEND RESPONSE:", data);

        let compressedText = "";

        if (typeof data.compression === "string") {
            compressedText = data.compression;
        } else if (data.compression) {
            compressedText =
                data.compression.text ||
                data.compression.compressed_context ||
                data.compression.content ||
                "";
        }

        let score = null;

        if (typeof data.quality === "number") {
            score = data.quality;
        } else if (data.quality) {
            score = data.quality.quality_score;

            if (score === undefined) {
                score = data.quality.score;
            }
        }

        const originalTokens =
            data.token_metrics?.original_tokens;

        const compressedTokens =
            data.token_metrics?.compressed_tokens;

        result.value = compressedText;

        messageCount.textContent =
            response.messages.length;

        qualityScore.textContent =
            typeof score === "number"
                ? `${score}%`
                : "-";

        if (typeof score === "number") {
            if (score >= 80) {
                contextStatus.textContent = "Excellent";
            } else if (score >= 60) {
                contextStatus.textContent = "Good";
            } else {
                contextStatus.textContent = "Needs Review";
            }
        } else {
            contextStatus.textContent = "Not Evaluated";
        }

        if (
            typeof originalTokens === "number" &&
            typeof compressedTokens === "number" &&
            originalTokens > 0
        ) {
            const reduction =
                (1 - compressedTokens / originalTokens) * 100;

            if (reduction >= 0) {
                compressionRatio.textContent =
                    `${reduction.toFixed(1)}%`;
            } else {
                compressionRatio.textContent =
                    "Expanded";
            }
        } else {
            compressionRatio.textContent = "-";
        }

        stats.classList.remove("hidden");
        resultContainer.classList.remove("hidden");

        status.textContent = compressedText
            ? "Compression complete."
            : "Compression completed, but no context was returned.";
    }
    catch (error) {
        console.error("ContextBridge Error:", error);
        status.textContent = `Error: ${error.message}`;
    }
    finally {
        compressBtn.disabled = false;
    }
});


copyBtn.addEventListener("click", async () => {
    if (!result.value) {
        return;
    }

    await navigator.clipboard.writeText(result.value);

    const oldText = copyBtn.textContent;
    copyBtn.textContent = "Copied!";

    setTimeout(() => {
        copyBtn.textContent = oldText;
    }, 1200);
});
