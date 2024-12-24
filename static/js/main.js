const chatList = document.querySelector('.chat-list');
const conversationArea = document.querySelector('.conversation-area');
const userQuery = document.getElementById('userQuery');
const sendButton = document.getElementById('sendButton');
const newChatButton = document.querySelector('.new-chat-button');

let currentChatId = 0;
const chats = [];

// Function to add a new chat to the left panel
function addNewChat() {
  const chatItem = document.createElement('div');
  chatItem.classList.add('chat-item');
  chatItem.textContent = `Chat ${chats.length + 1}`;
  chatItem.dataset.chatId = chats.length;
  chatItem.addEventListener('click', () => {
    switchChat(chatItem.dataset.chatId);
  });
  chatList.appendChild(chatItem);
  chats.push([]);
  switchChat(chats.length - 1);
}

// Function to switch to a different chat
function switchChat(chatId) {
  currentChatId = parseInt(chatId);
  updateChatUI();
}

// Function to add a message to the conversation area
function addMessage(message, isBot, isImage = false) {
  const messageElement = document.createElement('div');
  messageElement.classList.add(isBot ? 'bot-message' : 'user-message');
  
  if (isImage) {
    const img = document.createElement('img');
    img.src = message;
    img.alt = "Image";
    img.classList.add('message-image');
    messageElement.appendChild(img);
  } else {
    // Check if the message contains HTML (recipe.details)
    if (message.includes("<html>")) {
      // Use innerHTML to parse and render the HTML content
      messageElement.innerHTML = message;
    } else {
      const text = document.createElement('p');
      text.textContent = message;
      messageElement.appendChild(text);
    }
  }
  
  conversationArea.appendChild(messageElement);
  conversationArea.scrollTop = conversationArea.scrollHeight;
  
  chats[currentChatId].push({ message, isBot, isImage });
}



// Function to update the chat UI
function updateChatUI() {
  conversationArea.innerHTML = '';
  chats[currentChatId].forEach(({ message, isBot }) => {
    addMessage(message, isBot);
  });
}

//// Event listener for the send button
sendButton.addEventListener('click', () => {
  const query = userQuery.value.trim();
  if (query) {
    addMessage(query, false); // Add the user's message to the chat UI

    // Send the query to the backend
    fetch('/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Response from backend:', data);

        if (data.type === "substitutes") {
          // If the response type is "substitutes"
          const botMessage = data.message + "\n" + data.substitutes.join("\n");
          addMessage(botMessage, true);
        } 
        else if (data.type === "recipes") {
          data.recipes.forEach(recipe => {
            addMessage(`Title: ${recipe.title}`, true);
            addMessage(recipe.image, true, true); // Display image
            addMessage(recipe.details, true); // Render HTML content for recipe details
          });
        }
        else if (data.type === "conversation") {
          // If the response type is "conversation"
          const botMessage = data.conversation;
          addMessage(botMessage, true);
        }
        else if (data.type === "error") {
          // If there is an error
          addMessage('Oops! Something went wrong: ' + data.message, true);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        addMessage('Oops! Something went wrong. Please try again.', true);
      });

    userQuery.value = ''; // Clear the input field
  }
});


// Event listener for the new chat button
newChatButton.addEventListener('click', addNewChat);

// Initialize the first chat
addNewChat();




// // Another one
// document.getElementById("checkbox").addEventListener("change", async (event) => {
//   if (event.target.checked) {
//       // Start recording (same as before)
//       const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//       const mediaRecorder = new MediaRecorder(stream);
//       const audioChunks = [];

//       mediaRecorder.start();

//       mediaRecorder.ondataavailable = (event) => {
//           audioChunks.push(event.data);
//       };

//       mediaRecorder.onstop = () => {
//           const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
//           const formData = new FormData();
//           formData.append("audio", audioBlob, "recording.wav");

//           // Send audio to the Flask server
//           fetch("/upload_audio", {
//               method: "POST",
//               body: formData
//           })
//               .then(response => response.json())
//               .then(data => {
//                   console.log("Audio saved:", data);

//                   if (data.transcription) {
//                       // Update the text input with the transcription
//                       document.getElementById("userQuery").value = data.transcription;
//                   } else {
//                       console.error("No transcription available.");
//                   }
//               })
//               .catch(error => console.error("Error uploading audio:", error));
//       };

//       document.getElementById("checkbox").addEventListener("change", () => {
//           mediaRecorder.stop();
//       });
//   }
// });

// Get DOM elements
const micCheckbox = document.getElementById('checkbox');
let mediaRecorder = null;
let audioChunks = [];

// Initialize media recorder if browser supports it
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = function(e) {
                audioChunks.push(e.data);
            };

            mediaRecorder.onstop = function() {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                audioChunks = [];

                const formData = new FormData();
                formData.append('audio', audioBlob);

                // Show loading state in textarea
                userQuery.value = 'Transcribing...';
                userQuery.disabled = true;

                fetch('/upload_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.transcription) {
                        userQuery.value = data.transcription;
                    } else {
                        userQuery.value = 'Error transcribing audio';
                    }
                    userQuery.disabled = false;
                })
                .catch(error => {
                    console.error('Error:', error);
                    userQuery.value = 'Error transcribing audio';
                    userQuery.disabled = false;
                });
            };
        })
        .catch(function(err) {
            console.error('Error accessing microphone:', err);
            micCheckbox.disabled = true;
        });
} else {
    console.error('getUserMedia not supported');
    micCheckbox.disabled = true;
}

// Handle microphone button clicks
micCheckbox.addEventListener('change', function() {
    if (this.checked) {
        // Start recording
        audioChunks = [];
        mediaRecorder.start();
        userQuery.placeholder = 'Recording...';
    } else {
        // Stop recording
        mediaRecorder.stop();
        userQuery.placeholder = 'Type your message...';
    }
});

// Handle send button clicks
document.getElementById('sendButton').addEventListener('click', function() {
    // If recording is ongoing, stop it first
    if (micCheckbox.checked) {
        micCheckbox.checked = false;
        mediaRecorder.stop();
    }
    // Continue with your existing send logic here
});

document.addEventListener('DOMContentLoaded', async () => {
  try {
      const response = await fetch('/get_user');
      if (response.ok) {
          const data = await response.json();
          const userNameElement = document.getElementById('user-name');
          userNameElement.textContent = data.username; // Set the username
      } else {
          console.error("User not logged in or session expired.");
          document.getElementById('user-name').textContent = "Guest";
      }
  } catch (error) {
      console.error("Error fetching user data:", error);
      document.getElementById('user-name').textContent = "Guest";
  }
});



