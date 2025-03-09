# Location Finder

## 📌 Project Overview
This project is a **Deep Learning-based Location Finder** that extracts location names from uploaded images, converts them to geographical coordinates, and calculates distances and travel costs.

## 🚀 Features
- **Upload Images**: Users can upload images containing location names.
- **Location Extraction**: A deep learning model extracts the location name.
- **Geolocation Lookup**: Converts extracted names into latitude and longitude.
- **Distance Calculation**: Computes distance from a base location (Washington, D.C.).
- **Cost Calculation**: Calculates transportation cost ($0.10 per mile).
- **CRUD Operations**: Edit and delete location data.
- **Pagination Support**: Manage large datasets efficiently.

## 🛠️ Tech Stack
### **Backend (Django & Deep Learning)**
- **Django & Django REST Framework**: API for handling image uploads and geolocation.
- **TensorFlow/PyTorch**: Deep learning model for location name extraction.
- **MySQL**: Database for storing extracted metadata.
- **Geopy API**: Converts extracted locations to coordinates.
- **OpenWeather API (Optional)**: For additional location-based data.

### **Frontend (React)**
- **React.js**: User interface for uploading images and viewing extracted data.
- **Axios**: Handles API requests.

## 🏗️ Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/location-finder.git
cd location-finder
```

### 2️⃣ **Backend Setup (Django)**
```sh
cd backend
python -m venv env  # Create virtual environment
source env/bin/activate  # (Mac/Linux) OR `env\Scripts\activate` (Windows)
pip install -r requirements.txt  # Install dependencies
```

#### **Run Migrations & Start Server**
```sh
python manage.py migrate
python manage.py runserver
```

### 3️⃣ **Frontend Setup (React)**
```sh
cd frontend
npm install  # Install dependencies
npm start  # Start React app
```

## 🌍 API Endpoints
### **1. Upload Image**
```http
POST /api/images/predict/
```
- **Request:** Multipart form-data with an image file.
- **Response:** `{ "id": 1, "location": "Eiffel Tower", "latitude": 48.8584, "longitude": 2.2945 }`

### **2. Get Location Distance & Cost**
```http
GET /api/distance/{latitude}/{longitude}/
```
- **Response:** `{ "distance": 200, "cost": 20.0 }`

### **3. Update Location**
```http
PUT /api/images/update/{id}/
```
- **Request:** `{ "location": "New Name", "latitude": 40.7128, "longitude": -74.0060 }`

### **4. Delete Location**
```http
DELETE /api/images/delete/{id}/
```

## 🔥 Troubleshooting
### **Common Issues & Fixes**
**1. OSError: [WinError 123] Filename or Directory Syntax Error**  
✅ **Solution**: Ensure the model path is correct.
```python
import os
file_path = os.path.abspath(os.path.join(os.getcwd(), "..", "location_identifier_model.keras"))
```

**2. API Returning `null/null` in URL**  
✅ **Solution**: Ensure latitude & longitude are passed correctly from React.
```js
const fetchDistance = async (lat, lon) => {
    const response = await axios.get(`http://localhost:8000/api/distance/${lat}/${lon}/`);
    return response.data;
};
```

## 🤝 Contributing
Feel free to fork the repository and submit **Pull Requests** for new features or bug fixes.

## 📜 License
This project is licensed under the **MIT License**.
