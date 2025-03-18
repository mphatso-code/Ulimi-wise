/**
 * Ulimi Wise - Community Chat JavaScript
 * Handles chat room interactions, messaging, and user management
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatRoomItems = document.querySelectorAll('.chat-room-item');
    const startChatBtns = document.querySelectorAll('.start-chat-btn');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatInfoBtn = document.getElementById('chatInfoBtn');
    const noChatSelected = document.getElementById('noChatSelected');
    const activeChatArea = document.getElementById('activeChatArea');
    const chatMessagesContainer = document.getElementById('chatMessagesContainer');
    const chatMessageForm = document.getElementById('chatMessageForm');
    const chatMessageInput = document.getElementById('chatMessageInput');
    const newChatForm = document.getElementById('newChatForm');
    const createChatBtn = document.getElementById('createChatBtn');
    const isGroupChat = document.getElementById('isGroupChat');
    const topicField = document.getElementById('topicField');
    const participantsField = document.getElementById('participantsField');
    
    // Current active chat room
    let currentRoomId = null;
    
    // Initialize toasts
    initToasts();
    
    // Initialize room selection
    initRoomSelection();
    
    // Initialize chat form
    initChatForm();
    
    // Initialize new chat modal
    initNewChatModal();
    
    /**
     * Initialize toast messages
     */
    function initToasts() {
        const toastElements = document.querySelectorAll('.toast');
        toastElements.forEach(toastEl => {
            const toast = new bootstrap.Toast(toastEl, {
                autohide: true,
                delay: 3000
            });
            toast.show();
        });
    }
    
    /**
     * Initialize chat room selection
     */
    function initRoomSelection() {
        // Handle selecting a chat room
        chatRoomItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const roomId = this.dataset.roomId;
                loadChatRoom(roomId);
                
                // Mark this room as active
                chatRoomItems.forEach(room => room.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Handle starting a new private chat
        startChatBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const userId = this.dataset.userId;
                const userName = this.dataset.userName;
                
                // Start a private chat with this user
                fetch('/community-chat/start-private-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `user_id=${userId}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        loadChatRoom(data.room_id);
                        
                        // If it's a new chat room, we might want to reload the chat list
                        if (!data.exists) {
                            // In a real application, you'd update the UI here
                            // For now, we'll just reload
                            setTimeout(() => window.location.reload(), 500);
                        }
                    }
                })
                .catch(error => {
                    console.error('Error starting chat:', error);
                    showNotification('Failed to start chat', 'danger');
                });
            });
        });
        
        // Handle closing the active chat
        if (closeChatBtn) {
            closeChatBtn.addEventListener('click', function() {
                noChatSelected.classList.remove('d-none');
                activeChatArea.classList.add('d-none');
                currentRoomId = null;
                
                // Remove active class from all rooms
                chatRoomItems.forEach(room => room.classList.remove('active'));
            });
        }
        
        // Handle showing chat info
        if (chatInfoBtn) {
            chatInfoBtn.addEventListener('click', function() {
                if (currentRoomId) {
                    showChatInfo(currentRoomId);
                }
            });
        }
    }
    
    /**
     * Initialize chat message form
     */
    function initChatForm() {
        if (chatMessageForm) {
            chatMessageForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                if (!currentRoomId) return;
                
                const message = chatMessageInput.value.trim();
                if (!message) return;
                
                // Send message to the server
                fetch(`/community-chat/rooms/${currentRoomId}/messages`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message=${encodeURIComponent(message)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Add the message to the UI
                        appendMessage(data.message);
                        chatMessageInput.value = '';
                    }
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    showNotification('Failed to send message', 'danger');
                });
            });
        }
    }
    
    /**
     * Initialize new chat modal
     */
    function initNewChatModal() {
        // Toggle group chat fields
        if (isGroupChat) {
            isGroupChat.addEventListener('change', function() {
                if (this.checked) {
                    topicField.classList.remove('d-none');
                    participantsField.classList.remove('d-none');
                    // Load potential participants
                    loadParticipants();
                } else {
                    topicField.classList.add('d-none');
                    participantsField.classList.add('d-none');
                }
            });
        }
        
        // Handle select all participants checkbox
        const selectAllCheckbox = document.querySelector('.select-all-participants');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('.participant-checkbox');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = this.checked;
                });
            });
        }
        
        // Handle creating a new chat
        if (createChatBtn) {
            createChatBtn.addEventListener('click', function() {
                const name = document.getElementById('chatName').value.trim();
                const description = document.getElementById('chatDescription').value.trim();
                const topic = document.getElementById('chatTopic').value.trim();
                const isGroup = isGroupChat.checked;
                
                if (!name) {
                    showNotification('Chat name is required', 'warning');
                    return;
                }
                
                // For group chats, ensure at least one participant is selected
                let participantIds = [];
                if (isGroup) {
                    const checkboxes = document.querySelectorAll('.participant-checkbox:checked');
                    checkboxes.forEach(cb => {
                        participantIds.push(cb.value);
                    });
                    
                    if (participantIds.length === 0) {
                        showNotification('Select at least one participant', 'warning');
                        return;
                    }
                }
                
                // Create form data for the request
                const formData = new FormData();
                formData.append('name', name);
                formData.append('description', description);
                formData.append('is_group', isGroup.toString());
                if (topic) formData.append('topic', topic);
                participantIds.forEach(id => {
                    formData.append('participants[]', id);
                });
                
                // Send request to create the chat
                fetch('/community-chat/rooms', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Close the modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('newChatModal'));
                        modal.hide();
                        
                        // Load the new chat room
                        loadChatRoom(data.room.id);
                        
                        // In a real application, you'd update the UI here
                        // For now, we'll just reload
                        setTimeout(() => window.location.reload(), 500);
                    }
                })
                .catch(error => {
                    console.error('Error creating chat:', error);
                    showNotification('Failed to create chat', 'danger');
                });
            });
        }
    }
    
    /**
     * Load a chat room and its messages
     * @param {number} roomId - The ID of the chat room
     */
    function loadChatRoom(roomId) {
        fetch(`/community-chat/rooms/${roomId}/messages`)
            .then(response => response.json())
            .then(data => {
                // Set current room ID
                currentRoomId = roomId;
                
                // Show active chat area
                noChatSelected.classList.add('d-none');
                activeChatArea.classList.remove('d-none');
                
                // Set room name and participants
                document.getElementById('chatRoomName').textContent = data.room.name;
                
                // Set room icon
                const roomIcon = document.getElementById('chatRoomIcon');
                if (data.room.is_group) {
                    roomIcon.className = 'bi bi-people-fill fs-3';
                } else {
                    roomIcon.className = 'bi bi-person-circle fs-3';
                }
                
                // Set participants text
                const participantsEl = document.getElementById('chatRoomParticipants');
                if (data.room.is_group) {
                    participantsEl.textContent = `${data.room.participants.length} participants`;
                } else {
                    // For private chats, we would show the other person's name
                    const otherParticipants = data.room.participants.filter(p => p.id !== currentUserId);
                    if (otherParticipants.length > 0) {
                        participantsEl.textContent = otherParticipants[0].username;
                    } else {
                        participantsEl.textContent = '';
                    }
                }
                
                // Load messages
                loadMessages(data.messages);
            })
            .catch(error => {
                console.error('Error loading chat room:', error);
                showNotification('Failed to load chat', 'danger');
            });
    }
    
    /**
     * Load and display messages
     * @param {Array} messages - Array of message objects
     */
    function loadMessages(messages) {
        chatMessagesContainer.innerHTML = '';
        
        if (messages.length === 0) {
            chatMessagesContainer.innerHTML = `
                <div class="text-center p-4 text-muted">
                    <i class="bi bi-chat-dots fs-1"></i>
                    <p>No messages yet. Start the conversation!</p>
                </div>
            `;
            return;
        }
        
        messages.forEach(message => {
            appendMessage(message);
        });
        
        // Scroll to bottom
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
    
    /**
     * Append a message to the chat
     * @param {Object} message - Message object
     */
    function appendMessage(message) {
        const isOutgoing = message.is_mine;
        const messageEl = document.createElement('div');
        messageEl.className = `community-message ${isOutgoing ? 'outgoing' : 'incoming'}`;
        
        const messageContent = `
            <div class="community-message-bubble ${isOutgoing ? 'message-outgoing' : 'message-incoming'}">
                ${!isOutgoing ? `<div class="message-sender">${message.sender_name}</div>` : ''}
                <div class="message-text">${message.message}</div>
                <div class="message-time text-end">${message.created_at}</div>
            </div>
        `;
        
        messageEl.innerHTML = messageContent;
        chatMessagesContainer.appendChild(messageEl);
        
        // Scroll to bottom
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
    
    /**
     * Load potential participants for a group chat
     */
    function loadParticipants() {
        const participantsList = document.getElementById('participantsList');
        if (!participantsList) return;
        
        participantsList.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm" role="status"></div> Loading...</div>';
        
        // Fetch from API (for now, we'll emulate this)
        Promise.all([
            fetch('/users/extension-officers').then(res => res.json()),
            fetch('/users/buyers').then(res => res.json())
        ])
        .then(([officersData, buyersData]) => {
            const participants = [];
            
            if (officersData.officers) {
                officersData.officers.forEach(officer => {
                    participants.push({
                        id: officer.id,
                        name: officer.username,
                        type: "Extension Officer"
                    });
                });
            }
            
            if (buyersData.buyers) {
                buyersData.buyers.forEach(buyer => {
                    participants.push({
                        id: buyer.id,
                        name: buyer.username,
                        type: "Buyer"
                    });
                });
            }
            
            // Update the UI
            participantsList.innerHTML = '';
            
            if (participants.length === 0) {
                participantsList.innerHTML = '<div class="text-center p-3">No users available</div>';
                return;
            }
            
            participants.forEach(participant => {
                const item = document.createElement('div');
                item.className = 'form-check mb-2';
                item.innerHTML = `
                    <input class="form-check-input participant-checkbox" type="checkbox" value="${participant.id}" id="participant-${participant.id}">
                    <label class="form-check-label" for="participant-${participant.id}">
                        ${participant.name} <small class="text-muted">(${participant.type})</small>
                    </label>
                `;
                participantsList.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error loading participants:', error);
            participantsList.innerHTML = '<div class="text-center p-3 text-danger">Failed to load participants</div>';
        });
    }
    
    /**
     * Show chat information
     * @param {number} roomId - The ID of the chat room
     */
    function showChatInfo(roomId) {
        fetch(`/community-chat/rooms/${roomId}/messages`)
            .then(response => response.json())
            .then(data => {
                // Set modal content
                document.getElementById('infoRoomName').textContent = data.room.name;
                
                // Set topic if available
                const topicContainer = document.getElementById('infoTopicContainer');
                const topicText = document.getElementById('infoRoomTopic');
                if (data.room.topic) {
                    topicText.textContent = data.room.topic;
                    topicContainer.classList.remove('d-none');
                } else {
                    topicContainer.classList.add('d-none');
                }
                
                // Set description if available
                const descContainer = document.getElementById('infoDescriptionContainer');
                const descText = document.getElementById('infoRoomDescription');
                // Here we would use the room description if available
                // For now, just hide it
                descContainer.classList.add('d-none');
                
                // Set participants list
                const participantsList = document.getElementById('infoParticipantsList');
                participantsList.innerHTML = '';
                data.room.participants.forEach(participant => {
                    const item = document.createElement('div');
                    item.className = 'list-group-item d-flex align-items-center';
                    item.innerHTML = `
                        <i class="bi bi-person-circle me-2"></i>
                        <span>${participant.username} ${participant.id == currentUserId ? '(You)' : ''}</span>
                    `;
                    participantsList.appendChild(item);
                });
                
                // Set created at date
                // Here we would use the room creation date if available
                document.getElementById('infoCreatedAt').textContent = 'Recently'; 
                
                // Show the modal
                const modal = new bootstrap.Modal(document.getElementById('chatInfoModal'));
                modal.show();
            })
            .catch(error => {
                console.error('Error loading chat info:', error);
                showNotification('Failed to load chat information', 'danger');
            });
    }
    
    /**
     * Show a notification toast
     * @param {string} message - The message to display
     * @param {string} type - The type of toast (success, danger, warning)
     */
    function showNotification(message, type = 'success') {
        // Create toast element
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add to toast container
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        toastContainer.appendChild(toastEl);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 3000
        });
        toast.show();
        
        // Remove toast from DOM after it's hidden
        toastEl.addEventListener('hidden.bs.toast', function() {
            toastEl.remove();
        });
    }
});

// Global variable with current user ID (to be set in the template)
var currentUserId = null;