from flask import render_template, redirect, Blueprint, url_for, request, flash, jsonify, current_app
from recipe.models import User
from recipe import bcrypt, db
from flask_login import login_user, logout_user, current_user, login_required
import re
from langchain_cohere import ChatCohere
import os
from utils.lang_tools import search_recipes, search_ingredient_substitutes, conversation
from utils.fetch_api import fetch_recipes, fetch_substitutes
from utils.get_details import get_recipe_details
from utils.conversation import get_ai_response
from utils.transcribe_audio import transcribe_audio, load_whisper_model
from pydub import AudioSegment
import io
import tempfile

recipe = Blueprint('recipe', __name__, url_prefix="/")

cohere_key = os.getenv("COHERE_API_KEY")

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9_]+@gmail\.com$'


# Ensure upload folder exists
UPLOAD_FOLDER = 'recordings'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@recipe.route('/')
@login_required
def index():
    return render_template('login.html')

@recipe.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate missing fields
        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for('recipe.signup'))
        
        # Validate the email
        if not re.match(EMAIL_REGEX, email):
            flash("Please enter a valid Gmail address.")
            return redirect(url_for('recipe.signup'))

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User with this email already exists.")
            return redirect(url_for('recipe.signup'))
        
        # Generate password hash
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create the new user
        user = User(
            username=username,
            email=email,
            password=password_hash
        )

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Redirect to login page
        return redirect(url_for('recipe.login'))


@recipe.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash("Successfully logged in")

            login_user(user)
            return redirect(url_for('recipe.chatbot'))
        else:
            flash('Incorrect Email or Password', 'danger')
            return redirect(url_for('recipe.login'))
        
@recipe.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('recipe.login'))
        

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
#         tools = [search_recipes, search_ingredient_substitutes, conversation]
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
#             # substitutes_list = "\n".join(substitutes_list)
#             # print(message + substitutes_list)
#             response_data = {"type": "substitutes", "message": message, "substitutes": substitutes_list}

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
#         elif tool_name == "conversation":
#             response = get_ai_response(query)
#             response_data = {"type": "conversation", "conversation": response}

#         else:
#             print("Invalid tool call")
#             response_data = {"type": "error", "message": "Invalid tool call"}

#         # Send the response back to the frontend
#         return jsonify(response_data)

@recipe.route('/get_user', methods=['GET'])
@login_required  # Ensure the user is logged in
def get_user():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username}), 200
    return jsonify({"error": "User not logged in"}), 401

@recipe.route("/chatbot", methods=["GET", "POST"])
@login_required
def chatbot():
    if request.method == "GET":
        return render_template('chatbot.html')
    elif request.method == "POST":
        data = request.get_json()
        query = data.get('query')
        print(query)

        if not cohere_key:
            raise ValueError("COHERE_API_KEY is missing. Please add it to your .env file.")
        os.environ["COHERE_API_KEY"] = cohere_key

        # Initialize Cohere chat model
        llm = ChatCohere(model="command-r-plus-04-2024")

        # Define tools
        tools = [search_recipes, search_ingredient_substitutes, conversation]
        llm_with_tools = llm.bind_tools(tools)

        # Invoke tools and handle tool calls
        parameters = llm_with_tools.invoke(query).tool_calls

        # Execute the appropriate tool based on the response
        tool_name = parameters[0].get('name', None)
        tool_args = parameters[0].get('args', {})

        if tool_name == "search_ingredient_substitutes":
            result = fetch_substitutes(tool_args)
            substitutes_list = result['substitutes']
            message = result['message']
            # substitutes_list = "\n".join(substitutes_list)
            # print(message + substitutes_list)
            response_data = {"type": "substitutes", "message": message, "substitutes": substitutes_list}

        elif tool_name == "search_recipes":
            recipes = fetch_recipes(tool_args)

            if "error" in recipes:
                print(f"Error fetching recipes: {recipes['error']}")
                response_data = {"type": "error", "message": recipes['error']}
            else:
                recipe_details = []
                for recipe in recipes.get('results', []):
                    title = recipe.get('title', 'No title')
                    source_url = recipe.get('sourceUrl', 'No URL')
                    image = recipe.get('image', 'No image available')
                    
                    # Get detailed recipe information
                    details = get_recipe_details(source_url)
                    
                    # Append all information for the current recipe
                    recipe_details.append({
                        "title": title,
                        "image": image,
                        "details": details,
                    })

                # Format the response for the frontend
                response_data = {"type": "recipes", "recipes": recipe_details}
        elif tool_name == "conversation":
            response = get_ai_response(query)
            response_data = {"type": "conversation", "conversation": response}

        else:
            print("Invalid tool call")
            response_data = {"type": "error", "message": "Invalid tool call"}

        # Send the response back to the frontend
        return jsonify(response_data)
    


@recipe.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the WebM audio data
        webm_data = io.BytesIO(audio_file.read())
        
        # Create a temporary directory to store the converted files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save WebM file temporarily
            webm_path = os.path.join(temp_dir, 'temp.webm')
            with open(webm_path, 'wb') as f:
                f.write(webm_data.getvalue())
            
            # Convert WebM to WAV using pydub
            audio = AudioSegment.from_file(webm_path, format="webm")
            wav_path = os.path.join(temp_dir, 'converted.wav')
            audio.export(wav_path, format="wav")
            
            # Load Whisper model
            processor, model = load_whisper_model()
            
            # Transcribe the converted WAV file
            transcription = transcribe_audio(wav_path, processor, model)
            print("Transcription:", transcription)
            
            return jsonify({
                "message": "Audio transcribed successfully",
                "transcription": transcription
            }), 200
    except Exception as e:
        print("Error during processing:", str(e))
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
