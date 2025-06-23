import requests
import time
from datetime import datetime

def read_names_from_file(filename):
    """Reads names from a text file (one name per line)"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []

def check_minecraft_name(username, session):
    """Checks if a Minecraft username is available"""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:  # Name is taken
            return False
        elif response.status_code == 404 and "Couldn't find any profile" in response.text:
            return True  # Name is available
        return False
    except requests.exceptions.RequestException as e:
        print(f"Network error checking {username}: {e}")
        return False

def main():
    input_file = "names.txt"  # Input file with names
    output_file = "available_names.txt"  # Output file
    
    print(f"Reading names from {input_file}...")
    names = read_names_from_file(input_file)
    if not names:
        return
    
    print(f"Checking {len(names)} names...\n")
    
    available_names = []
    session = requests.Session()
    start_time = time.time()
    checked_count = 0
    
    for i, name in enumerate(names, 1):
        if check_minecraft_name(name, session):
            available_names.append(name)
            print(f"\033[92m[AVAILABLE]\033[0m {name} ({i}/{len(names)})")
        else:
            print(f"\033[91m[TAKEN]\033[0m {name} ({i}/{len(names)})")
        
        checked_count += 1
        
        # Dynamic rate limiting
        if checked_count % 50 == 0:
            time.sleep(2)  # Longer pause every 50 names
        else:
            time.sleep(0.8)  # Base delay
        
        # Estimate remaining time
        if i % 10 == 0:
            elapsed = time.time() - start_time
            remaining = (elapsed/i) * (len(names)-i)
            print(f"Estimated time remaining: {remaining/60:.1f} minutes")

    # Save results with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"# Minecraft name availability check ({timestamp})\n")
        file.write(f"# Checked {len(names)} names, found {len(available_names)} available\n\n")
        file.write("\n".join(available_names))
    
    print(f"\nDone! Found {len(available_names)} available names out of {len(names)}")
    print(f"Results saved to {output_file}")
    print(f"Total time: {(time.time()-start_time)/60:.1f} minutes")

if __name__ == "__main__":
    main()