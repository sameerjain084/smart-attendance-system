# 📸 Smart Attendance System Using Face Recognition

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Face%20Recognition-red.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent, contactless attendance tracking system that leverages real-time facial recognition technology to automate the attendance process.

---

## 🌟 Overview
The **Smart Attendance System** is a modern Flask-based web application designed to eliminate manual attendance processes. It provides accurate, contactless student monitoring using advanced face recognition algorithms. The system includes dual dashboards for students and faculty, offering real-time insights, analytics, and comprehensive reporting.

## ✨ Key Features
- **👤 Face Registration & Recognition:** Securely register students with facial data and mark attendance automatically upon detection.
- **👥 Dual Dashboard System:** Tailored, interactive interfaces for both faculty and students.
- **⏱️ Real-time Tracking:** Live attendance marking with instant visual feedback.
- **📊 Analytics & Reporting:** Comprehensive attendance reports, charts, and downloadable analytics.
- **🔒 Secure Authentication:** Role-based access control and secure user sessions.
- **📱 Responsive Design:** Modern, sleek interface accessible on desktops, tablets, and smartphones.

---

## 🛠️ Technologies Used

### Backend
- **Core:** Python
- **Framework:** Flask
- **Database:** SQLite (with robust thread-safe connection handling)

### AI & Computer Vision
- **Face Detection/Recognition:** OpenCV, `face_recognition` library
- **Data Processing:** NumPy, Pandas

### Frontend
- **Structure & Style:** HTML5, CSS3, Bootstrap 5
- **Interactivity:** JavaScript, AJAX

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your system
- CMake (Required for `dlib` installation used by `face_recognition`)
- A webcam for live attendance capturing

### Step-by-Step Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/sameerjain084/smart-attendance-system.git
   cd smart-attendance-system
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the application**
   Run the application, which will automatically initialize the database and load the ML models.
   ```bash
   python app.py
   ```

5. **Access the Application**
   Open your browser and navigate to:
   ```text
   http://localhost:5001
   ```

---

## 💻 Usage

1. **Faculty/Admin Login:** Log in as an administrator to manage students, view holistic reports, and start the live attendance session.
2. **Student Registration:** Add new students through the admin panel, providing their details and capturing their face data.
3. **Mark Attendance:** Navigate to the "Take Attendance" section to open the live camera feed. Registered faces will be recognized and marked as "Present".
4. **Student Dashboard:** Students can log in to view their personal attendance records and statistics.

---

## 📁 Project Structure

```text
smart-attendance-system/
├── app.py                      # Main Flask application
├── database.py                 # Database initialization and operations
├── my_face_utils.py            # Face recognition logic and utility functions
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── index.html              # Login/Landing page
│   ├── student_dashboard.html  # Student interface
│   ├── faculty_dashboard.html  # Admin/Faculty interface
│   └── ...
├── static/                     # CSS, JavaScript, and static assets
│   ├── style.css               # Main stylesheet
│   └── ...
└── README.md                   # Project documentation
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to check out the [issues page](https://github.com/sameerjain084/smart-attendance-system/issues) if you want to contribute.

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).