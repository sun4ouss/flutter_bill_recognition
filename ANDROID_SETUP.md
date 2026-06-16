# Android SDK Setup Guide

## Problem: Android SDK components missing

Flutter is working, but Android development tools need to be installed.

---

## Step 1: Install Android Studio

### Download and Install:
1. **Go to:** https://developer.android.com/studio
2. **Download:** Android Studio (latest version)
3. **Run installer:** Follow default installation
4. **Launch Android Studio** after installation

### First-time Setup:
1. **Welcome screen:** Select "Standard" installation
2. **Accept licenses:** Click through all license agreements
3. **Download components:** Wait for SDK and tools to download
4. **Finish setup:** Click "Finish" when complete

---

## Step 2: Install Required Components

### In Android Studio:
1. **File > Settings** (or Tools > SDK Manager)
2. **Go to:** Appearance & Behavior > System Settings > Android SDK
3. **Install these:**
   - **Android SDK Platform-Tools** (latest)
   - **Android SDK Command-line Tools** (latest)
   - **Android 13 (API level 33)** - Recommended
   - **Android 12 (API level 31)** - Minimum

### Alternative: Command Line Installation
If Android Studio installation fails:

1. **Download Command Line Tools:**
   - Go to: https://developer.android.com/studio#command-line-tools-only
   - Download: "Command line tools only"

2. **Extract to:** `C:\Android\Sdk\cmdline-tools\latest\`

3. **Set Environment Variable:**
   - Win + R → `sysdm.cpl`
   - Advanced → Environment Variables
   - New → `ANDROID_HOME` = `C:\Android\Sdk`
   - Add to PATH: `%ANDROID_HOME%\cmdline-tools\latest\bin`

---

## Step 3: Accept Android Licenses

### Using Flutter:
```bash
# Run from project directory
C:\flutter\flutter\bin\flutter.bat doctor --android-licenses

# Type 'y' for all licenses when prompted
```

### Expected Output:
```
Android SDK license not accepted. Review the terms that have not been accepted.
1/5: 
...
Do you accept the license? (y/N): y
```

---

## Step 4: Create Android Virtual Device

### In Android Studio:
1. **Tools > Device Manager**
2. **Click "Create Device"**
3. **Choose device:** Pixel 6 or similar
4. **Choose system image:**
   - Recommended: Android 13 (API 33)
   - Or: Android 12 (API 31)
5. **Download system image** if not present
6. **Finish setup**

### Emulator Settings:
- **RAM:** 4GB minimum (6GB recommended)
- **Internal Storage:** 6GB minimum
- **Graphics:** Hardware - GLES 2.0+

---

## Step 5: Verify Installation

### Check Flutter Doctor:
```bash
C:\flutter\flutter\bin\flutter.bat doctor
```

### Expected Output:
```
[✓] Flutter (Channel stable, 3.41.6)
[✓] Windows Version (Windows 10 Pro 64-bit)
[✓] Android toolchain (develop for Android devices)
[✓] Chrome - develop for the web
[!] Visual Studio - develop Windows apps
[✓] Connected device (1 available)
```

### Check Connected Devices:
```bash
C:\flutter\flutter\bin\flutter.bat devices
```

### Expected Output:
```
Found 1 connected device:
Pixel 6 API 33 (mobile) • emulator-5554 • android-x64 • Android 13 (API 33)
```

---

## Step 6: Run Your App

### With Emulator:
```bash
cd C:\Users\Sanya\Desktop\progaduplom
C:\flutter\flutter\bin\flutter.bat run
```

### With Physical Phone:
1. **Enable USB debugging** on phone
2. **Connect phone** to PC
3. **Allow USB debugging** when prompted
4. **Run app:**
```bash
C:\flutter\flutter\bin\flutter.bat run
```

---

## Troubleshooting

### Issue: "cmdline-tools component is missing"
**Solution:**
1. Install Android Studio
2. Or download command-line tools separately
3. Set ANDROID_HOME environment variable

### Issue: "Android license status unknown"
**Solution:**
```bash
C:\flutter\flutter\bin\flutter.bat doctor --android-licenses
# Type 'y' for all licenses
```

### Issue: "No connected devices"
**Solution:**
1. Create Android emulator in Android Studio
2. Or connect physical phone with USB debugging
3. Run `flutter devices` to verify

### Issue: Visual Studio warnings
**Solution:**
- This is optional for Flutter development
- Only needed if developing Windows desktop apps
- Can be ignored for mobile development

---

## Quick Setup Commands

### Install Android Studio (Recommended):
```bash
# Download from: https://developer.android.com/studio
# Run installer with default settings
# Launch Android Studio
# Accept all licenses and downloads
```

### Verify Everything:
```bash
# Check Flutter environment
C:\flutter\flutter\bin\flutter.bat doctor

# Accept Android licenses
C:\flutter\flutter\bin\flutter.bat doctor --android-licenses

# Check devices
C:\flutter\flutter\bin\flutter.bat devices

# Run your app
cd C:\Users\Sanya\Desktop\progaduplom
C:\flutter\flutter\bin\flutter.bat run
```

---

## What to Do Right Now

1. **Install Android Studio** from developer.android.com
2. **Launch Android Studio** and complete initial setup
3. **Accept Android licenses** with `flutter doctor --android-licenses`
4. **Create emulator** in Device Manager
5. **Run your app** with `flutter run`

**After this, your app will be ready for testing!** 🚀
