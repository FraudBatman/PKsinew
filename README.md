# PKsinew

**PKsinew** is a companion app/frontend launcher for **Gen 3 Pokémon games** that lets you **track your progress across all 5 GBA games**.

It allows you to:
- Access Sinew **default start+select**
- Gain **achievements and rewards**
- Handle **mass storage & transferring Pokémon between games**
- Access **mythical rewards**
- Explore **re-imagined abandoned features** from the original games
- Export **save data to readable text file** for other projects

PKsinew supports **Windows, macOS, and Linux**, and works best with a **controller** for seamless gameplay tracking.

**Devlog / Updates:** [Sinew Devlog](https://pksinew.hashnode.dev/pksinew-devlog-index-start-here)

**Discord:** [Sinew Discord](https://discord.gg/t28tmQsyuq)

---

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [Install Python 3](#install-python-3)
3. [Install Dependencies](#install-dependencies)
4. [Prepare the Launcher](#prepare-the-launcher)
5. [Add ROMs](#add-roms)
6. [Run the App](#run-the-app)
7. [First-time In-App Setup](#first-time-in-app-setup)
8. [Tips & Notes](#tips--notes)

---

## Quick Setup

Clone the repo:

```bash
git clone https://github.com/Cambotz/PKsinew.git
cd PKsinew
```

> ⚠️ On older macOS/Linux, HTTPS may fail. Use SSH or bypass SSL when cloning.

---

## Install Python 3

| Platform | Instructions |
|----------|--------------|
| **Windows** | [Download Python 3.12](https://www.python.org/downloads/windows/) |
| **macOS** | [Download Python 3](https://www.python.org/downloads/macos/) |
| **Linux** | See below |

### Windows — Important Installation Steps

1. Download **Python 3.12** from the link above (3.12 is recommended for best compatibility)
2. Run the installer
3. **On the first screen, check the box that says "Add Python to PATH"** — this is critical. If you skip this, commands won't work
4. Click **Install Now** and let it finish
5. Open **PowerShell** (search for it in the Start menu) and verify it worked:

```powershell
python --version
```

You should see something like `Python 3.12.x`. If you get an error, you likely missed the PATH checkbox — re-run the installer and check it.

### macOS

[Download Python 3](https://www.python.org/downloads/macos/) and follow the standard installer.

**Verify installation:**

```bash
python3 --version
```

### Linux

```bash
sudo apt install python3 python3-pip
```

**Verify installation:**

```bash
python3 --version
```

---

## Install Dependencies

All commands from this point on need to be run from **inside the PKsinew folder**. Here's how to open a terminal there:

<details>
<summary><b>Windows — Opening PowerShell in the PKsinew folder</b></summary>

**Option A (easiest — Windows 11):**
1. Open File Explorer and navigate to the PKsinew folder
2. Right-click on an empty space inside the folder
3. Select **"Open in Terminal"**

**Option B (Windows 10):**
1. Open File Explorer and navigate to the PKsinew folder
2. Hold **Shift** and right-click on an empty space inside the folder
3. Select **"Open PowerShell window here"**

**Option C (manual cd):**
1. Open PowerShell from the Start menu
2. Type `cd` followed by the path to your PKsinew folder, for example:
   ```powershell
   cd C:\Users\YourName\Downloads\PKsinew
   ```

> ⚠️ Do **not** use Command Prompt (cmd) — use PowerShell only.

</details>

<details>
<summary><b>macOS / Linux — Opening a terminal in the PKsinew folder</b></summary>

**macOS:**
1. Right-click the PKsinew folder in Finder
2. Select **"New Terminal at Folder"** (if available), or open Terminal and drag the folder into it

**Linux:**
1. Most file managers support right-click → **"Open Terminal Here"**
2. Or open a terminal and `cd` to the folder:
   ```bash
   cd ~/Downloads/PKsinew
   ```

</details>

Once your terminal is open inside the PKsinew folder, install the dependencies:

### Windows (PowerShell)

```powershell
pip install pillow numpy pygame requests
```

### macOS / Linux

```bash
pip3 install pillow numpy pygame requests
```

> **Note:** Pillow replaces PIL. NumPy and Pygame are required for Sinew. requests is used to build the database.

If pip gives a permissions error on macOS/Linux, try:

```bash
pip3 install --user pillow numpy pygame requests
```

---

## Prepare the Launcher

<details>
<summary><b>Windows</b></summary>

Double-click `Sinew.bat` to launch.

If nothing happens, right-click it and select **Run as administrator**, or open PowerShell in the PKsinew folder and run:

```powershell
python main.py
```

</details>

<details>
<summary><b>macOS</b></summary>

1. Make the launcher executable:
   ```bash
   chmod +x Sinew.bat
   ```

2. Right-click `Sinew.bat` → **Get Info** → **Open with:** Terminal → **Change All...**

3. Double-click `Sinew.bat` to run

</details>

<details>
<summary><b>Linux</b></summary>

1. Make the launcher executable:
   ```bash
   chmod +x Sinew.bat
   ```

2. Run from terminal:
   ```bash
   ./Sinew.bat
   ```

   Or create a desktop shortcut pointing to the script.

</details>

---

## Add ROMs

1. Place your legally obtained ROMs in the `roms` folder
2. Supported formats: `.gba`, `.zip`, `.7z`
3. Supported games:
   - Pokémon Ruby
   - Pokémon Sapphire
   - Pokémon Emerald
   - Pokémon FireRed
   - Pokémon LeafGreen

---

## Run the App

Make sure your terminal is open inside the PKsinew folder (see [Install Dependencies](#install-dependencies) above for how to do this), then run:

**Windows (PowerShell):**
```powershell
python main.py
```

**macOS / Linux:**
```bash
python3 main.py
```

> 💡 **Tip:** Using a controller is strongly recommended for the best experience.

---

## First-time In-App Setup

1. **Map your controller buttons** in Settings
2. Point each game slot to its ROM file
3. Start playing — achievements and tracking begin automatically

---

## Tips & Notes

- Save files are stored in the `saves/` folder — back these up regularly
- Logs are written to `sinew.log` in the root folder — include this if reporting a bug
- If the app crashes on launch, check that all dependencies installed correctly by running `pip show pygame` in PowerShell
- Controller is highly recommended but keyboard works too

---

## Troubleshooting

**"python is not recognized" error on Windows**
> You missed the "Add Python to PATH" checkbox during installation. Re-run the Python installer, choose "Modify", and enable the PATH option. Or uninstall and reinstall with the checkbox checked.

**"pip is not recognized" on Windows**
> Same cause as above — Python isn't on your PATH. Re-run the installer with the PATH option enabled.

**Black screen / app won't start**
> Make sure all dependencies are installed. Open PowerShell and run:
> ```powershell
> pip install pillow numpy pygame requests
> ```

**"No such file or directory: main.py" error**
> Your terminal isn't open in the PKsinew folder. See the [Install Dependencies](#install-dependencies) section for how to open PowerShell directly inside the folder.

**Game not detected**
> Make sure your ROM filename contains the game name (e.g. `Pokemon Ruby.gba`). Check the `roms/` folder and ensure the file extension is `.gba`.
