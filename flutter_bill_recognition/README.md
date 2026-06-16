# Flutter додаток для розпізнавання доларових банкнот

## 📱 Опис
Мобільний додаток на Flutter для розпізнавання номіналу доларових банкнот за допомогою TensorFlow Lite.

## 🚀 Встановлення та запуск

### 1. Встановлення Flutter
```bash
# Завантаження Flutter
https://flutter.dev/docs/get-started/install

# Перевірка встановлення
flutter doctor
```

### 2. Налаштування проекту
```bash
# Перейти в папку проекту
cd flutter_bill_recognition

# Встановити залежності
flutter pub get

# Створити папку assets/models якщо не існує
mkdir -p assets/models
```

### 3. Підготовка моделі
```bash
# Скопіювати TFLite модель в assets/models
# Потрібно створити bill_classifier.tflite з вашої моделі
cp ../models/bill_classifier.tflite assets/models/
```

### 4. Запуск додатку
```bash
# Для Android
flutter run

# Для iOS (потрібен macOS)
flutter run -d ios
```

## 📋 Вимоги
- Flutter SDK >= 3.0.0
- Android SDK (для Android)
- Xcode (для iOS)
- Камера на пристрої

## 🔧 Функціонал
- ✅ Зйомка фото через камеру
- ✅ Вибір зображення з галереї
- ✅ Розпізнавання номіналу банкноти
- ✅ Відображення точності розпізнавання
- ✅ Інтерактивний інтерфейс

## 📊 Класи розпізнавання
- 1 Dollar
- 2 Dollar
- 5 Dollar
- 10 Dollar
- 50 Dollar
- 100 Dollar

## ⚠️ Важливо
1. **TFLite модель**: Потрібно скопіювати `bill_classifier.tflite` в `assets/models/`
2. **Дозволи**: Додаток потребує дозволу на камеру
3. **Тестування**: Рекомендується тестувати на реальних банкнотах

## 🐛 Вирішення проблем

### Помилка "Модель не завантажена"
- Перевірте наявність `bill_classifier.tflite` в `assets/models/`
- Перевірте `pubspec.yaml` - секція `assets`

### Помилка дозволу камери
- Додайте дозволи в `android/app/src/main/AndroidManifest.xml`
- Для iOS налаштуйте в `ios/Runner/Info.plist`

## 📱 Скріншоти додатку
[Тут будуть скріншоти після запуску]

## 🤖 Технології
- **Flutter** - UI фреймворк
- **TensorFlow Lite** - ML інференс
- **Camera** - доступ до камери
- **Image Picker** - вибір з галереї
