# MC-ModSec

MCModSec is a lightweight, Python-based static analysis tool designed to detect malicious payloads, infostealers, and credential-harvesting scripts hidden within compiled Minecraft modifications (.jar files).

## What is this?

Let's be real, the Minecraft modding scene is amazing, but it has been taking some hits lately. With malware campaigns like Fractureiser and Stargazers sneaking credential stealers into popular modpacks, downloading .jar files has become a bit of a gamble. Standard antiviruses usually do not care about what is happening deep inside your mods folder.

MCModSec is a lightweight Python tool I am building to scan your Minecraft mods for sketchy stuff—like hidden webhooks, hardcoded IPs, and token stealers—before you actually run the game. It peeks inside the .jar files safely in memory without executing any of the Java bytecode.
## What it does right now

NOTE: It is very much work in progress! Be careful when using it.

1. Reads the Manifests
Whether you are using Fabric, Quilt, or Forge, the scanner cracks open the archive and figures out exactly what the mod claims to be by reading its internal config files.

2. Scans the Bytecode
It digs into the compiled .class files, translates the raw data, and hunts for massive red flags like Discord webhooks and shady dropper domains using regular expressions.

3. Batch Scans the Whole Folder
Nobody plays with just one mod. You can drop your entire modpack into a target folder, and the script will sequentially chew through all of them in one go.
## What's coming next (The Roadmap)

This is currently only terminal-based, but I am actively working on upgrading it to a full desktop app. Here is what is on the menu:

1. A  CustomTkinter UI
Because staring at a terminal gets old. I am building a dark-mode graphical interface so you can just click a button, select your mod folder, and watch a progress bar do the heavy lifting.

2. Cryptographic Hashing
The engine will soon generate a unique SHA-256 fingerprint for every mod it scans to definitively identify files, even if they get renamed.

3. VirusTotal & API Integrations
I will be hooking those file hashes up to the VirusTotal API and checking them against the official Modrinth/CurseForge databases to catch tampered files instantly.

4. Pro-Level Threat Hunting
Moving away from basic Python regex and upgrading the engine to use industry-standard YARA rules and obfuscation detection.
## How to use it

  Clone this repo to your machine.
  Run python main.py in your terminal. It will politely create a test_ressources folder for you.
  Drop your sketchy (or totally safe) .jar files into that new folder.
  Run python main.py one more time and watch the console for the verdict!
