const compressBtn = document.getElementById("compressBtn");
const status = document.getElementById("status");
const conversationBox = document.getElementById("conversation");

compressBtn.addEventListener("click", async () => {
    status.textContent = "Extracting conversation...";
    conversationBox.textContent = "";

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (!tab || !tab.id) {
            status.textContent = "No active tab found.";
            return;
        }

        const response = await chrome.tabs.sendMessage(tab.id, {
            action: "extractConversation"
        });

        if (!response || !response.success) {
            status.textContent = "Failed to extract conversation.";
            return;
        }

        status.textContent =
            `Extracted ${response.messages.length} messages. Sending to backend...`;

        const backendResponse = await fetch(
            "http://127.0.0.1:8000/process-conversation",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    messages: response.messages
                })
            }
        );

        if (!backendResponse.ok) {
            throw new Error("Backend request failed");
        }

        const processedData = await backendResponse.json();

        status.textContent =
            `Processed ${processedData.stats.total_messages} messages. ` +
            `Estimated tokens: ${processedData.stats.estimated_tokens}`;

        processedData.messages.forEach((message) => {
            const messageBox = document.createElement("div");
            messageBox.className = "message";

            const role = document.createElement("strong");
            role.textContent = message.role.toUpperCase();

            const text = document.createElement("p");
            text.textContent = message.content;

            const metadata = document.createElement("small");
            metadata.textContent =
                `Words: ${message.word_count} | ` +
                `Tokens: ${message.estimated_tokens} | ` +
                `Characters: ${message.character_count} | ` +
                `Code: ${message.has_code}`;

            messageBox.appendChild(role);
            messageBox.appendChild(text);
            messageBox.appendChild(metadata);

            conversationBox.appendChild(messageBox);
        });

    } catch (error) {
        console.error(error);
        status.textContent = "Backend connection failed.";
    }
});
