# script_log_json_paths.py

import pathlib

def find_and_log_json_paths(source_folder, output_file):
    """
    Recursively finds all .json files in a source folder and writes their
    absolute paths to a text file.

    Args:
        source_folder (str): The path to the folder to search in.
        output_file (str): The path to the text file where paths will be saved.
    """
    source_path = pathlib.Path(source_folder)
    output_file_path = pathlib.Path(output_file)

    # --- 1. Ensure the output file's parent directory exists ---
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # --- 2. Find all JSON files recursively ---
    # .rglob('*.json') finds all files matching the pattern '*.json'
    json_files = list(source_path.rglob('*.json'))
    
    if not json_files:
        print(f"No .json files found in '{source_path}'.")
        # Still create an empty output file for consistency
        output_file_path.touch()
        print(f"Empty output file created at '{output_file_path}'.")
        return

    print(f"Found {len(json_files)} JSON file(s). Writing paths to '{output_file_path}'...")

    # --- 3. Write the paths to the output file ---
    # 'w' mode opens the file for writing, creating it if it doesn't exist
    # or overwriting it if it does.
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for json_file in json_files:
                # .resolve() gets the full absolute path of the file
                absolute_path = json_file.resolve()
                f.write(f"{absolute_path}\n")
        
        print(f"\nSuccessfully wrote {len(json_files)} paths to the file.")
    except IOError as e:
        print(f"Error writing to file {output_file_path}: {e}")

# --- SCRIPT EXECUTION ---
if __name__ == "__main__":
    
    source_directory = "C:/Users/ashwa/Downloads/Android Forensics/Android Forensics/output"

    # Define the name and location of the output text file
    output_text_file = 'json_file_paths.txt'

    # Check if placeholder paths have been changed
   
    find_and_log_json_paths(source_directory, output_text_file)