# Dollar Banknote Recognition App

A Flutter mobile application for recognizing US dollar banknote denominations designed specifically for visually impaired people.

## Features

- **Camera Integration**: Real-time camera preview for capturing dollar bill images
- **Banknote Recognition**: AI-powered recognition of US dollar banknote denominations ($1-$100)
- **Voice Feedback**: Text-to-speech functionality for accessibility
- **User-Friendly Interface**: Large buttons and clear visual indicators
- **Real-time Processing**: Fast recognition with visual feedback

## Supported Banknotes

- $1
- $2  
- $5
- $10
- $20
- $50
- $100

## Technical Implementation

### Architecture
- **MVVM Pattern**: Separation of UI and business logic
- **Service Layer**: Modular services for camera and recognition
- **Widget System**: Reusable UI components

### Key Technologies
- **Flutter**: Cross-platform mobile development framework
- **Dart**: Programming language
- **TensorFlow Lite**: Machine learning inference
- **Camera Plugin**: Hardware camera integration
- **Flutter TTS**: Text-to-speech synthesis
- **Image Processing**: Computer vision preprocessing

### Dependencies
```yaml
dependencies:
  flutter:
    sdk: flutter
  camera: ^0.10.5+5
  tflite_flutter: ^0.10.4
  flutter_tts: ^3.8.3
  permission_handler: ^11.0.1
  image: ^4.1.3
  path_provider: ^2.1.1
  flutter_screenutil: ^5.9.0
```

## Installation

1. Install Flutter SDK: https://flutter.dev/docs/get-started/install
2. Clone this repository
3. Run `flutter pub get` to install dependencies
4. Connect a device or start an emulator
5. Run `flutter run`

## Usage

1. Grant camera permissions when prompted
2. Point the camera at a banknote
3. Center the banknote in the frame guides
4. Tap "Capture & Recognize" button
5. Listen to the voice announcement of the recognized denomination

## Accessibility Features

- **Voice Guidance**: Automatic voice announcements for all actions
- **Large UI Elements**: Optimized for users with visual impairments
- **High Contrast**: Clear visual indicators
- **Simple Navigation**: Intuitive single-button operation

## Model Training (For Production)

To improve recognition accuracy:

1. Collect dataset of banknote images
2. Preprocess images (resize, normalize)
3. Train TensorFlow Lite model
4. Convert to .tflite format
5. Place model in `assets/models/` directory

## File Structure

```
lib/
  main.dart                 # App entry point
  screens/
    home_screen.dart        # Main application screen
  services/
    camera_service.dart     # Camera operations
    recognition_service.dart # ML recognition logic
  widgets/
    camera_preview_widget.dart  # Camera preview UI
    result_display_widget.dart  # Results display
```

## Permissions Required

- Camera: Required for capturing banknote images
- Storage: Required for saving temporary images

## Future Enhancements

- Support for other currencies
- Offline model optimization
- Haptic feedback
- Multi-language support
- Continuous recognition mode

## Contributing

This project is part of a diploma thesis on computer vision applications for accessibility.

## License

Educational use only.
