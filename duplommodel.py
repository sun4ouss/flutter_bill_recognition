import sys, os

if sys.platform == "win32":

    sys.stdout.reconfigure(encoding='utf-8')

    os.system('chcp 65001 > nul 2>&1')



import tensorflow as tf

from tensorflow.keras import layers, models, callbacks

from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import numpy as np

from sklearn.metrics import classification_report, confusion_matrix

import seaborn as sns

import pandas as pd



DATA_DIR = r"C:\Users\Sanya\Desktop\duplom\dataset"

MODEL_DIR = "models"

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32



class_map = {

    '01_1 Dollar': 0, '02_2 Dollar': 1, '03_5 Dollar': 2,

    '04_10 Dollar': 3, '05_50 Dollar': 4, '06_100 Dollar': 5,

}



print("=== Новий запуск з аугментацією ===")

Path(MODEL_DIR).mkdir(exist_ok=True)



# Збираємо дані

image_paths = []

labels = []

for class_name, cid in class_map.items():

    folder = Path(DATA_DIR) / class_name

    if folder.exists():

        files = [str(f) for f in folder.glob("*.*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]

        image_paths.extend(files)

        labels.extend([cid] * len(files))

        print(f"{class_name}: {len(files)} фото")



# Validate dataset

if len(image_paths) == 0:

    print("ERROR: No images found in dataset!")

    print(f"Check path: {DATA_DIR}")

    sys.exit(1)



if len(set(labels)) < 2:

    print("ERROR: Need at least 2 classes for training!")

    sys.exit(1)



print(f"Total images: {len(image_paths)}")

print(f"Classes found: {len(set(labels))}")



# Proper train/val split

train_paths, val_paths, train_labels, val_labels = train_test_split(

    image_paths, labels, test_size=0.2, stratify=labels, random_state=42

)



# Validate split

if len(train_paths) == 0 or len(val_paths) == 0:

    print("ERROR: Train or validation set is empty!")

    sys.exit(1)



print(f"Train: {len(train_paths)} images")

print(f"Val: {len(val_paths)} images")



# Dataset + augmentation

def augment(img):

    img = tf.image.random_flip_left_right(img)

    img = tf.image.random_brightness(img, 0.15)

    img = tf.image.random_contrast(img, 0.8, 1.2)

    img = tf.image.random_saturation(img, 0.8, 1.2)

    return img



def load_image(path, label, training=False):

    img = tf.io.read_file(path)

    img = tf.image.decode_image(img, channels=3, expand_animations=False)

    img = tf.image.resize(img, IMAGE_SIZE)

    img = tf.cast(img, tf.float32) / 255.0

    if training:

        img = augment(img)

    return img, label



# Create proper datasets

train_ds = tf.data.Dataset.from_tensor_slices((train_paths, train_labels))

train_ds = train_ds.map(lambda x,y: load_image(x,y,True), num_parallel_calls=tf.data.AUTOTUNE)

train_ds = train_ds.shuffle(2000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)



val_ds = tf.data.Dataset.from_tensor_slices((val_paths, val_labels))

val_ds = val_ds.map(lambda x,y: load_image(x,y,False), num_parallel_calls=tf.data.AUTOTUNE)

val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)



# Модель

base = tf.keras.applications.MobileNetV2(input_shape=(*IMAGE_SIZE, 3), include_top=False, weights='imagenet')

base.trainable = False



model = models.Sequential([

    base,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.5),

    layers.Dense(256, activation='relu'),

    layers.Dropout(0.5),

    layers.Dense(6, activation='softmax')

])



model.compile(optimizer=tf.keras.optimizers.Adam(0.0005),

              loss='sparse_categorical_crossentropy',

              metrics=['accuracy'])



model.summary()



callbacks_list = [

    callbacks.EarlyStopping(patience=8, restore_best_weights=True, verbose=1),

    callbacks.ReduceLROnPlateau(factor=0.5, patience=4, verbose=1),

    callbacks.ModelCheckpoint(f"{MODEL_DIR}/best_v3.keras", monitor='val_accuracy', save_best_only=True, verbose=1)

]



