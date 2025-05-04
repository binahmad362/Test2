import os
import subprocess

# GitHub repository details
REPO_URL = "https://github.com/binahmad362/Test2.git"  # Replace with your repository URL
BRANCH = "main"  # Ensure this matches the branch in your GitHub repository
FILE_NAME = "test.txt"
CONTENT = "hello"

# Hardcoded GitHub Personal Access Token (PAT) (⚠ Security Risk)
GITHUB_PAT = "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"

# Git user details
GIT_USER_NAME = "binahmad362"  # Replace with your GitHub username
GIT_USER_EMAIL = "tajuttech360@gmail.com"  # Replace with your GitHub email

# Ensure repository directory exists
REPO_DIR = "Git"
if not os.path.exists(REPO_DIR):
    os.mkdir(REPO_DIR)
os.chdir(REPO_DIR)

# Function to write the file
def write_file():
    print(f"Creating file '{FILE_NAME}'...")
    try:
        with open(FILE_NAME, "w") as file:
            file.write(CONTENT)
        print(f"File '{FILE_NAME}' created with content: '{CONTENT}'")
    except Exception as e:
        print(f"Error writing file: {e}")
        exit(1)

# Function to initialize Git and push changes
def push_to_github():
    print("Initializing Git repository and pushing changes...")
    try:
        # Initialize a new Git repository
        subprocess.run(["git", "init"], check=True)

        # Set Git user details
        subprocess.run(["git", "config", "user.name", GIT_USER_NAME], check=True)
        subprocess.run(["git", "config", "user.email", GIT_USER_EMAIL], check=True)

        # Ensure correct branch is set
        subprocess.run(["git", "checkout", "-b", BRANCH], check=True)

        # Add and commit files
        subprocess.run(["git", "add", FILE_NAME], check=True)
        subprocess.run(["git", "commit", "-m", f"Added {FILE_NAME} with content '{CONTENT}'"], check=True)

        # Configure remote with token
        repo_url_with_token = REPO_URL.replace("https://", f"https://{GITHUB_PAT}@")
        subprocess.run(["git", "remote", "add", "origin", repo_url_with_token], check=True)

        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", BRANCH], check=True)
        print("Changes pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes: {e}")
        exit(1)

# Main function
def main():
    write_file()
    push_to_github()

if __name__ == "__main__":
    main()
