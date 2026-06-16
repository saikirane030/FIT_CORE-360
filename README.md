# 💪 FitCore 360 — Streamlit Health & Fitness App

## 📁 Project Structure
```
fitcore360/
├── app.py                  ← Main entry point (run this)
├── requirements.txt        ← All Python packages
├── README.md               ← This file
├── pages/
│   ├── __init__.py
│   ├── home.py             ← Home/landing page
│   ├── profile.py          ← User profile (saved to SQLite)
│   ├── bmi.py              ← BMI Calculator with gauge chart
│   ├── nutrition.py        ← Meal logger + planner (CSV food DB)
│   ├── analytics.py        ← Charts: weight, calories, macros
│   └── gym_map.py          ← Interactive Folium gym map
├── database/
│   ├── __init__.py
│   ├── db_setup.py         ← SQLite setup & all DB functions
│   └── fitcore360.db       ← Auto-created when you run the app
└── data/
    ├── food_database.csv   ← 35+ Indian food items with nutrition
    └── gyms.csv            ← 12 gyms across Indian cities
```

---

## 🚀 How to Run (Step by Step)

### Step 1 — Open VS Code
Open VS Code and open the `fitcore360` folder.

### Step 2 — Open Terminal
Press `Ctrl + `` ` `` ` to open the terminal inside VS Code.

### Step 3 — Install packages
```bash
pip install -r requirements.txt
```
Wait for all packages to install (takes 1-2 minutes).

### Step 4 — Run the app
```bash
streamlit run app.py
```

### Step 5 — Open in browser
Your browser will open automatically at:
```
http://localhost:8501
```

---

## 🧭 How to Use

1. **Profile Setup** → Create your profile first (saved to SQLite DB)
2. **BMI Calculator** → Enter weight & height to calculate BMI
3. **Nutrition Planner** → Log meals from the food database
4. **Analytics** → See charts of your weight & calorie history
5. **Gym Finder** → Find gyms on the map, filter by city & type

---

## 🛠️ Tech Stack
| Technology | Use |
|---|---|
| Streamlit | Frontend web dashboard |
| SQLite | Store user profiles & diet history |
| Pandas | Read CSV food database |
| Plotly | Interactive charts & BMI gauge |
| Folium | Interactive gym map |
| Python | All backend logic |

---

## ❓ Troubleshooting

**ModuleNotFoundError** → Run `pip install -r requirements.txt` again

**Port already in use** → Run `streamlit run app.py --server.port 8502`

**streamlit not found** → Run `pip install streamlit` first
