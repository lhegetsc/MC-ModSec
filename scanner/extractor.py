import zipfile
import json

"""
    Identifies the mod loader and extracts relevant metadata from the archive.
    
    This function inspects the contents of a provided ZipFile object to determine 
    if the mod was built for Fabric, Quilt, or Forge. It then opens the corresponding 
    configuration file directly in memory to extract the mod's declared identity.
    
    Parameters:
    jar_archive (zipfile.ZipFile): The actively opened Jar archive being analyzed.
    
    Returns:
    dict: A dictionary containing the 'loader' type, the mod 'name', and the 'version'.
"""
def get_mod_metadata(jar_archive):
    """Identifies the mod loader and extracts metadata."""
    archive_files = jar_archive.namelist()
    metadata = {"name": "Unknown", "version": "Unknown", "loader": "Unknown"}

    try:
        if 'fabric.mod.json' in archive_files:
            metadata["loader"] = "Fabric"
            with jar_archive.open('fabric.mod.json') as f:
                data = json.load(f)
                metadata["name"] = data.get('name', 'Unknown')
                metadata["version"] = data.get('version', 'Unknown')
                
        elif 'quilt.mod.json' in archive_files:
            metadata["loader"] = "Quilt"
            with jar_archive.open('quilt.mod.json') as f:
                data = json.load(f)
                metadata["name"] = data.get('quilt_loader', {}).get('metadata', {}).get('name', 'Unknown')
                metadata["version"] = data.get('quilt_loader', {}).get('metadata', {}).get('version', 'Unknown')
                
        elif 'META-INF/mods.toml' in archive_files:
            metadata["loader"] = "Forge"
            # Forge uses TOML format, which is slightly harder to parse natively than JSON.
            with jar_archive.open('META-INF/mods.toml') as f:
                raw_toml = f.read().decode('utf-8', errors='ignore')
                for line in raw_toml.split('\n'):
                    if line.startswith('displayName'):
                        metadata["name"] = line.split('=')[-1].strip().strip('"')
                    elif line.startswith('version'):
                        metadata["version"] = line.split('=')[-1].strip().strip('"')
    except Exception as e:
        print(f"Error parsing metadata: {e}")

    return metadata