history = model.fit(train_ds, validation_data=val_ds, epochs=20, 

                    callbacks=callbacks_list, verbose=1)



# Графіки

plt.plot(history.history['accuracy'], label='Train')

plt.plot(history.history['val_accuracy'], label='Val')

plt.legend()

plt.title('Accuracy')

plt.grid(True)

plt.savefig(f"{MODEL_DIR}/acc_plot.png")

plt.show()



print(f"Найкраща val_accuracy: {max(history.history.get('val_accuracy', [0])):.4f}")



# === ДОДАТКОВЕ ЗБЕРЕЖЕННЯ ДЛЯ TFLITE ===
print("\n" + "="*50)
print("ДОДАТКОВЕ ЗБЕРЕЖЕННЯ ДЛЯ TFLITE")
print("="*50)

# 1. Збереження у SavedModel формат (найкращий для конвертації)
saved_model_path = f"{MODEL_DIR}/best_v3_saved"
model.save(saved_model_path, save_format='tf')
print(f"SavedModel збережено: {saved_model_path}")

# 2. Також зберігаємо у старий h5 формат (про всяк випадок)
model.save(f"{MODEL_DIR}/best_v3.h5")
print("h5 модель також збережена")

# 3. Конвертація відразу після навчання
print("Конвертація в TFLite...")

converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,
    tf.lite.OpsSet.SELECT_TF_OPS
]
converter.allow_custom_ops = True

tflite_model = converter.convert()

tflite_path = f"{MODEL_DIR}/bill_classifier_v3.tflite"
with open(tflite_path, 'wb') as f:
    f.write(tflite_model)

print(f" TFLite модель успішно створена!")
print(f"Шлях: {tflite_path}")
print(f"Розмір: {len(tflite_model)/(1024*1024):.2f} MB")

# === COMPREHENSIVE EVALUATION ===

print("\n" + "="*50)

print("COMPREHENSIVE MODEL EVALUATION")

print("="*50)



# Get predictions on validation set

y_true = []

y_pred = []



for images, labels in val_ds:

    predictions = model.predict(images, verbose=0)

    y_true.extend(labels.numpy())

    y_pred.extend(np.argmax(predictions, axis=1))



y_true = np.array(y_true)

y_pred = np.array(y_pred)



# Calculate metrics

loss, accuracy = model.evaluate(val_ds, verbose=0)

print(f"\nFinal Validation Loss: {loss:.4f}")

print(f"Final Validation Accuracy: {accuracy:.4f}")



# Classification Report

print("\n" + "="*30)

print("CLASSIFICATION REPORT")

print("="*30)

class_names = list(class_map.keys())

report = classification_report(y_true, y_pred, target_names=class_names, digits=4)

print(report)



# Confusion Matrix

print("\n" + "="*30)

print("CONFUSION MATRIX")

print("="*30)

cm = confusion_matrix(y_true, y_pred)



# Plot confusion matrix

plt.figure(figsize=(10, 8))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 

            xticklabels=class_names, yticklabels=class_names)

plt.title('Confusion Matrix')

plt.ylabel('True Label')

plt.xlabel('Predicted Label')

plt.tight_layout()

plt.savefig(f"{MODEL_DIR}/confusion_matrix.png")

plt.show()



# Per-class metrics

print("\n" + "="*30)

print("PER-CLASS METRICS")

print("="*30)

for i, class_name in enumerate(class_names):

    tp = cm[i, i]

    fp = cm[:, i].sum() - tp

    fn = cm[i, :].sum() - tp

    tn = cm.sum() - tp - fp - fn

    

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0

    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    

    print(f"{class_name}:")

    print(f"  Precision: {precision:.4f}")

    print(f"  Recall: {recall:.4f}")

    print(f"  F1-Score: {f1:.4f}")

    print(f"  True Positives: {tp}")

    print(f"  False Positives: {fp}")

    print(f"  False Negatives: {fn}")

    print(f"  True Negatives: {tn}")

    print()



