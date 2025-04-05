import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Load JSON from file
df = pd.read_json("participation.json")

# Drop text-based identifiers (optional)
df = df.drop(columns=["name", "title", "description"], errors="ignore")

# Target
y = df["participating"]
X = df.drop(columns=["participating"])

# Define feature types
categorical = ["nsfw", "ad_friendly", "removed_content_fraction",
               "user_social_capital", "economic_capital", "cultural_capital"]
numeric = ["subscribers", "active_users", "subreddit_age", "comments_per_moderator"]

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first'), categorical)
], remainder='passthrough')

# Choose model (Random Forest for better feature importances)
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train the model
model.fit(X, y)

# Extract feature names and importances
importances = model.named_steps['classifier'].feature_importances_
feature_names = model.named_steps['preprocessor'].get_feature_names_out()
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values(by='importance', ascending=False)

print(importance_df)
