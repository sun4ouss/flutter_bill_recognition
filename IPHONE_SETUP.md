# iPhone Setup Guide for Flutter Testing

## Important: iPhone Testing Limitations

### Requirements for iPhone Development:
- **Mac computer** with macOS
- **Xcode** (from App Store)
- **Apple Developer Account** (free or paid)
- **iOS device** with iOS 11.0+
- **Lightning/USB-C cable**

### If you DON'T have a Mac:
**iPhone testing is not directly possible** from Windows PC. See alternatives below.

---

## Method 1: Direct iPhone Testing (Mac Required)

### Step 1: Install Xcode
1. Open App Store on Mac
2. Search and install "Xcode"
3. Launch Xcode and accept license agreement
4. Install additional components when prompted

### Step 2: Configure iPhone
1. **Enable Developer Mode on iPhone:**
   - Go to Settings > Privacy & Security
   - Scroll down to "Developer Mode"
   - Toggle it ON
   - Enter iPhone passcode when prompted
   - Restart iPhone

2. **Trust Your Mac:**
   - Connect iPhone to Mac via USB
   - Unlock iPhone
   - Tap "Trust" when prompted about "This Computer"

### Step 3: Configure Flutter for iOS
```bash
# On Mac
cd /path/to/your/project
flutter doctor

# Install iOS dependencies
flutter doctor --verbose
```

### Step 4: Run on iPhone
```bash
# Connect iPhone to Mac
flutter devices

# Run on iPhone
flutter run -d <iphone-id>
```

---

## Method 2: Alternatives for Windows Users

### Option A: Android Emulator (Recommended)
Since you're on Windows, use Android emulator:

#### Install Android Emulator:
1. **Install Android Studio:**
   - Download from https://developer.android.com/studio
   - Install with default settings
   - Launch Android Studio

2. **Create Virtual Device:**
   - In Android Studio: Tools > Device Manager
   - Click "Create Device"
   - Choose Pixel 6 or similar
   - Select latest Android version
   - Finish setup

3. **Run Flutter on Emulator:**
```bash
# Check available devices
flutter devices

# Run on emulator
flutter run -d <emulator-id>
```

### Option B: Web Testing
Test the app in web browser:

```bash
# Enable web support
flutter config --enable-web

# Run in Chrome
flutter run -d chrome
```

### Option C: Test with Real Images
Create a test script to test model with real dollar bill images:

```python
# Create test_with_images.py
import tensorflow as tf
import numpy as np
from PIL import Image
import os

def test_with_real_images():
    """Test model with real dollar bill images"""
    
    # Load TFLite model
    interpreter = tf.lite.Interpreter(model_path="assets/models/banknote_model.tflite")
    interpreter.allocate_tensors()
    
    # Get input/output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Load labels
    with open("assets/models/labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines() if line.strip()]
    
    # Test with images in test_images folder
    test_images_dir = "test_images"
    
    if not os.path.exists(test_images_dir):
        print(f"Create '{test_images_dir}' folder and add dollar bill images")
        return
    
    for image_file in os.listdir(test_images_dir):
        if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Load and preprocess image
            image_path = os.path.join(test_images_dir, image_file)
            image = Image.open(image_path)
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            input_data = np.expand_dims(image_array, axis=0).astype(np.float32)
            
            # Run inference
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            # Get prediction
            predicted_class = np.argmax(output_data[0])
            confidence = output_data[0][predicted_class]
            
            print(f"Image: {image_file}")
            print(f"Predicted: {labels[predicted_class]}")
            print(f"Confidence: {confidence:.4f}")
            print("-" * 40)

if __name__ == "__main__":
    test_with_real_images()
```

---

## Method 3: Build IPA for Testing (Advanced)

### If you have access to a Mac:
1. **Build IPA file:**
```bash
flutter build ipa
```

2. **Install on iPhone:**
   - Use Xcode to install
   - Or use TestFlight (requires Apple Developer account)
   - Or use AltStore (requires iOS 14+)

---

## Method 4: Remote Testing Services

### Online Services:
- **BrowserStack** - Real device testing online
- **Sauce Labs** - Cross-platform testing
- **Firebase Test Lab** - Android testing (not iOS)

---

## Quick Recommendation

### For Your Diploma Project:

**Best Option: Android Emulator on Windows**
1. Install Android Studio
2. Create Pixel 6 emulator
3. Test with camera emulator
4. Take screenshots for documentation

**Alternative: Test with Real Images**
1. Create `test_images/` folder
2. Add dollar bill photos
3. Run test script
4. Document results

### Why Android is Better for Testing:
- **Easier setup** on Windows
- **Camera emulator** works well
- **Debug logging** is better
- **Performance testing** is easier
- **Documentation** is straightforward

---

## iPhone Testing Summary

| Method | Requirements | Difficulty | Recommendation |
|--------|--------------|------------|----------------|
| Direct iPhone | Mac + Xcode | Hard | Only if you have Mac |
| Android Emulator | Windows PC | Easy | **Best for Windows** |
| Web Testing | Any PC | Easy | Limited camera testing |
| Real Images | Any PC | Medium | Good for model testing |

---

## Next Steps

1. **Choose Android Emulator** (recommended for Windows)
2. **Install Android Studio**
3. **Create virtual device**
4. **Test your app**
5. **Document results for diploma**

**Your app will work perfectly on iPhone once deployed to App Store, but for development/testing, Android emulator is much easier on Windows.**
