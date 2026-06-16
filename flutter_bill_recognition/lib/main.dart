import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:image/image.dart' as img;
 
void main() {
  runApp(const BillRecognitionApp());
}
 
/// Кореневий віджет застосунку
class BillRecognitionApp extends StatelessWidget {
  const BillRecognitionApp({super.key});
 
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bill Recognition',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const CameraScreen(),
    );
  }
}
 
/// Головний екран із камерою та кнопками розпізнавання
class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});
 
  @override
  State<CameraScreen> createState() => _CameraScreenState();
}
 
class _CameraScreenState extends State<CameraScreen> {
  CameraController? _cameraController;
  List<CameraDescription>? _cameras;
  Interpreter? _interpreter;
  bool _isModelLoaded = false;
  String _result = '';
  double _confidence = 0.0;
  bool _isProcessing = false;
 
  /// Назви класів у тому ж порядку, що й виходи моделі
  final List<String> _classNames = [
    '1 Dollar', '2 Dollar', '5 Dollar',
    '10 Dollar', '50 Dollar', '100 Dollar',
  ];
 
  /// Мінімальна впевненість для показу результату
  static const double _confidenceThreshold = 0.85;
 
  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _loadModel();
  }
 
  @override
  void dispose() {
    if (_isModelLoaded) _interpreter?.close();
    _cameraController?.dispose();
    super.dispose();
  }
 
  /// Завантажує TFLite-модель із папки assets
  Future<void> _loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset(
        'assets/models/bill_classifier_v3.tflite',
        options: InterpreterOptions()..threads = 4,
      );
      setState(() => _isModelLoaded = true);
    } catch (e) {
      _showMessage('Не вдалося завантажити модель');
    }
  }
 
  /// Запитує дозвіл і ініціалізує першу доступну камеру
  Future<void> _initializeCamera() async {
    var cameraStatus = await Permission.camera.request();
    if (cameraStatus.isGranted) {
      _cameras = await availableCameras();
      if (_cameras != null && _cameras!.isNotEmpty) {
        _cameraController = CameraController(
          _cameras![0],
          ResolutionPreset.high,
          enableAudio: false,
        );
        await _cameraController!.initialize();
        if (mounted) setState(() {});
      }
    } else {
      _showMessage('Потрібен дозвіл на використання камери');
    }
  }
 
  /// Читає файл зображення, готує тензор і запускає інференс
  Future<void> _recognizeImage(File imageFile) async {
    if (!_isModelLoaded || _interpreter == null) {
      _showMessage('Модель ще не завантажена');
      return;
    }
 
    try {
      final imageBytes = await imageFile.readAsBytes();
      img.Image? image = img.decodeImage(imageBytes);
      if (image == null) throw Exception('Не вдалося декодувати зображення');
 
      // Приводимо зображення до розміру, очікуваного моделлю
      img.Image resized = img.copyResize(image, width: 224, height: 224);
 
      final input = _imageToFloat32Input(resized);
 
      // Вихід моделі: масив ймовірностей для кожного класу
      final output = [List<double>.filled(6, 0.0)];
 
      _interpreter!.run(input, output);
 
      final probabilities = output[0];
      int maxIndex = 0;
      double maxProb = probabilities[0];
 
      // Шукаємо клас із найвищою ймовірністю
      for (int i = 1; i < probabilities.length; i++) {
        if (probabilities[i] > maxProb) {
          maxProb = probabilities[i];
          maxIndex = i;
        }
      }
 
      setState(() {
        if (maxProb >= _confidenceThreshold) {
          _result = _classNames[maxIndex];
          _confidence = maxProb * 100;
        } else {
          // Впевненість нижче порогу — результат ненадійний
          _result = 'Не розпізнано';
          _confidence = maxProb * 100;
        }
      });
    } catch (e) {
      setState(() {
        _result = 'Помилка розпізнавання';
        _confidence = 0;
      });
    }
  }
 
  /// Перетворює зображення у 4-вимірний тензор [1, 224, 224, 3]
  /// зі значеннями пікселів, нормалізованими у діапазон [0, 1]
  List<List<List<List<double>>>> _imageToFloat32Input(img.Image image) {
    final inputBuffer = List.generate(
      1,
      (_) => List.generate(
        224,
        (y) => List.generate(
          224,
          (x) => List.generate(3, (_) => 0.0),
        ),
      ),
    );
 
    for (int y = 0; y < 224; y++) {
      for (int x = 0; x < 224; x++) {
        final pixel = image.getPixel(x, y);
        inputBuffer[0][y][x][0] = pixel.r.toDouble() / 255.0; // R
        inputBuffer[0][y][x][1] = pixel.g.toDouble() / 255.0; // G
        inputBuffer[0][y][x][2] = pixel.b.toDouble() / 255.0; // B
      }
    }
    return inputBuffer;
  }
 
  /// Робить знімок камерою та передає його на розпізнавання
  Future<void> _captureAndRecognize() async {
    if (_cameraController == null ||
        !_cameraController!.value.isInitialized ||
        _isProcessing) return;
 
    setState(() {
      _isProcessing = true;
      _result = '';
    });
 
    try {
      final image = await _cameraController!.takePicture();
      await _recognizeImage(File(image.path));
    } catch (e) {
      _showMessage('Помилка зйомки фото');
    } finally {
      setState(() => _isProcessing = false);
    }
  }
 
  /// Відкриває галерею та передає вибране фото на розпізнавання
  Future<void> _pickImageFromGallery() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
 
    if (pickedFile != null) {
      setState(() {
        _isProcessing = true;
        _result = '';
      });
      try {
        await _recognizeImage(File(pickedFile.path));
      } catch (e) {
        _showMessage('Помилка обробки зображення');
      } finally {
        setState(() => _isProcessing = false);
      }
    }
  }
 
  /// Показує короткe повідомлення у нижній частині екрана
  void _showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.blue),
    );
  }
 
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Розпізнавання банкнот'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          // Превью камери або індикатор завантаження
          Expanded(
            flex: 2,
            child: _cameraController != null &&
                    _cameraController!.value.isInitialized
                ? CameraPreview(_cameraController!)
                : const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(),
                        SizedBox(height: 16),
                        Text('Ініціалізація камери...'),
                      ],
                    ),
                  ),
          ),
 
          // Блок із результатом розпізнавання
          Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Text(
                  'Результат розпізнавання:',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 8),
                Text(
                  _result.isEmpty
                      ? 'Натисніть кнопку для зйомки'
                      : _result == 'Не розпізнано'
                          ? '⚠️ Банкноту не розпізнано. Спробуйте ще раз.'
                          : '$_result (${_confidence.toStringAsFixed(1)}%)',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: _result.isEmpty
                            ? Colors.grey
                            : _result == 'Не розпізнано'
                                ? Colors.orange
                                : Colors.green,
                        fontWeight: FontWeight.bold,
                      ),
                ),
                // Індикатор прогресу під час обробки
                if (_isProcessing) ...[
                  const SizedBox(height: 16),
                  const LinearProgressIndicator(),
                  const SizedBox(height: 8),
                  const Text('Обробка зображення...'),
                ],
              ],
            ),
          ),
 
          // Кнопки: зйомка камерою та вибір із галереї
          Container(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: (!_isProcessing && _isModelLoaded)
                        ? _captureAndRecognize
                        : null,
                    icon: _isProcessing
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.camera_alt),
                    label: Text(_isProcessing ? 'Обробка...' : 'Зняти фото'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: (!_isProcessing && _isModelLoaded)
                        ? _pickImageFromGallery
                        : null,
                    icon: const Icon(Icons.photo_library),
                    label: const Text('Галерея'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
 