import re

"""
These are the regular expressions used to identify potential threats within the bytecode of compiled Java classes.
- WEBHOOK_PATTERN: Detects strings that resemble Discord webhook URLs, which are commonly used for exfiltrating data or sending notifications to attackers.
- IPV4_PATTERN: Identifies hardcoded IPv4 addresses, which may indicate attempts to connect to external servers for command and control or data exfiltration.
- SUSPICIOUS_DOMAINS: Flags references to known file hosting and pastebin services that are often used by attackers to host malicious payloads or share stolen data.

TODO: add more patterns and improve existing ones as needed, such as:
- Suspicious API calls (e.g., Runtime.exec, ProcessBuilder)
- Obfuscated strings that may indicate hidden functionality
"""
# Pre-compile the regular expressions for maximum performance
WEBHOOK_PATTERN = re.compile(r"discord(?:app)?\.com/api/webhooks/")
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SUSPICIOUS_DOMAINS = re.compile(r"(?:pastebin\.com|raw\.githubusercontent\.com|anonfiles\.com)")


"""
    Scans compiled Java classes within the archive for known threat signatures.
    
    This function iterates through all files in the provided ZipFile object, filtering 
    specifically for compiled '.class' files. It decodes the raw bytecode into text, 
    ignoring unreadable binary characters, and searches the resulting strings for 
    Discord webhooks, hardcoded IPv4 addresses, and suspicious dropper domain names.
    
    Parameters:
    jar_archive (zipfile.ZipFile): The actively opened Jar archive being analyzed.
    
    Returns:
    list: A collection of string messages detailing any discovered threat signatures.
"""
def scan_classes_for_threats(jar_archive):
    archive_files = jar_archive.namelist()
    findings = []

    for file_name in archive_files:
        if file_name.endswith('.class'):
            raw_data = jar_archive.read(file_name).decode('utf-8', errors='ignore')
            
            if WEBHOOK_PATTERN.search(raw_data):
                findings.append(f"[WEBHOOK] Hidden Discord webhook found in {file_name}")
                
            if IPV4_PATTERN.search(raw_data):
                findings.append(f"[IP ADDRESS] Hardcoded IPv4 address found in {file_name}")
                
            if SUSPICIOUS_DOMAINS.search(raw_data):
                findings.append(f"[DROPPER DOMAIN] Suspicious external domain found in {file_name}")

    return findings