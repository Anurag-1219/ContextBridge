function extractConversation() {
    const messages = [];

    const elements = document.querySelectorAll('[data-message-author-role]');

    elements.forEach((element) => {
        const role = element.getAttribute('data-message-author-role');
        const text = element.innerText.trim();

        if (text) {
            messages.push({
                role: role,
                content: text
            });
        }
    });

    return messages;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractConversation") {
        const conversation = extractConversation();

        sendResponse({
            success: true,
            messages: conversation
        });
    }

    return true;
});
