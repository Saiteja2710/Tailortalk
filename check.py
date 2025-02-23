from fastapi import FastAPI
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from pydantic import BaseModel

# Load Titanic dataset
df = pd.read_csv("Titanic-Dataset.csv")

app = FastAPI()

# Pydantic model for request
class QueryRequest(BaseModel):
    question: str

# Function to generate base64 images from plots
def generate_plot(plot_func, *args, **kwargs):
    plt.figure(figsize=(6, 4))
    plot_func(*args, **kwargs)
    plt.xlabel(kwargs.get("x", ""))
    plt.ylabel(kwargs.get("y", ""))
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

@app.post("/query")
def query_data(request: QueryRequest):
    question = request.question.lower()

    if "percentage of passengers were male" in question:
        male_percentage = (df["Sex"].value_counts(normalize=True).get("male", 0) * 100)
        return {"answer": f"{male_percentage:.2f}% of passengers were male."}

    elif "percentage of passengers were female" in question:
        female_percentage = (df["Sex"].value_counts(normalize=True).get("female", 0) * 100)
        return {"answer": f"{female_percentage:.2f}% of passengers were female."}

    elif "histogram of passenger ages" in question:
        img_base64 = generate_plot(sns.histplot, df["Age"].dropna(), bins=20, kde=True)
        return {"answer": "Here is the age distribution:", "image": img_base64}

    elif "average age of passengers" in question:
        avg_age = df["Age"].mean()
        return {"answer": f"The average age of passengers was {avg_age:.2f} years."}

    elif "average ticket fare" in question:
        avg_fare = df["Fare"].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}."}
    elif "percentage of passengers were male" in question:
        male_percentage = (df["Sex"].value_counts(normalize=True).get("male", 0) * 100)
        return {"answer": f"{male_percentage:.2f}% of passengers were male."}

    elif "highest ticket fare" in question:
        max_fare = df["Fare"].max()
        return {"answer": f"The highest ticket fare was ${max_fare:.2f}."}

    elif "lowest ticket fare" in question:
        min_fare = df["Fare"].min()
        return {"answer": f"The lowest ticket fare was ${min_fare:.2f}."}

    elif "passengers embarked from each port" in question:
        img_base64 = generate_plot(sns.countplot, x=df["Embarked"].dropna())
        return {"answer": "Here is the count of passengers from each port:", "image": img_base64}

    elif "number of survivors" in question:
        survivors = df[df["Survived"] == 1].shape[0]
        return {"answer": f"There were {survivors} survivors."}

    elif "number of non-survivors" in question:
        non_survivors = df[df["Survived"] == 0].shape[0]
        return {"answer": f"There were {non_survivors} non-survivors."}

    elif "survival rate by class" in question:
        survival_by_class = df.groupby("Pclass")["Survived"].mean() * 100
        return {"answer": f"Survival rate by class:\n{survival_by_class.to_string()}."}

    elif "number of passengers in each class" in question:
        class_counts = df["Pclass"].value_counts()
        return {"answer": f"Passenger count per class:\n{class_counts.to_string()}."}

    elif "gender-based survival rate" in question:
        gender_survival = df.groupby("Sex")["Survived"].mean() * 100
        return {"answer": f"Survival rate by gender:\n{gender_survival.to_string()}."}

    else:
        return {"answer": "Sorry, I don't have an answer for that. Try asking about passenger stats, fares, survival rates, or embarkation details."}
