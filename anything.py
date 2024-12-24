# <div class="container">
#   <div class="left-panel">
#     <div class="chat-history">
#       <h3>Chat History</h3>
#       <div class="chat-list">
#         <!-- Chat history items will be added dynamically -->
#       </div>
#     </div>
#     <button class="new-chat-button">New Chat</button>
#   </div>
#   <div class="main-content">
#     <div class="chatbot-header">
#       <div class="chatbot-name">Claude</div>
#       <div class="user-profile">
#         <img src="user-avatar.jpg" alt="User Avatar">
#         <span class="user-name">John Doe</span>
#       </div>
#     </div>
#     <div class="conversation-area">
#       <!-- Chat messages between user and bot will be added dynamically -->
#     </div>
#     <div class="user-input">
#       <textarea placeholder="Type your message..." rows="2"></textarea>
#       <button class="send-button">Send</button>
#     </div>
#   </div>
# </div>


# .container {
#   display: flex;
#   height: 100vh;
# }

# .left-panel {
#   width: 300px;
#   background-color: #f5f5f5;
#   padding: 20px;
#   display: flex;
#   flex-direction: column;
# }

# .chat-history {
#   flex-grow: 1;
#   overflow-y: auto;
# }

# .chat-history h3 {
#   font-size: 18px;
#   margin-bottom: 10px;
# }

# .chat-list .chat-item {
#   display: flex;
#   justify-content: space-between;
#   align-items: center;
#   padding: 10px;
#   border-radius: 5px;
#   cursor: pointer;
#   transition: background-color 0.3s;
# }

# .chat-list .chat-item:hover {
#   background-color: #e6e6e6;
# }

# .chat-list .chat-item.active {
#   background-color: #d9d9d9;
#   font-weight: bold;
# }

# .new-chat-button {
#   background-color: #4CAF50;
#   color: white;
#   padding: 10px 16px;
#   border: none;
#   border-radius: 5px;
#   cursor: pointer;
#   margin-top: 10px;
# }

# .main-content {
#   flex-grow: 1;
#   padding: 20px;
#   display: flex;
#   flex-direction: column;
# }

# .chatbot-header {
#   display: flex;
#   justify-content: space-between;
#   align-items: center;
#   margin-bottom: 20px;
# }

# .chatbot-name {
#   font-size: 24px;
#   font-weight: bold;
# }

# .user-profile {
#   display: flex;
#   align-items: center;
# }

# .user-profile img {
#   width: 40px;
#   height: 40px;
#   border-radius: 50%;
#   margin-right: 10px;
# }

# .conversation-area {
#   flex-grow: 1;
#   background-color: #f5f5f5;
#   padding: 20px;
#   border-radius: 5px;
#   overflow-y: auto;
# }

# .user-message,
# .bot-message {
#   margin-bottom: 10px;
#   padding: 10px;
#   border-radius: 5px;
# }

# .user-message {
#   background-color: #d9f1d9;
#   align-self: flex-end;
# }

# .bot-message {
#   background-color: #e6e6e6;
#   align-self: flex-start;
# }

# .user-input {
#   display: flex;
#   align-items: center;
#   margin-top: 20px;
# }

# .user-input textarea {
#   flex-grow: 1;
#   padding: 10px;
#   border: 1px solid #ccc;
#   border-radius: 5px;
#   resize: none;
# }

# .user-input .send-button {
#   background-color: #4CAF50;
#   color: white;
#   padding: 10px 16px;
#   border: none;
#   border-radius: 5px;
#   cursor: pointer;
#   margin-left: 10px;
# }


# const chatList = document.querySelector('.chat-list');
# const conversationArea = document.querySelector('.conversation-area');
# const userInput = document.querySelector('.user-input textarea');
# const sendButton = document.querySelector('.user-input .send-button');
# const newChatButton = document.querySelector('.new-chat-button');

# let currentChatId = 0;
# const chats = [];

# // Function to add a new chat to the left panel
# function addNewChat() {
#   const chatItem = document.createElement('div');
#   chatItem.classList.add('chat-item');
#   chatItem.textContent = `Chat ${chats.length + 1}`;
#   chatItem.dataset.chatId = chats.length;
#   chatItem.addEventListener('click', () => {
#     switchChat(chatItem.dataset.chatId);
#   });
#   chatList.appendChild(chatItem);
#   chats.push([]);
#   switchChat(chats.length - 1);
# }

# // Function to switch to a different chat
# function switchChat(chatId) {
#   currentChatId = parseInt(chatId);
#   updateChatUI();
# }

# // Function to add a message to the conversation area
# function addMessage(message, isBot) {
#   const messageElement = document.createElement('div');
#   messageElement.classList.add(isBot ? 'bot-message' : 'user-message');
#   messageElement.textContent = message;
#   conversationArea.appendChild(messageElement);
#   conversationArea.scrollTop = conversationArea.scrollHeight;
#   chats[currentChatId].push({ message, isBot });
# }

# // Function to update the chat UI
# function updateChatUI() {
#   conversationArea.innerHTML = '';
#   chats[currentChatId].forEach(({ message, isBot }) => {
#     addMessage(message, isBot);
#   });
# }

# // Event listener for the send button
# sendButton.addEventListener('click', () => {
#   const userMessage = userInput.value.trim();
#   if (userMessage) {
#     addMessage(userMessage, false);
#     userInput.value = '';

#     // Simulate a bot response after a short delay
#     setTimeout(() => {
#       addMessage('This is a sample bot response.', true);
#     }, 1000);
#   }
# });

# // Event listener for the new chat button
# newChatButton.addEventListener('click', addNewChat);

# // Initialize the first chat
# addNewChat();























