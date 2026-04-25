# Smart Expense Predictor

A complete beginner-friendly Machine Learning project to predict daily expenses using Python and Linear Regression.

## 📂 Project Structure

- `expense_predictor.py`: The core Machine Learning script. It does the data generation, analysis, visualization, model training, predicting, and saving the model.
- `app.py`: A simple Streamlit App providing a User Interface on top of your trained model.
- `expenses.csv`: The dataset generated automatically.
- `expense_model.pkl`: The saved ML model.

## 🚀 How to Run the Project

### 1. Install Requirements
Open your terminal inside the project directory and install the necessary libraries:
```bash
pip install pandas numpy matplotlib scikit-learn streamlit
```

### 2. Run the Main Script (Command Line)
Execute the Python script to see the analysis, train the model, and do predictions:
```bash
python expense_predictor.py
```
**What will happen?**
- It will print dataset statistics and the prediction for day 30.
- It will generate two images: `scatter_plot.png` & `regression_plot.png` so you can visually verify the training data.
- It saves out the model to `expense_model.pkl`.

### 3. Run the Interactive Web App (Bonus UI!)
Now let's see the application in a nice UI where you can tweak inputs:
```bash
streamlit run app.py
```
A new browser window will open magically with your interactive app! From the sidebar, you can enter any arbitrary day and see it predict the future expense based on the trained model.
