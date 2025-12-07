import os
import shutil

mcEduPath = "/Applications/minecraft-edu.app"
materialBinsPath = None
scriptPath = os.path.dirname(os.path.abspath(__file__))
MCPACKS = os.path.join(scriptPath, "MCPACKS")
Temp = os.path.join(scriptPath, "Temp")
BackupMaterialBins = os.path.join(scriptPath, "BackupMaterialBins")
os.remove(os.path.join(BackupMaterialBins, "te"))
os.remove(os.path.join(MCPACKS, "te"))
os.remove(os.path.join(Temp, "te"))

def copyfiles(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
    
        # Only copy files (skip subfolders)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_file)

# Welcome
print("Welcome to edumacosinject!".center(28))
print("Made by jeremylpro on Github\n")

# Check First Time Use
if os.path.isfile(os.path.join(scriptPath, "NEW_USER")):
    # New User Prompts
    pathinput = input("Is Minecraft Education installed in /Applications/minecraft-edu.app?\n(Press enter key if yes, specify path AND name of .app if the path is different.)\nE.g. /Applications/Games/minecraft-edu.app\n")
    if not pathinput.startswith("/") and pathinput != "":
        print("Input is not a path, please restart the script.")
        quit()
    if not os.path.isdir(pathinput) and pathinput != "":
        print("Path does not exist, please restart the script.")
        quit()
    if not os.path.isdir(os.path.join(pathinput, "Contents/Resources/data/renderer/materials")) and pathinput != "":
        print("Path is either not a Minecraft Education install, or this script is too old. Please restart the script.")
        quit()
    if pathinput != "":
        mcEduPath = pathinput
    # Set Paths
    materialBinsPath = os.path.join(mcEduPath, "Contents/Resources/data/renderer/materials")
    # Save Settings
    with open(os.path.join(scriptPath, "settings.txt"), "w") as file:
        file.write(mcEduPath)
    print("Successfully set path to " + mcEduPath + "!")
    # Back Up material.bin Files
    print("Backing up material.bin files...")
    copyfiles(materialBinsPath, BackupMaterialBins)
    os.remove(os.path.join(scriptPath, "NEW_USER"))
    print("Success!")
else:
    # Read From settings.txt
    with open(os.path.join(scriptPath, "settings.txt"), "r") as file:
        lines = file.readlines()
        mcEduPath = lines[0]
        materialBinsPath = os.path.join(mcEduPath, "Contents/Resources/data/renderer/materials")

# List Options
option = input("Options:\n[1] Inject shaders in PACKS folder\n[2] Restore material bins from backup\n[3] (DO NOT SELECT IF SHADERS ARE CURRENTLY INJECTED) Backup material bins from current install\n")
if option == "1":
    print("Injecting shaders from MCPACKS folder...")
    # Extract Resource Packs
    for filename in os.listdir(MCPACKS):
        file_path = os.path.join(MCPACKS, filename)
        if filename != ".DS_Store":
            shutil.unpack_archive(file_path, Temp, format="zip")
    # Inject Vanilla Shaders
    for foldername in os.listdir(Temp):
        folder_path = os.path.join(Temp, foldername)
        if os.path.isdir(folder_path):
            copyfiles(os.path.join(folder_path, "renderer/materials"), materialBinsPath)
    # Clean Up
    shutil.rmtree(Temp)
    os.mkdir(Temp)
    print("Success!")
elif option == "2":
    print("Restoring from backup...")
    copyfiles(BackupMaterialBins, materialBinsPath)
    print("Success!")
elif option == "3":
    print("Backing up material bin files...")
    copyfiles(materialBinsPath, BackupMaterialBins)
else:
    print("Invalid option, please restart the script.")
    quit()
print("Thank you for using edumacosinject!")
quit()
