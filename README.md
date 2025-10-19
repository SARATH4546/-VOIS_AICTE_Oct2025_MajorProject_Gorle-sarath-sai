# 🎬 Netflix Dataset Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15.0-red.svg)](https://plotly.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)](https://getbootstrap.com/)

A professional-grade data analytics platform for Netflix content analysis with interactive visualizations and comprehensive insights.

![Netflix Analysis Dashboard](https://via.placeholder.com/800x400/E50914/FFFFFF?text=Netflix+Analysis+Dashboard)

## ✨ Features

- **📊 Interactive Dashboard** - Real-time charts with Plotly.js
- **🔍 Advanced Analytics** - Temporal, geographic, and genre analysis
- **📈 Professional Visualizations** - Netflix-themed charts and graphs
- **🌐 Web Interface** - Modern Flask-based UI with responsive design
- **📱 Mobile-Friendly** - Responsive design for all devices
- **🚀 Production Ready** - Docker support and deployment configs
- **🧪 Comprehensive Testing** - Full test suite included
- **📚 Detailed Documentation** - Complete setup and usage guides

## 🎯 Demo

### Dashboard Analytics
- **Content Growth Trends** - Analyze Netflix's content expansion over time
- **Genre Distribution** - Popular genres and diversity metrics  
- **Geographic Analysis** - Global content distribution patterns
- **Content Strategy** - Movies vs TV shows strategic analysis

### Key Insights Generated
- **Temporal Analysis** - Release patterns and growth rates
- **Market Positioning** - International vs domestic content breakdown
- **Content Diversity** - Genre and country entropy metrics
- **Strategic Recommendations** - Data-driven business suggestions

## 🛠️ Installation

### Quick Start (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/SARATH4546/-VOIS_AICTE_Oct2025_MajorProject_Gorle-sarath-sai.git
   cd -VOIS_AICTE_Oct2025_MajorProject_Gorle-sarath-sai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv netflix_env
   source netflix_env/bin/activate  # On Windows: netflix_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser**
   ```
   http://localhost:5000
   ```

### Docker Installation

```bash
# Build and run with Docker
docker build -t netflix-analysis .
docker run -p 5000:5000 netflix-analysis
```

### Heroku Deployment

```bash
# Deploy to Heroku
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

## 📊 Usage

### 1. Upload Dataset
- Navigate to the upload page
- Select your Netflix CSV dataset
- Click upload to process the data

### 2. Explore Dashboard
- View interactive charts and statistics
- Analyze content growth patterns
- Examine geographic distribution

### 3. Generate Reports
- Access detailed analysis page
- View executive summary
- Export insights and visualizations

### 4. API Access
Available endpoints:
- `/api/temporal-chart` - Content growth data
- `/api/genre-chart` - Genre distribution
- `/api/geographic-chart` - Country analysis
- `/api/content-mix-chart` - Movies vs TV shows

## 🏗️ Project Structure

```
netflix-analysis-platform/
├── 📁 src/                    # Source code modules
│   ├── 📁 data/              # Data processing
│   ├── 📁 analysis/          # Analytics engine
│   ├── 📁 visualization/     # Chart generation
│   └── 📁 utils/             # Helper utilities
├── 📁 templates/             # HTML templates
│   ├── 📄 base.html         # Base template
│   ├── 📄 dashboard.html    # Main dashboard
│   ├── 📄 index.html        # Landing page
│   ├── 📄 upload.html       # File upload
│   └── 📄 analysis.html     # Detailed analysis
├── 📁 static/               # Static assets
│   ├── 📁 css/             # Stylesheets
│   ├── 📁 js/              # JavaScript files
│   └── 📁 images/          # Images and icons
├── 📁 data/                 # Dataset storage
│   ├── 📁 raw/             # Original datasets
│   ├── 📁 processed/       # Cleaned data
│   └── 📁 exports/         # Generated reports
├── 📁 tests/               # Test suite
├── 📁 docs/                # Documentation
├── 📄 app.py              # Main application
├── 📄 requirements.txt    # Dependencies
├── 📄 Dockerfile         # Docker configuration
├── 📄 Procfile          # Heroku deployment
└── 📄 README.md         # This file
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_netflix_analysis.py

# Run with coverage
python -m pytest tests/ --cov=src/
```

## 🎨 Screenshots

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x500/E50914/FFFFFF?text=Netflix+Analytics+Dashboard)

### Content Growth Analysis
![Growth Chart](https://via.placeholder.com/600x400/221F1F/FFFFFF?text=Content+Growth+Over+Time)

### Geographic Distribution
![Geographic Analysis](https://via.placeholder.com/600x400/564D4D/FFFFFF?text=Global+Content+Distribution)

## 🚀 Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.2** - Web framework
- **Pandas 2.0.3** - Data manipulation and analysis
- **NumPy 1.24.3** - Numerical computing
- **SciPy 1.11.1** - Scientific computing

### Frontend
- **HTML5 & CSS3** - Structure and styling
- **JavaScript ES6+** - Interactive functionality
- **Bootstrap 5.3.2** - Responsive UI framework
- **Font Awesome 6.4.0** - Icons

### Data Visualization
- **Plotly.js 2.27.0** - Interactive charts
- **Matplotlib 3.7.1** - Static visualizations
- **Seaborn 0.12.2** - Statistical plots

### Development & Deployment
- **Docker** - Containerization
- **Heroku** - Cloud deployment
- **Gunicorn** - WSGI HTTP Server
- **pytest** - Testing framework

## 📈 Performance

- **Fast Loading** - Optimized for quick chart rendering
- **Scalable** - Handles datasets up to 100,000+ records
- **Responsive** - Works on desktop, tablet, and mobile
- **Memory Efficient** - Optimized data processing pipeline

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/SARATH4546/netflix-analysis-platform.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 src/ tests/
black src/ tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Project Maintainer 

**NAME** : Gorle Sarathsai

**Email**:sarathsaigorle996@gmail.com

**LinkedIn**: SARATHSAI GORLE

**GitHub**:SARATH4546

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Open an issue on GitHub for bug reports
- **Questions**: Use GitHub Discussions for general questions
- **Email**: sarathsaigorle996@gmail.com

## 🔮 Roadmap

### Version 2.0 (Upcoming)
- [ ] Machine Learning predictions
- [ ] Real-time data streaming
- [ ] Advanced filtering options
- [ ] Export to multiple formats
- [ ] User authentication system
- [ ] Custom dashboard themes
- [ ] API rate limiting
- [ ] Automated testing pipeline

### Version 1.1 (Current)
- [x] Interactive dashboard
- [x] Comprehensive analytics
- [x] Professional visualizations
- [x] Docker support
- [x] Heroku deployment
- [x] Complete test suite

---

**🎬 Built with ❤️ for Netflix Data Analysis Excellence**

