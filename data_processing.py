import pandas as pd
import os

def load_and_combine():
    # Verify files exist
    required_files = [
        'data/heart.csv',
        'data/cholesterol.xls',
        'data/diabetes.xls'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("Error: Missing files:")
        for f in missing_files:
            print(f"- {f}")
        return None

    try:
        print("Loading datasets...")
        
        # Load datasets with correct separators
        heart = pd.read_csv('data/heart.csv', sep='\t')
        cholesterol = pd.read_csv('data/cholesterol.xls', sep='\t')
        diabetes = pd.read_csv('data/diabetes.xls', sep='\t')

        print(f"Heart columns: {list(heart.columns)}")
        print(f"Cholesterol columns: {list(cholesterol.columns)}")
        print(f"Diabetes columns: {list(diabetes.columns)}")

        # Standardize column names
        cholesterol.rename(columns={
            'num': 'heart_disease', 
            'chol': 'cholesterol',
            'sex': 'gender'
        }, inplace=True)

        diabetes.rename(columns={
            'Outcome': 'diabetes',
            'BloodPressure': 'bp',
            'Glucose': 'glucose',
            'Age': 'age',
            'BMI': 'diabetes_BMI'  # Rename to avoid conflict
        }, inplace=True)

        # Create common ID
        heart['id'] = heart['age'].astype(str) + '_' + heart['currentSmoker'].astype(str)
        cholesterol['id'] = cholesterol['age'].astype(str) + '_' + cholesterol['gender'].astype(str)
        diabetes['id'] = diabetes['age'].astype(str) + '_' + diabetes['Pregnancies'].astype(str)

        # First merge - heart and cholesterol
        print("Merging heart and cholesterol...")
        merged_hc = pd.merge(
            heart,
            cholesterol,
            on='id',
            how='outer',
            suffixes=('_heart', '_chol')
        )

        # Second merge - with diabetes
        print("Merging with diabetes...")
        combined = pd.merge(
            merged_hc,
            diabetes,
            on='id',
            how='outer'
        )

        # Create unified BMI column (priority: heart > diabetes)
        combined['BMI'] = combined['BMI'].fillna(combined['diabetes_BMI'])
        
        # Feature engineering using unified BMI
        combined['metabolic_risk'] = (
            (combined['BMI'].fillna(0) > 30) |
            (combined['glucose'].fillna(0) > 100) |
            (combined['trestbps'].fillna(0) > 130)
        ).astype(int)

        # Fill missing values
        numeric_cols = combined.select_dtypes(include=['number']).columns
        combined[numeric_cols] = combined[numeric_cols].fillna(combined[numeric_cols].median())

        # Clean up - drop temporary columns
        columns_to_drop = ['diabetes_BMI']
        combined.drop([col for col in columns_to_drop if col in combined.columns], 
                     axis=1, inplace=True)

        # Save processed data
        combined.to_csv('data/combined_data.csv', index=False)
        print("\nData processing completed successfully!")
        print(f"Final dataset shape: {combined.shape}")
        print("\nFirst 3 rows of combined data:")
        print(combined.head(3))
        return combined

    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        print("\nDebug Info:")
        try:
            print(f"Heart data sample:\n{heart.head()}")
        except:
            pass
        try:
            print(f"\nCholesterol data sample:\n{cholesterol.head()}")
        except:
            pass
        try:
            print(f"\nDiabetes data sample:\n{diabetes.head()}")
        except:
            pass
        return None

if __name__ == '__main__':
    result = load_and_combine()