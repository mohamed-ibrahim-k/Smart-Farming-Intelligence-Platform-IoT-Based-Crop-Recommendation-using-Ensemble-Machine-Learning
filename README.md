# 🌱 Smart Farming Intelligence Platform

### IoT-Based Crop Recommendation Using Ensemble Machine Learning

An end-to-end **precision agriculture platform** that combines real-time soil sensing, IoT communication, cloud services, weather APIs, edge computing, and ensemble machine learning to recommend the most suitable crop based on actual field conditions.

The system integrates an industrial **7-in-1 soil sensor**, **ESP32**, **ThingSpeak Cloud**, **Raspberry Pi**, live weather services, and an ensemble of **CatBoost, XGBoost, LightGBM, and Gradient Boosting** models to deliver intelligent, data-driven crop recommendations.

---

## 📌 Table of Contents

* [Overview](#-overview)
* [Key Features](#-key-features)
* [System Architecture](#-system-architecture)
* [How It Works](#-how-it-works)
* [Hardware Components](#-hardware-components)
* [Machine Learning Pipeline](#-machine-learning-pipeline)
* [Ensemble Model](#-ensemble-model)
* [Input Features](#-input-features)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [Configuration](#-configuration)
* [Running the Project](#-running-the-project)
* [Challenges and Solutions](#-challenges-and-solutions)
* [Future Improvements](#-future-improvements)
* [Contributors](#-contributors)
* [License](#-license)

---

## 🔍 Overview

Traditional crop selection often depends heavily on farmer experience and manual observation. However, rapidly changing soil conditions, unpredictable weather, improper irrigation, and inefficient fertilizer usage can significantly affect agricultural productivity.

This project addresses these challenges by developing a complete **IoT-enabled Smart Farming Intelligence Platform** capable of:

* Collecting real-time soil measurements.
* Monitoring environmental conditions.
* Retrieving dynamic weather and rainfall data.
* Processing sensor and API data at the edge.
* Running ensemble machine learning inference.
* Recommending the most suitable crop for current field conditions.

Unlike traditional crop recommendation systems that rely exclusively on historical datasets, this platform combines **live field measurements with external environmental data** to provide context-aware recommendations.

---

## ✨ Key Features

* 🌱 **Real-Time Soil Monitoring** — Collects live nitrogen, phosphorus, potassium, pH, moisture, temperature, and electrical conductivity measurements.

* 📡 **Industrial Sensor Communication** — Uses RS485 and MODBUS communication through a MAX485 TTL converter.

* ⚡ **ESP32-Based Data Acquisition** — Reads sensor measurements and uploads them to the cloud through Wi-Fi.

* ☁️ **Cloud IoT Integration** — Uses ThingSpeak for real-time sensor storage, monitoring, visualization, and API-based retrieval.

* 🌦️ **Dynamic Weather Integration** — Retrieves live temperature and humidity information through OpenWeather.

* 🌧️ **Historical Rainfall Intelligence** — Uses NASA POWER data for location-specific rainfall information.

* 📍 **Automatic Location Detection** — Supports dynamic geographic coordinate detection for flexible deployment.

* 🧠 **Ensemble Machine Learning** — Combines multiple boosting algorithms for improved prediction robustness.

* 🍚 **Real-Time Crop Recommendation** — Generates crop recommendations using current soil and environmental conditions.

* 🖥️ **Edge AI Deployment** — Executes machine learning inference locally on Raspberry Pi.

---

## 🏗️ System Architecture

```text
┌─────────────────────────┐
│    7-in-1 Soil Sensor   │
│ N │ P │ K │ pH │ EC │  │
│ Moisture │ Temperature  │
└────────────┬────────────┘
             │
             │ RS485 / MODBUS
             ▼
┌─────────────────────────┐
│    MAX485 Converter     │
└────────────┬────────────┘
             │
             │ UART
             ▼
┌─────────────────────────┐
│          ESP32          │
│   Sensor Acquisition    │
│   Wi-Fi Communication   │
└────────────┬────────────┘
             │
             │ HTTP / REST API
             ▼
┌─────────────────────────┐
│     ThingSpeak Cloud    │
│   Storage & Monitoring  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Raspberry Pi       │
│     Edge AI Device      │
└────────────┬────────────┘
             │
       ┌─────┴─────┐
       ▼           ▼
┌────────────┐ ┌────────────┐
│OpenWeather │ │ NASA POWER │
│    API     │ │    API     │
└──────┬─────┘ └──────┬─────┘
       │                │
       └────────┬───────┘
                ▼
┌─────────────────────────┐
│   Feature Engineering   │
│  N • P • K • pH         │
│  Temp • Humidity • Rain │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│   Ensemble ML Pipeline  │
│                         │
│ CatBoost  │  XGBoost    │
│ LightGBM  │  Gradient   │
│           │  Boosting   │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│   🌾 Crop Recommendation │
└─────────────────────────┘
```

---

## ⚙️ How It Works

The complete data pipeline follows these steps:

1. The **7-in-1 industrial soil sensor** measures live soil parameters.

2. Sensor data is transmitted through **RS485 using the MODBUS protocol**.

3. A **MAX485 converter** enables communication between the RS485 sensor and ESP32.

4. The **ESP32** reads and parses the sensor data.

5. Sensor measurements are uploaded to **ThingSpeak Cloud** over Wi-Fi.

6. The **Raspberry Pi** retrieves the latest soil readings from ThingSpeak.

7. Geographic coordinates are automatically determined through an IP geolocation service.

8. **OpenWeather API** provides current temperature and humidity.

9. **NASA POWER API** provides location-specific historical rainfall data.

10. The collected information is processed through the feature-engineering pipeline.

11. The ensemble machine learning model analyzes seven primary input features.

12. The system generates the recommended crop for the current field conditions.

---

## 🔌 Hardware Components

| Component              | Purpose                                                   |
| ---------------------- | --------------------------------------------------------- |
| **7-in-1 Soil Sensor** | Measures N, P, K, pH, moisture, soil temperature, and EC  |
| **MAX485 Converter**   | Converts RS485 communication to TTL                       |
| **ESP32**              | Reads sensor values and uploads them to ThingSpeak        |
| **Raspberry Pi**       | Performs API integration, preprocessing, and ML inference |

### Soil Parameters Monitored

| Parameter               | Description                                    |
| ----------------------- | ---------------------------------------------- |
| Nitrogen (N)            | Essential macronutrient for plant growth       |
| Phosphorus (P)          | Supports root development and energy transfer  |
| Potassium (K)           | Improves plant strength and disease resistance |
| pH                      | Indicates soil acidity or alkalinity           |
| Moisture                | Measures soil water content                    |
| Temperature             | Measures soil temperature                      |
| Electrical Conductivity | Indicates soluble salt concentration           |

---

## 🤖 Machine Learning Pipeline

```text
                    ┌───────────────────┐
                    │  Training Dataset │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │   Data Cleaning   │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ Feature Selection │
                    │  & Engineering    │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ Feature Scaling   │
                    │  StandardScaler   │
                    └─────────┬─────────┘
                              ▼
               ┌──────────────┴──────────────┐
               ▼                             ▼
       ┌───────────────┐             ┌───────────────┐
       │ Training Data │             │  Testing Data │
       └───────┬───────┘             └───────────────┘
               ▼
    ┌──────────────────────────────┐
    │      Ensemble Training       │
    │                              │
    │  CatBoost     │  XGBoost     │
    │  LightGBM     │  Gradient    │
    │               │  Boosting    │
    └──────────────┬───────────────┘
                   ▼
    ┌──────────────────────────────┐
    │   Soft Voting / Stacking     │
    │ Logistic Regression Meta-ML  │
    └──────────────┬───────────────┘
                   ▼
    ┌──────────────────────────────┐
    │ Cross-Validation & Evaluation│
    └──────────────┬───────────────┘
                   ▼
    ┌──────────────────────────────┐
    │    Serialized ML Model       │
    │        Joblib / PKL          │
    └──────────────┬───────────────┘
                   ▼
    ┌──────────────────────────────┐
    │ Raspberry Pi Edge Inference │
    └──────────────┬───────────────┘
                   ▼
              🌾 Recommended Crop
```

---

## 🧠 Ensemble Model

Instead of relying on a single machine learning classifier, this project combines four powerful boosting algorithms:

| Model                 | Role                                                      |
| --------------------- | --------------------------------------------------------- |
| **CatBoost**          | Gradient boosting with strong generalization capabilities |
| **XGBoost**           | Highly optimized gradient boosting algorithm              |
| **LightGBM**          | Fast and efficient tree-based boosting                    |
| **Gradient Boosting** | Sequential ensemble learning for classification           |

Final predictions are generated using:

* **Soft Voting** — Combines class probabilities produced by individual models.
* **Stacking** — Uses Logistic Regression as a meta-learner to combine predictions from base models.

This ensemble architecture improves robustness compared with relying on a single classifier.

---

## 📊 Input Features

The final machine learning model receives seven primary features:

| Feature     | Source          |
| ----------- | --------------- |
| Nitrogen    | Soil Sensor     |
| Phosphorus  | Soil Sensor     |
| Potassium   | Soil Sensor     |
| pH          | Soil Sensor     |
| Temperature | OpenWeather API |
| Humidity    | OpenWeather API |
| Rainfall    | NASA POWER API  |

### Output

```text
Recommended Crop → Rice / Cotton / Maize / Wheat / Jute / ...
```

---

## 🛠️ Technology Stack

### Artificial Intelligence & Machine Learning

![Python](https://img.shields.io/badge/Python-Machine%20Learning-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Ensemble-red)
![LightGBM](https://img.shields.io/badge/LightGBM-Boosting-green)
![CatBoost](https://img.shields.io/badge/CatBoost-ML-yellow)

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* LightGBM
* CatBoost
* Joblib

### IoT & Embedded Systems

![ESP32](https://img.shields.io/badge/ESP32-IoT-black)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Edge%20AI-red)

* ESP32
* Raspberry Pi
* RS485
* MAX485
* MODBUS
* UART

### Cloud & APIs

* ThingSpeak
* OpenWeather API
* NASA POWER API
* IP Geolocation API
* REST APIs
* HTTP
* JSON

---

## 📂 Project Structure

```text
Smart-Farming-Intelligence-Platform/
│
├── Hardware/
│   ├── ESP32/
│   │   └── sensor_data_acquisition.ino
│   │
│   └── Sensor_Documentation/
│
├── Software/
│   ├── Model/
│   │   ├── crop_model_all.pkl
│   │   ├── train_model.py
│   │   └── preprocessing.py
│   │
│   ├── Raspberry_Pi/
│   │   ├── main.py
│   │   ├── weather_api.py
│   │   ├── rainfall_api.py
│   │   └── crop_prediction.py
│   │
│   └── Dataset/
│
├── Documentation/
│   ├── Project_Report.pdf
│   └── Architecture/
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

> **Note:** Update the project structure above to exactly match the actual folders and filenames in your repository.

---

## 🚀 Installation

### Prerequisites

Ensure the following are installed:

* Python 3.9 or later
* Git
* Required Python packages
* ESP32 development environment, if modifying embedded firmware
* Raspberry Pi OS, for edge deployment

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd Smart-Farming-Intelligence-Platform
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Raspberry Pi**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Never hardcode API keys, Wi-Fi credentials, passwords, or access tokens directly into source files.

Create a `.env` file:

```env
THINGSPEAK_CHANNEL_ID=your_channel_id
THINGSPEAK_READ_API_KEY=your_read_api_key
THINGSPEAK_WRITE_API_KEY=your_write_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

Add the following to `.gitignore`:

```gitignore
.env
*.env
__pycache__/
*.pyc
venv/
.venv/
```

---

## ▶️ Running the Project

### Run ML Inference

```bash
python main.py
```

The application performs the following operations:

```text
Retrieve Soil Data
        ↓
Determine Location
        ↓
Fetch Weather Data
        ↓
Fetch Rainfall Data
        ↓
Feature Engineering
        ↓
Load Ensemble Model
        ↓
Generate Crop Recommendation
```

Example output:

```text
========================================
     SMART FARMING INTELLIGENCE SYSTEM
========================================

Soil Data:
Nitrogen    : 90 mg/kg
Phosphorus  : 42 mg/kg
Potassium   : 43 mg/kg
pH          : 6.5

Environmental Data:
Temperature : 25.8 °C
Humidity    : 81.2 %
Rainfall    : 202.9 mm

----------------------------------------
Recommended Crop: RICE
----------------------------------------
```

---

## 🧩 Challenges and Solutions

| Challenge                        | Solution                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| Reading industrial RS485 sensors | Integrated MAX485 converter with MODBUS communication                              |
| Hardware-cloud communication     | Connected ESP32 to ThingSpeak through Wi-Fi and REST APIs                          |
| Dynamic environmental data       | Integrated OpenWeather and NASA POWER APIs                                         |
| Location-independent deployment  | Added automatic geographic coordinate detection                                    |
| Single-model limitations         | Developed an ensemble of four boosting algorithms                                  |
| Edge deployment                  | Serialized the trained model and deployed inference on Raspberry Pi                |
| Multi-system integration         | Designed modular Python components for sensors, APIs, preprocessing, and inference |

---

## 📈 Project Impact

* **7** live soil and environmental features used for prediction.
* **4** boosting algorithms combined into an ensemble architecture.
* **3** external services integrated into the complete pipeline.
* End-to-end **IoT → Cloud → Edge AI → Crop Recommendation** workflow.
* Real-time soil monitoring through industrial sensors.
* Successfully demonstrated as a working hardware prototype.

---

## 🔮 Future Improvements

Potential enhancements include:

* Mobile application for farmers.
* Multilingual user interface.
* Disease detection using computer vision.
* Fertilizer recommendation.
* Automated irrigation control.
* Long-term soil health analytics.
* LoRaWAN support for long-range rural communication.
* Offline-first inference for low-connectivity regions.
* Explainable AI for interpreting crop recommendations.
* Cloud-based monitoring dashboard.

---

## 👥 Contributors

This project was developed by a **three-member interdisciplinary team** as part of an academic mini-project.

### Mohamed Ibrahim K

**Role:** AI/ML Engineer · IoT Developer · System Integration

Key contributions:

* Dataset preparation and feature engineering.
* Ensemble machine learning model development.
* Model evaluation and deployment.
* ESP32 and ThingSpeak integration.
* Raspberry Pi edge deployment.
* Weather and rainfall API integration.
* End-to-end hardware, cloud, and AI system integration.

---

## 🎓 Academic Information

| Field              | Details                                                                             |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Academic Title** | Prediction of Crop Yield Based on Soil Parameters using Machine Learning Algorithms |
| **Domain**         | AI · Machine Learning · IoT · Embedded Systems · Precision Agriculture              |
| **Duration**       | January 2026 – May 2026                                                             |
| **Team Size**      | 3 Members                                                                           |
| **University**     | SASTRA Deemed University                                                            |
| **Project Type**   | Mini Project                                                                        |
| **Status**         | Completed                                                                           |

---

## 📄 License

If this repository includes the MIT License:

```text
Copyright © 2026 Mohamed Ibrahim K. All rights reserved.

This repository is publicly available for portfolio and educational demonstration purposes. No permission is granted to copy, modify, distribute, or commercially use the source code without explicit written permission.
```

---

## ⭐ Project Summary

This project demonstrates the development of a complete real-world intelligent system spanning:

**Industrial Sensors → Embedded Systems → IoT → Cloud Computing → External APIs → Data Engineering → Ensemble Machine Learning → Edge AI**

The platform showcases how artificial intelligence, IoT, and embedded systems can be integrated into an end-to-end precision agriculture solution for intelligent, real-time crop recommendation.
