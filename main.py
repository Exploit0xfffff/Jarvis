import google.generativeai as palm
import csv
import os
import webbrowser
import wikipedia
import subprocess

# Set your API keys
palm_api_key = 'A*******************************A'
openai_api_key = 'sk-************************************l'
github_api_key = 'g**************************************p'
spotify_api_key = ''
# Set up API keys for services
api_keys = {
    'palm': palm_api_key,
    'openai': openai_api_key,
    'github': github_api_key
}

# Set the active service
active_service = 'palm'

# Configure API keys
if active_service in api_keys:
    palm.configure(api_key=api_keys[active_service])
else:
    print(f"Error: API key for {active_service} is missing.")
    exit()

# Initialize data file
csv_file_path = 'assistant_data.csv'
header = ["Role", "Content"]

# Create the CSV file if it doesn't exist
if not os.path.isfile(csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

# Load existing messages from the CSV file
messages = []
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    for row in reader:
        messages.append({"role": row[0], "content": row[1]})

print("Jarvis: Hi, I'm Jarvis. I'm your personalized assistant")

while True:
    user_input = input("👤: ")

    if user_input.lower() == "exit":
        break

    if user_input.lower() == "clear":
        print("\033[H\033[J")
        print("Jarvis: Hi, I'm Jarvis. I'm your personalized assistant")
        messages = []
        continue

    messages.append({"role": "user", "content": user_input})

    # Detect if the user is writing code
    if any(keyword in user_input.lower() for keyword in ["def ", "class ", "import ", "for ", "while ", "if ", "else "]):
        print("Jarvis is observing your coding activity...")

    try:
        print("Jarvis is thinking...")
        response = palm.generate_text(prompt=user_input)

        # Check for errors in the Palm API response
        if response and response.result:
            reply_palm = response.result.strip()
            messages.append({"role": "assistant", "content": reply_palm})
            print(f"🤖 (Jarvis): {reply_palm}")
        else:
            print("Error in Palm response or empty response. Please try again.")
            continue

        # Open the Canva website based on the response
        if "canva" in reply_palm.lower():
            print("Opening Canva website...")
            webbrowser.open("https://www.canva.com/")
            # Provide additional instructions for the user or automate further steps as needed
        elif "youtube" in reply_palm.lower():
            print("Opening Youtube website...")
            webbrowser.open("https://www.youtube.com/")
        elif "google" in reply_palm.lower():
            print("Opening Google website...")
            webbrowser.open("https://www.google.com/")
        elif "github" in reply_palm.lower():
            print("Opening GitHub website...")
            webbrowser.open("https://www.github.com/")
        
        elif "spotify" in reply_palm.lower():
            print("Opening Spotify application...")
            # This assumes that there is a command or URL scheme to open Spotify
            subprocess.run(["spotify"])  # Adjust this line based on your system and Spotify installation
        elif "wikipedia" in reply_palm.lower():
            # Check for Wikipedia-related queries
            try:
                search_query = user_input.replace("who is", "").strip()
                result = wikipedia.summary(search_query, sentences=1)
                print(f"🤖 (Jarvis): {result}")
                messages.append({"role": "assistant", "content": result})
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"Palm error: {e}")
                continue

    except Exception as e:
        print("Palm error: ", str(e))
        continue

    # Store the new interaction in the CSV file
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([messages[-1]["role"], messages[-1]["content"]])
