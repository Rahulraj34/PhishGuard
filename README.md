# PhishGuard
 🛡️ PhishGuard: Real-Time URL Classification Using Flask and Machine Learning  

PhishGuard is an intelligent **web-based phishing detection system** built using **Flask** and **Machine Learning (Random Forest)**.  
It analyzes website URLs in real-time and classifies them as **Safe** or **Phishing**, helping users stay protected from malicious websites.  

 Project Overview  
PhishGuard provides an interactive web interface where users can enter any website URL.  
The system extracts lexical features from the URL and uses a pre-trained Random Forest model to predict whether the site is **phishing** or **legitimate**.  

It combines **cybersecurity awareness** with **AI-powered detection**, making it ideal for both learning and professional portfolio projects.  

 Features  
✅ Real-time phishing URL detection  
✅ Trained Machine Learning model (`rf_phishing_model.joblib`)  
✅ Stylish dark UI with cyber-detection effects  
✅ Fast and lightweight Flask web server  
✅ Supports multiple URL inputs at once  

 🧠 Tech Stack  
- Frontend: HTML, CSS, JavaScript  
- Backend: Python (Flask)  
- ML Model: RandomForestClassifier (scikit-learn)  
- Dataset: Kaggle Phishing Websites + Tranco Safe URLs  

Model Details:

Algorithm: Random Forest Classifier

Trained using phishing and safe URL datasets from Kaggle and Tranco

Extracted lexical-based features:

URL Length

Number of Dots & Hyphens

Suspicious Keywords (login, secure, verify, etc.)

Use of HTTPS and IPs in domain

Output:

0 → Safe

1 → Phishing
