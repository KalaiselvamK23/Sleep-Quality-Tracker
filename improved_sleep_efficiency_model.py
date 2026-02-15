from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

data = df.copy()

# 1. Encode Categorical Variables
le = LabelEncoder()
data['Smoking status_encoded'] = le.fit_transform(data['Smoking status'])
data['Gender_encoded'] = le.fit_transform(data['Gender'])

# Drop original categorical and time columns
data.drop(['Smoking status', 'Gender', 'Bedtime', 'Wakeup time'], axis=1, inplace=True)

# 2. Split Features and Target
feature_columns = [
    'Age', 'Gender_encoded', 'REM sleep percentage', 'Deep sleep percentage',
    'Light sleep percentage', 'Awakenings', 'Smoking status_encoded',
    'Caffeine consumption', 'Alcohol consumption', 'Exercise frequency'
]
X = data[feature_columns]
y = data['Sleep efficiency']

# 3. Impute & Scale
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

train_x, test_x, train_y, test_y = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
train_x_scaled = scaler.fit_transform(train_x)
test_x_scaled = scaler.transform(test_x)

# 4. Train and Evaluate Multiple Models
models = {
    'Linear Regression': LinearRegression(),
    'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=5),
    'Support Vector Machine': SVR(kernel='rbf'),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}

for model_name, model in models.items():
    model.fit(train_x_scaled, train_y)
    train_pred = model.predict(train_x_scaled)
    test_pred = model.predict(test_x_scaled)
    
    train_r2 = r2_score(train_y, train_pred)
    test_r2 = r2_score(test_y, test_pred)
    test_rmse = mean_squared_error(test_y, test_pred, squared=False)
    test_mae = mean_absolute_error(test_y, test_pred)
    
    results[model_name] = {
        'Train R²': train_r2,
        'Test R²': test_r2,
        'Test RMSE': test_rmse,
        'Test MAE': test_mae
    }
    
    print(f"\n{model_name}:")
    print(f"  Train R² Score: {train_r2:.4f}")
    print(f"  Test R² Score: {test_r2:.4f}")
    print(f"  Test RMSE: {test_rmse:.4f}")
    print(f"  Test MAE: {test_mae:.4f}")

# 5. Select and Use Best Model
results_df = pd.DataFrame(results).T
print("\n" + "="*60)
print("Model Comparison Summary:")
print(results_df)

best_model_name = results_df['Test R²'].idxmax()
print(f"\nBest Model: {best_model_name}")

final_model = models[best_model_name]
final_model.fit(train_x_scaled, train_y)

# 6. Feature Importance (if available)
if hasattr(final_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': final_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 5 Most Important Features:")
    print(feature_importance.head())

print("\nModel Training Complete.")