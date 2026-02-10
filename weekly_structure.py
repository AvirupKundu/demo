import os
import shutil
import pandas as pd
from datetime import datetime

# U: Lab
# Y: Hackathon
nas_paths = [r"U:\\Hackathon\\Kolkata\\Gitanjali_Park\\", r"U:\\Hackathon\\Kolkata\\Ecospace\\", r"U:\\Hackathon\\Kolkata\\Candor\\", r"Y:\\Hackathon\\Kolkatta\\Gitanjali Park\\", r"Y:\\Hackathon\\Kolkatta\\Gitanjali Park\\"]

# 📁 Path to the screen recording file
screen_recording_path = r"C:\\Projects\\Weekly_Structure\\Weekly_Structure\\Screen_Recorder.zip"

# 📁 Path to the Sample Test zip file
sample_code_path = r"C:\\Projects\\WEEKLY_STRUCTURE\\Weekly_Structure\\Test_Project-Sample_Code.zip"

# 📁 Path to the README file
readme_path = r"C:\\Projects\\WEEKLY_STRUCTURE\\Weekly_Structure\\README.md"

# 📁 Path to the Handbook file
handbook_path = r"C:\\Projects\\Weekly_Structure\\Weekly_Structure\\AI_Fridays_Participant_Handbook.pdf"

# Generate folder name with today's date
master_folder = f"Kolkata_AI_Friday_06-02-26_Master"
os.makedirs(master_folder, exist_ok=True)

# 📄 Try reading from Excel or CSV
file_name = "Kolkata.xlsx" if os.path.exists("Kolkata.xlsx") else "Kolkata.csv"
df = pd.read_excel(file_name) if file_name.endswith(".xlsx") else pd.read_csv(file_name)

# 🔑 Static model list
models = [
    "genailab-maas-gpt-35-turbo",
    "gemini-3-pro-preview",
    "azure/genailab-maas-gpt-4o-mini",
    "azure/genailab-maas-text-embedding-3-large",
    "azure/genailab-maas-whisper",
    "azure_ai/genailab-maas-DeepSeek-R1",
    "azure_ai/genailab-maas-Llama-3.2-90B-Vision-Instruct",
    "azure_ai/genailab-maas-Llama-3.3-70B-Instruct",
    "azure_ai/genailab-maas-Llama-4-Maverick-17B-128E-Instruct-FP8",
    "genailab-maas-gpt-4o",
    "azure_ai/genailab-maas-Phi-4-reasoning",
    "azure/genailab-maas-gpt-4.1-mini",
    "azure/genailab-maas-gpt-4.1-nano",
    "azure_ai/Llama-3.3-70B-Instruct_Mass",
    "azure_ai/genailab-maas-Phi-3.5-vision-instruct",
    "azure/genailab-maas-gpt-4.1",
    "azure/genailab-maas-gpt-5-mini",
    "genailab-maas-DeepSeek-V3-0324",
    "gemini-2.5-flash",
    "gemini-2.0-flash-001",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview"
]


# 🗂️ Create subfolders and .env files
for index, row in df.iterrows():
    # slno = str(row[0]).strip()
    team_alias = str(row[1]).strip().replace(" ", "_")
    team_name = str(row[4]).strip().replace(" ", "_")
    api_key = str(row[3]).strip()  # Column H is index 7

    team_folder = os.path.join(master_folder, f"Team_{team_alias}_{team_name}")
    os.makedirs(team_folder, exist_ok=True)

    # 📁 Create Solution subfolder
    solutions_folder = os.path.join(team_folder, "Solution")
    os.makedirs(solutions_folder, exist_ok=True)

    # 📁 Create Presentation subfolder
    presentation_folder = os.path.join(team_folder, "Presentation")
    os.makedirs(presentation_folder, exist_ok=True)

    # 📁 Create Screen Recording subfolder
    recording_folder = os.path.join(team_folder, "Recording")
    os.makedirs(recording_folder, exist_ok=True)

    # 📦 Copy handbook file
    try:
        shutil.copy(handbook_path, team_folder)
    except Exception as e:
        print(f"❌ Could not copy handbook to {team_folder}: {e}")

    # 📦 Copy Readme file
    try:
        shutil.copy(readme_path, team_folder)
    except Exception as e:
        print(f"❌ Could not copy README.md to {team_folder}: {e}")

    # 📦 Copy screenRecording.zip
    try:
        shutil.copy(screen_recording_path, team_folder)
    except Exception as e:
        print(f"❌ Could not copy screenRecording.zip to {team_folder}: {e}")

    # 📦 Copy testProject.zip
    try:
        shutil.copy(sample_code_path, team_folder)
    except Exception as e:
        print(f"❌ Could not copy {sample_code_path} to {team_folder} because of the following exception: {e}")

    env_path = os.path.join(team_folder, ".env")
    with open(env_path, "w") as env_file:
        env_file.write('api_endpoint="https://genailab.tcs.in/"\n')
        env_file.write(f'api_key="{api_key}"\n')
        for model in models:
            env_file.write(f'model="{model}"\n')

print(f"✅ Folder structure created under '{master_folder}'")

# 📤 Copy to NAS paths
for nas_path in nas_paths:
    destination = os.path.join(nas_path, master_folder)
    try:
        shutil.copytree(master_folder, destination)
        print(f"✅ Successfully copied {master_folder} to {destination}")
    except Exception as e:
        print(f"❌ Failed to copy {master_folder} to {nas_path}: {e}")

print("🎉 All tasks completed!")
