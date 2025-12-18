# healthsync-analytics
A complete data engineering pipeline that processes healthcare data from multiple sources, applies AI/ML insights, and delivers analytics through a cloud-native platform

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg?style=for-the-badge)

**Real-time healthcare monitoring and predictive analytics platform**

[Live Demo](https://healthsync-analytics.up.railway.app) • [API Docs](https://healthsync-analytics.up.railway.app/docs) • [Report Bug](https://github.com/MpiloG29/healthsync-analytics/issues) • [Request Feature](https://github.com/MpiloG29/healthsync-analytics/issues)

</div>

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Live Deployment](#-live-deployment)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Dashboard Guide](#-dashboard-guide)
- [Local Development](#-local-development)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Algorithm](#-algorithm)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Contact](#-contact)

## 🎯 Overview

**HealthSync Analytics** is a modern, cloud-based healthcare monitoring system designed to provide real-time analytics and predictive risk assessment for cardiovascular diseases. The platform combines a powerful FastAPI backend with an intuitive dashboard frontend, enabling healthcare professionals to monitor patient data and predict potential health risks efficiently.

### Key Objectives
- ✅ Provide real-time patient analytics visualization
- ✅ Predict cardiovascular risk based on clinical parameters
- ✅ Offer an intuitive, responsive web interface
- ✅ Ensure seamless cloud deployment and scalability
- ✅ Facilitate easy integration with existing healthcare systems

## ✨ Features

### 📊 **Analytics Dashboard**
- Real-time patient statistics monitoring
- Interactive charts and data visualizations
- Live API status indicators
- Recent predictions history viewer
- Mobile-responsive design

### 🔮 **Risk Prediction Engine**
- Cardiovascular risk assessment based on age and blood pressure
- Three-tier risk classification (Low/Medium/High)
- Detailed prediction results with recommendations
- Prediction history tracking
- Real-time calculation with instant feedback

### 🔧 **API Backend**
- RESTful API with complete CRUD operations
- Comprehensive CORS support
- Automatic API documentation (Swagger/OpenAPI)
- Health monitoring endpoints
- Production-ready error handling

### 🚀 **Deployment & DevOps**
- Automatic cloud deployment via Railway
- Continuous integration ready
- Environment-based configuration
- Zero-downtime deployment capability
- Comprehensive logging and monitoring

### 🛡️ **Security & Reliability**
- CORS configuration for cross-origin requests
- Input validation and sanitization
- Error handling with user-friendly messages
- Rate limiting ready
- Health check endpoints for monitoring

## 🌐 Live Deployment

| Component | URL | Description |
|-----------|-----|-------------|
| **Live Application** | [https://healthsync-analytics.up.railway.app](https://healthsync-analytics.up.railway.app) | Main application entry point |
| **API Documentation** | [https://healthsync-analytics.up.railway.app/docs](https://healthsync-analytics.up.railway.app/docs) | Interactive Swagger UI |
| **Dashboard** | [https://healthsync-analytics.up.railway.app/dashboard.html](https://healthsync-analytics.up.railway.app/dashboard.html) | Primary user interface |
| **API Health Check** | [https://healthsync-analytics.up.railway.app/health](https://healthsync-analytics.up.railway.app/health) | Service status endpoint |
| **GitHub Repository** | [https://github.com/MpiloG29/healthsync-analytics](https://github.com/MpiloG29/healthsync-analytics) | Source code repository |

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (Download from [python.org](https://python.org))
- **Git** (Download from [git-scm.com](https://git-scm.com))
- **Modern Web Browser** (Chrome, Firefox, Edge, or Safari)
- **Internet Connection** (for cloud deployment)

### Installation & Local Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/MpiloG29/healthsync-analytics.git
cd healthsync-analytics