# @recipe.route("/chatbot", methods=["GET", "POST"])
# @login_required
# def chatbot():
#     if request.method == "GET":
#         return render_template('chatbot.html')
#     elif request.method == "POST":
#         data = request.get_json()
#         query = data.get('query')
#         print(query)

#         if not cohere_key:
#             raise ValueError("COHERE_API_KEY is missing. Please add it to your .env file.")
#         os.environ["COHERE_API_KEY"] = cohere_key

#         # Initialize Cohere chat model
#         llm = ChatCohere(model="command-r-plus-04-2024")

#         # Define tools
#         tools = [search_recipes, search_ingredient_substitutes]
#         llm_with_tools = llm.bind_tools(tools)

#         # Invoke tools and handle tool calls
#         parameters = llm_with_tools.invoke(query).tool_calls

#         # Execute the appropriate tool based on the response
#         tool_name = parameters[0].get('name', None)
#         tool_args = parameters[0].get('args', {})

#         if tool_name == "search_ingredient_substitutes":
#             result = fetch_substitutes(tool_args)
#             substitutes_list = result['substitutes']
#             message = result['message']
#             bot_response = message + "\n" + "\n".join(substitutes_list)
#             print(bot_response)
#             response_data = {"type": "substitutes", "message": bot_response}

#         elif tool_name == "search_recipes":
#             recipes = fetch_recipes(tool_args)

#             if "error" in recipes:
#                 print(f"Error fetching recipes: {recipes['error']}")
#                 response_data = {"type": "error", "message": recipes['error']}
#             else:
#                 recipe_details = []
#                 for recipe in recipes.get('results', []):
#                     title = recipe.get('title', 'No title')
#                     source_url = recipe.get('sourceUrl', 'No URL')
#                     image = recipe.get('image', 'No image available')
                    
#                     # Get detailed recipe information
#                     details = get_recipe_details(source_url)
                    
#                     # Append all information for the current recipe
#                     recipe_details.append({
#                         "title": title,
#                         "image": image,
#                         "details": details,
#                     })

#                 # Format the response for the frontend
#                 response_data = {"type": "recipes", "recipes": recipe_details}

#         else:
#             print("Invalid tool call")
#             response_data = {"type": "error", "message": "Invalid tool call"}

#         # Send the response back to the frontend
#         return jsonify(response_data)



# const chatList = document.querySelector('.chat-list');
# const conversationArea = document.querySelector('.conversation-area');
# const userQuery = document.getElementById('userQuery');
# const sendButton = document.getElementById('sendButton');
# const newChatButton = document.querySelector('.new-chat-button');

# let currentChatId = 0;
# const chats = [];

# // Function to add a new chat to the left panel
# function addNewChat() {
#   const chatItem = document.createElement('div');
#   chatItem.classList.add('chat-item');
#   chatItem.textContent = `Chat ${chats.length + 1}`;
#   chatItem.dataset.chatId = chats.length;
#   chatItem.addEventListener('click', () => {
#     switchChat(chatItem.dataset.chatId);
#   });
#   chatList.appendChild(chatItem);
#   chats.push([]);
#   switchChat(chats.length - 1);
# }

# // Function to switch to a different chat
# function switchChat(chatId) {
#   currentChatId = parseInt(chatId);
#   updateChatUI();
# }

# // Function to add a message to the conversation area
# function addMessage(message, isBot) {
#   const messageElement = document.createElement('div');
#   messageElement.classList.add(isBot ? 'bot-message' : 'user-message');
#   messageElement.textContent = message;
#   conversationArea.appendChild(messageElement);
#   conversationArea.scrollTop = conversationArea.scrollHeight;
#   chats[currentChatId].push({ message, isBot });
# }

# // Function to update the chat UI
# function updateChatUI() {
#   conversationArea.innerHTML = '';
#   chats[currentChatId].forEach(({ message, isBot }) => {
#     addMessage(message, isBot);
#   });
# }

# //// Event listener for the send button
# sendButton.addEventListener('click', () => {
#   const query = userQuery.value.trim();
#   if (query) {
#     addMessage(query, false); // Add the user's message to the chat UI

#     // Send the query to the backend
#     fetch('/chatbot', {
#       method: 'POST',
#       headers: {
#         'Content-Type': 'application/json',
#       },
#       body: JSON.stringify({ query: query }),
#     })
#       .then((response) => response.json())
#       .then((data) => {
#         console.log('Response from backend:', data);

#         if (data.type === "substitutes") {
#           // If the response type is "substitutes"
#           const botMessage = data.message + "\n" + data.substitutes.join("\n");
#           addMessage(botMessage, true);
#         } 
#         else if (data.type === "recipes") {
#           // If the response type is "recipes"
#           let botMessage = "Here are the recipes I found:\n";
#           data.recipes.forEach(recipe => {
#             botMessage += `Title: ${recipe.title}\nImage: ${recipe.image}\nDetails: ${recipe.details}\n\n`;
#           });
#           addMessage(botMessage, true);
#         }
#         else if (data.type === "conversation") {
#           // If the response type is "conversation"
#           const botMessage = data.conversation;
#           addMessage(botMessage, true);
#         }
#         else if (data.type === "error") {
#           // If there is an error
#           addMessage('Oops! Something went wrong: ' + data.message, true);
#         }
#       })
#       .catch((error) => {
#         console.error('Error:', error);
#         addMessage('Oops! Something went wrong. Please try again.', true);
#       });

#     userQuery.value = ''; // Clear the input field
#   }
# });


# // Event listener for the new chat button
# newChatButton.addEventListener('click', addNewChat);

# // Initialize the first chat
# addNewChat();
