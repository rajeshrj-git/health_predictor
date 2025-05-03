import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib

def train_model():
    # Load processed data
    data = pd.read_csv('data/combined_data.csv')
    
    # Select features and targets
    features = data[[
        'age', 'BMI', 'heartRate', 
        'trestbps', 'glucose', 'cholesterol',
        'currentSmoker', 'prevalentHyp'
    ]]
    
    targets = data[['heart_disease', 'diabetes', 'metabolic_risk']]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )
    
    # Build model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(8,)),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(3, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[EarlyStopping(patience=3)]
    )
    
    # Save model
    model.save('models/health_model.h5')
    joblib.dump(features.columns.tolist(), 'models/feature_columns.pkl')
    print("Model trained and saved!")

if __name__ == '__main__':
    train_model()