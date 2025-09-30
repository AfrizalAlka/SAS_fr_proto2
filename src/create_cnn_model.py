from sklearn.calibration import LabelEncoder
import tensorflow as tf
from tensorflow import Sequential
from tensorflow import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

def create_cnn_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dropout(0.5),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    return model

def train_model():
    # Load preprocessed data
    X = np.load('data/training_data/X_train.npy')
    y = np.load('data/training_data/y_train.npy')

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create CNN model
    num_classes=len(np.unique(y))
    model = create_cnn_model(input_shape=X.shape[1:], num_classes=num_classes)

    # Compile model
    model.compile(optimizer=Adam(learning_rate=0.001), 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])

    print("Model Summary:")
    model.summary()

    # Train model
    history = model.fit(X_train, 
                        y_train, 
                        validation_data=(X_val, y_val), 
                        epochs=50, 
                        batch_size=32,
                        verbose=1)

    # Save model
    model.save('data/models/face_recognition_model.h5')

    # Save label encoder
    with open('data/models/label_encoder.pkl', 'wb') as f:
        pickle.dump(LabelEncoder(), f)

    print("Model saved successfully!")

    return model, history

if __name__ == "__main__":
    train_model()