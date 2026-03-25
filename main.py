import zipfile
import os
from scanner import extractor, analyzer

"""
    Orchestrates the security scan for a single Minecraft modification file.
    
    This function validates the provided file path, safely opens the .jar file as a 
    zip archive, and delegates the data extraction and threat analysis to the respective 
    modules. It then prints a formatted report of the findings to the standard output.
    
    Parameters:
    jar_path (str): The absolute file path to the .jar file designated for scanning.
    
    Returns:
    None. Results are currently routed directly to the console.
"""
def run_scan(jar_path):
    if not os.path.exists(jar_path):
        print(f"Error: Could not locate {jar_path}")
        return

    print(f"\n{'='*50}")
    print(f"Analyzing: {os.path.basename(jar_path)}")
    print(f"{'='*50}")

    try:
        with zipfile.ZipFile(jar_path, 'r') as jar_archive:
            
            # Step 1: Extract Metadata
            metadata = extractor.get_mod_metadata(jar_archive)
            print(f"Mod Loader : {metadata['loader']}")
            print(f"Mod Name   : {metadata['name']}")
            print(f"Version    : {metadata['version']}\n")

            # Step 2: Hunt for Threats
            print("Scanning compiled bytecode...")
            threats = analyzer.scan_classes_for_threats(jar_archive)

            # Step 3: Report Results
            if threats:
                print("\n!!! THREATS DETECTED !!!")
                for threat in threats:
                    print(threat)
            else:
                print("\nScan Complete: No explicit threats detected.")
                
    except zipfile.BadZipFile:
        print("CRITICAL: The file is not a valid archive.")

if __name__ == "__main__":
    # Locate the directory where main.py is saved
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path to the test folder
    test_folder_name = "test_ressources"
    test_directory = os.path.join(script_directory, test_folder_name)
    
    # Ensure the directory exists before trying to scan it
    if not os.path.exists(test_directory):
        print(f"Directory '{test_folder_name}' not found. Creating it now...")
        os.makedirs(test_directory)
        print(f"Please drop your test .jar files into the new '{test_folder_name}' folder and run again.")
    else:
        # Gather all .jar files in the directory for batch processing
        jar_files = [f for f in os.listdir(test_directory) if f.endswith('.jar')]
        
        if not jar_files:
            print(f"No .jar files found in the '{test_folder_name}' directory.")
        else:
            print(f"Found {len(jar_files)} .jar file(s). Starting batch scan...\n")
            
            # Loop through and scan each file sequentially
            for file_name in jar_files:
                absolute_jar_path = os.path.join(test_directory, file_name)
                run_scan(absolute_jar_path)