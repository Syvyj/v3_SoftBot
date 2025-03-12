import os
import sys
import venv
from pathlib import Path

def create_env():
    """Create virtual environment"""
    venv_dir = Path('.venv')
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create('.venv', with_pip=True)
        return True
    return False

def get_python_command():
    """Get the correct python command based on the platform"""
    if sys.platform == "win32":
        return str(Path('.venv/Scripts/python.exe'))
    return str(Path('.venv/bin/python'))

def get_pip_command():
    """Get the correct pip command based on the platform"""
    if sys.platform == "win32":
        return str(Path('.venv/Scripts/pip.exe'))
    return str(Path('.venv/bin/pip'))

def setup_project():
    """Setup the project"""
    try:
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('images', exist_ok=True)

        # Create virtual environment if it doesn't exist
        is_new_env = create_env()

        # Get the correct commands for the platform
        python_cmd = get_python_command()
        pip_cmd = get_pip_command()

        if is_new_env:
            # Upgrade pip
            os.system(f'"{python_cmd}" -m pip install --upgrade pip')

        # Install requirements
        os.system(f'"{pip_cmd}" install -r requirements.txt')

        # Create .env file if it doesn't exist
        env_file = Path('.env')
        if not env_file.exists():
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write('BOT_TOKEN=your_bot_token_here\n')
                f.write('ADMIN_CHAT_ID=your_admin_chat_id_here\n')
                f.write('TRACKER_ADMIN_CHAT_ID=your_tracker_admin_chat_id_here\n')

        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Edit the .env file with your bot token and admin chat IDs")
        print("2. Run the bot with:")
        if sys.platform == "win32":
            print("   .venv\\Scripts\\python bot.py")
        else:
            print("   .venv/bin/python bot.py")

    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_project() 