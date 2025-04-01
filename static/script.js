/* Muse Summoner Web Application JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const conversation = document.getElementById('conversation');
    const activeMuse = document.getElementById('active-muse');
    const statusBadge = document.getElementById('status-badge');
    const museList = document.getElementById('muse-list');
    const creationPanel = document.getElementById('creation-panel');
    const creationPrompt = document.getElementById('creation-prompt');
    const creationInput = document.getElementById('creation-input');
    const creationSubmit = document.getElementById('creation-submit');
    const creationCancel = document.getElementById('creation-cancel');

    // State variables
    let isCreatingMuse = false;
    let currentMuseName = 'System';

    // Initialize the application
    init();

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    creationSubmit.addEventListener('click', submitCreationInput);
    creationInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitCreationInput();
        }
    });

    creationCancel.addEventListener('click', cancelCreation);

    // Functions
    function init() {
        // Load available muses
        fetchMuses();
        
        // Focus on input field
        userInput.focus();
    }

    function fetchMuses() {
        fetch('/api/get_muses')
            .then(response => response.json())
            .then(data => {
                displayMuses(data.muses);
            })
            .catch(error => {
                console.error('Error fetching muses:', error);
                addSystemMessage('Error loading muses. Please try again later.');
            });
    }

    function displayMuses(muses) {
        museList.innerHTML = '';
        
        if (muses.length === 0) {
            museList.innerHTML = '<p class="text-muted">No muses available.</p>';
            return;
        }

        const list = document.createElement('ul');
        list.className = 'list-group list-group-flush';
        
        muses.forEach(muse => {
            const item = document.createElement('li');
            item.className = 'list-group-item muse-item';
            item.innerHTML = `
                <div><strong>${muse.name}</strong></div>
                <div class="muse-trigger">"${muse.trigger_phrase}"</div>
                <small class="text-muted">${muse.purpose}</small>
            `;
            item.addEventListener('click', function() {
                userInput.value = muse.trigger_phrase;
                userInput.focus();
            });
            list.appendChild(item);
        });
        
        museList.appendChild(list);
    }

    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') {
            return;
        }

        // Check if we're creating a muse
        if (isCreatingMuse) {
            processCreationInput(message);
            return;
        }

        // Check if this is a command to create a new muse
        if (message.toLowerCase() === 'create a new muse') {
            startMuseCreation();
            return;
        }

        // Add user message to conversation
        addUserMessage(message);
        
        // Clear input field
        userInput.value = '';
        
        // Update status
        statusBadge.textContent = 'Processing...';
        statusBadge.className = 'badge bg-warning';
        
        // Send message to server
        fetch('/api/process_input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Add response to conversation
            if (data.muse_name && data.muse_name !== 'System') {
                addMuseMessage(data.response, data.muse_name);
                currentMuseName = data.muse_name;
                activeMuse.textContent = data.muse_name;
                statusBadge.textContent = 'Active';
                statusBadge.className = 'badge bg-success';
            } else {
                addSystemMessage(data.response);
                currentMuseName = 'System';
                activeMuse.textContent = 'Muse Summoner System';
                statusBadge.textContent = 'Idle';
                statusBadge.className = 'badge bg-secondary';
            }
            
            // Scroll to bottom of conversation
            conversation.scrollTop = conversation.scrollHeight;
            
            // Focus on input field
            userInput.focus();
        })
        .catch(error => {
            console.error('Error:', error);
            addSystemMessage('Error processing your message. Please try again.');
            statusBadge.textContent = 'Error';
            statusBadge.className = 'badge bg-danger';
        });
    }

    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${formatMessage(message)}</p>
            </div>
        `;
        conversation.appendChild(messageDiv);
        conversation.scrollTop = conversation.scrollHeight;
    }

    function addMuseMessage(message, museName) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message muse';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${formatMessage(message)}</p>
            </div>
        `;
        conversation.appendChild(messageDiv);
        conversation.scrollTop = conversation.scrollHeight;
    }

    function addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system';
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${formatMessage(message)}</p>
            </div>
        `;
        conversation.appendChild(messageDiv);
        conversation.scrollTop = conversation.scrollHeight;
    }

    function formatMessage(message) {
        // Convert line breaks to <br> tags
        let formatted = message.replace(/\n/g, '<br>');
        
        // Convert bullet points to HTML lists
        if (formatted.includes('- ')) {
            const lines = formatted.split('<br>');
            let inList = false;
            let result = '';
            
            for (const line of lines) {
                if (line.trim().startsWith('- ')) {
                    if (!inList) {
                        result += '<ul>';
                        inList = true;
                    }
                    result += `<li>${line.trim().substring(2)}</li>`;
                } else {
                    if (inList) {
                        result += '</ul>';
                        inList = false;
                    }
                    result += line + '<br>';
                }
            }
            
            if (inList) {
                result += '</ul>';
            }
            
            formatted = result;
        }
        
        return formatted;
    }

    function startMuseCreation() {
        // Add user message to conversation
        addUserMessage('Create a new muse');
        
        // Clear input field
        userInput.value = '';
        
        // Show creation panel
        creationPanel.style.display = 'block';
        
        // Update status
        statusBadge.textContent = 'Creating Muse';
        statusBadge.className = 'badge bg-info';
        
        // Send request to start creation process
        fetch('/api/create_muse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: 'start' }),
        })
        .then(response => response.json())
        .then(data => {
            creationPrompt.innerHTML = data.prompt;
            isCreatingMuse = data.creating;
            creationInput.focus();
        })
        .catch(error => {
            console.error('Error:', error);
            addSystemMessage('Error starting muse creation. Please try again.');
            creationPanel.style.display = 'none';
            statusBadge.textContent = 'Error';
            statusBadge.className = 'badge bg-danger';
        });
    }

    function processCreationInput(input) {
        // Send creation input to server
        fetch('/api/create_muse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: input }),
        })
        .then(response => response.json())
        .then(data => {
            creationPrompt.innerHTML = data.prompt;
            isCreatingMuse = data.creating;
            
            // Clear input field
            creationInput.value = '';
            
            // If creation is complete, hide panel and update conversation
            if (!data.creating) {
                addSystemMessage(data.prompt);
                creationPanel.style.display = 'none';
                statusBadge.textContent = 'Idle';
                statusBadge.className = 'badge bg-secondary';
                
                // Refresh muse list
                fetchMuses();
            }
            
            creationInput.focus();
        })
        .catch(error => {
            console.error('Error:', error);
            addSystemMessage('Error processing muse creation. Please try again.');
            isCreatingMuse = false;
            creationPanel.style.display = 'none';
            statusBadge.textContent = 'Error';
            statusBadge.className = 'badge bg-danger';
        });
    }

    function submitCreationInput() {
        const input = creationInput.value.trim();
        
        if (input === '') {
            return;
        }
        
        processCreationInput(input);
    }

    function cancelCreation() {
        isCreatingMuse = false;
        creationPanel.style.display = 'none';
        addSystemMessage('Muse creation cancelled.');
        statusBadge.textContent = 'Idle';
        statusBadge.className = 'badge bg-secondary';
        userInput.focus();
    }
});
