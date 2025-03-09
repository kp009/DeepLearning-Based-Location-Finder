import os
import numpy as np
import cv2
from keras._tf_keras.keras.applications import MobileNetV2
from keras._tf_keras.keras.models import Model
from keras._tf_keras.keras.layers import Dense, GlobalAveragePooling2D
from keras._tf_keras.keras.utils import to_categorical
 
def load_data(data_dir):
    images = []
    labels = []
    for label in os.listdir(data_dir):
        label_folder = os.path.join(data_dir, label)
        for filename in os.listdir(label_folder):
            img = cv2.imread(os.path.join(label_folder, filename))
            if img is not None:
                img = cv2.resize(img, (224, 224)) / 255.0
                images.append(img)
                labels.append(label)
    return np.array(images), np.array(labels)

train_path = os.path.abspath(os.path.join(os.getcwd(), "dataset\\train"))  # Uses the current directory
test_path = os.path.abspath(os.path.join(os.getcwd(), "dataset\\test")) # Uses the current directory
# Load data
train_images, train_labels = load_data(train_path)
val_images, val_labels = load_data(test_path)
 
# Create a label mapping
label_mapping = {label: idx for idx, label in enumerate(set(train_labels))}
train_labels = np.array([label_mapping[label] for label in train_labels])
val_labels = np.array([label_mapping[label] for label in val_labels])
 
# Convert to categorical
num_classes = len(label_mapping)
train_labels = to_categorical(train_labels, num_classes)
val_labels = to_categorical(val_labels, num_classes)
# Build the model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)
# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
 
# Train the model
model.fit(train_images, train_labels, validation_data=(val_images, val_labels), epochs=10, batch_size=32)
 
# Save the model
model.save('location_identifier_model.keras')
 
 
 