# Save training history to CSV

history_df = pd.DataFrame(history.history)

history_df.to_csv(f"{MODEL_DIR}/training_history.csv", index=False)



# Save model summary

with open(f"{MODEL_DIR}/model_summary.txt", "w", encoding="utf-8") as f:

    f.write("MODEL ARCHITECTURE SUMMARY\n")

    f.write("="*50 + "\n\n")

    model.summary(print_fn=lambda x: f.write(x + "\n"))



# Overfitting check

print("\n" + "="*30)

print("OVERFITTING CHECK")

print("="*30)

print(f"Final Train Accuracy: {history.history['accuracy'][-1]:.4f}")

print(f"Final Val Accuracy: {history.history['val_accuracy'][-1]:.4f}")

print(f"Final Train Loss: {history.history['loss'][-1]:.4f}")

print(f"Final Val Loss: {history.history['val_loss'][-1]:.4f}")



overfitting_gap = history.history['accuracy'][-1] - history.history['val_accuracy'][-1]

print(f"Accuracy Gap (Train-Val): {overfitting_gap:.4f}")

if overfitting_gap > 0.05:

    print("WARNING: Potential overfitting detected!")

else:

    print("GOOD: No significant overfitting detected")



# Loss plot

plt.figure(figsize=(12, 4))



plt.subplot(1, 2, 1)

plt.plot(history.history['accuracy'], label='Train Accuracy')

plt.plot(history.history['val_accuracy'], label='Val Accuracy')

plt.legend()

plt.title('Accuracy')

plt.grid(True)



plt.subplot(1, 2, 2)

plt.plot(history.history['loss'], label='Train Loss')

plt.plot(history.history['val_loss'], label='Val Loss')

plt.legend()

plt.title('Loss')

plt.grid(True)



plt.tight_layout()

plt.savefig(f"{MODEL_DIR}/training_plots.png")

plt.show()



# Save detailed results

with open(f"{MODEL_DIR}/evaluation_results.txt", 'w', encoding='utf-8') as f:

    f.write("COMPREHENSIVE MODEL EVALUATION RESULTS\n")

    f.write("="*50 + "\n\n")

    f.write(f"Final Validation Loss: {loss:.4f}\n")

    f.write(f"Final Validation Accuracy: {accuracy:.4f}\n\n")

    f.write("OVERFITTING ANALYSIS:\n")

    f.write(f"Train Accuracy: {history.history['accuracy'][-1]:.4f}\n")

    f.write(f"Val Accuracy: {history.history['val_accuracy'][-1]:.4f}\n")

    f.write(f"Accuracy Gap: {overfitting_gap:.4f}\n\n")

    f.write("CLASSIFICATION REPORT:\n")

    f.write(report + "\n\n")

    f.write("CONFUSION MATRIX:\n")

    f.write(str(cm) + "\n\n")

    f.write("PER-CLASS METRICS:\n")

    for i, class_name in enumerate(class_names):

        tp = cm[i, i]

        fp = cm[:, i].sum() - tp

        fn = cm[i, :].sum() - tp

        tn = cm.sum() - tp - fp - fn

        

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0

        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        

        f.write(f"{class_name}:\n")

        f.write(f"  Precision: {precision:.4f}\n")

        f.write(f"  Recall: {recall:.4f}\n")

        f.write(f"  F1-Score: {f1:.4f}\n\n")



print(f"\nAll results saved:")

print(f"  Model: {MODEL_DIR}/best_v2.keras")

print(f"  Training History: {MODEL_DIR}/training_history.csv")

print(f"  Model Summary: {MODEL_DIR}/model_summary.txt")

print(f"  Training Plots: {MODEL_DIR}/training_plots.png")

print(f"  Confusion Matrix: {MODEL_DIR}/confusion_matrix.png")

print(f"  Evaluation Results: {MODEL_DIR}/evaluation_results.txt")

print("="*50)