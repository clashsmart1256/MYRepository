from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import os
import subprocess
import json

print("=== Telegram Direct Uploader ===")
print()

with open('.env', 'r') as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
CHANNEL = os.getenv('CHANNEL')

if not all([API_ID, API_HASH, PHONE, CHANNEL]):
    print("Error: .env file me API_ID, API_HASH, PHONE, CHANNEL set karo!")
    print("Edit karo: nano .env")
    exit(1)

print(f"Using API_ID: {API_ID}")
print(f"Using PHONE: {PHONE}")
print(f"Using CHANNEL: {CHANNEL}")
print()

def pick_folder():
    print("Select folder from picker (or press Enter for manual path):")
    try:
        result = subprocess.run(['termux-storage-get', '-d'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print("Picker cancelled, entering manual path...")
            return None
    except Exception as e:
        print(f"Picker error: {e}")
        return None

def get_all_files(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            all_files.append(filepath)
    return all_files

def load_progress():
    try:
        with open('.upload_progress.json', 'r') as f:
            return json.load(f)
    except:
        return {'uploaded': [], 'folder': None}

def save_progress(uploaded_list, folder_path):
    data = {'uploaded': uploaded_list, 'folder': folder_path}
    with open('.upload_progress.json', 'w') as f:
        json.dump(data, f)

def clear_progress():
    try:
        os.remove('.upload_progress.json')
    except:
        pass

async def upload():
    client = TelegramClient('my_session', int(API_ID), API_HASH)
    await client.start(phone=PHONE)
    me = await client.get_me()
    print()
    print(f"Logged in as: {me.first_name}")
    
    try:
        if CHANNEL.startswith('-100'):
            channel_id = int(CHANNEL)
            channel = await client.get_entity(channel_id)
        else:
            channel = await client.get_entity(CHANNEL)
        print(f"Channel: {channel.title}")
    except Exception as e:
        print(f"Channel error: {e}")
        await client.disconnect()
        return
    
    print()
    print("=== FOLDER SELECTION ===")
    folder_path = pick_folder()
    
    if not folder_path:
        print()
        print("Select folder:")
        print("1. /storage/emulated/0/Download")
        print("2. /storage/emulated/0/DCIM/Camera")
        print("3. /storage/emulated/0/Movies")
        print("4. /storage/emulated/0/Documents")
        print("5. /storage/emulated/0/Pictures")
        print("6. Custom path")
        print()
        choice = input("Enter choice (1-6): ").strip()
        
        paths = {
            '1': '/storage/emulated/0/Download',
            '2': '/storage/emulated/0/DCIM/Camera',
            '3': '/storage/emulated/0/Movies',
            '4': '/storage/emulated/0/Documents',
            '5': '/storage/emulated/0/Pictures'
        }
        
        if choice in paths:
            folder_path = paths[choice]
        elif choice == '6':
            folder_path = input("Enter custom path: ").strip()
        else:
            print("Invalid choice!")
            await client.disconnect()
            return
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        await client.disconnect()
        return
    
    print()
    print(f"Folder: {folder_path}")
    all_files = get_all_files(folder_path)
    if not all_files:
        print("No files found in folder!")
        await client.disconnect()
        return
    print(f"Found {len(all_files)} files")
    print()
    progress = load_progress()
    if progress['folder'] == folder_path:
        uploaded = set(progress['uploaded'])
        remaining = [f for f in all_files if f not in uploaded]
        print(f"Resuming... {len(progress['uploaded'])} already uploaded, {len(remaining)} remaining")
        print()
    else:
        uploaded = set()
        remaining = all_files
        print("New upload session")
        print()
    failed_files = []
    for i, filepath in enumerate(remaining, 1):
        filename = os.path.basename(filepath)
        print(f"[{i}/{len(remaining)}] Uploading: {filename}")
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                await client.send_file(channel, filepath)
                print(f"OK: {filename}")
                uploaded.add(filepath)
                save_progress(list(uploaded), folder_path)
                break
            except FloodWaitError as e:
                print(f"Wait: {e.seconds} seconds...")
                await asyncio.sleep(e.seconds)
                retry_count += 1
            except Exception as e:
                error_msg = str(e)
                if 'timeout' in error_msg.lower() or 'network' in error_msg.lower() or 'connection' in error_msg.lower():
                    print("Network error... Waiting 10s")
                    await asyncio.sleep(10)
                    retry_count += 1
                else:
                    print(f"Error: {error_msg[:60]}")
                    failed_files.append(filepath)
                    break
        if retry_count >= max_retries:
            print(f"Failed after {max_retries} retries: {filename}")
            failed_files.append(filepath)
    print()
    print("=" * 50)
    print("UPLOAD COMPLETE")
    print("=" * 50)
    print(f"Total files: {len(all_files)}")
    print(f"Uploaded: {len(uploaded)}")
    print(f"Failed: {len(failed_files)}")
    if failed_files:
        print()
        print("Failed files:")
        for f in failed_files:
            print(f"  - {os.path.basename(f)}")
    if len(failed_files) == 0:
        clear_progress()
        print()
        print("Progress file cleared")
    await client.disconnect()
    print()
    print("Done!")

asyncio.run(upload())
