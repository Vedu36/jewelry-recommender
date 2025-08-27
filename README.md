# 🎯 Dazzlez - AI-Powered Jewelry Recommender

An intelligent jewelry recommendation system that creates personalized diamond ring suggestions based on customer stories, preferences, and visual inspiration. Built with FastAPI and modern web technologies.

## ✨ Features

- **Story-Based Recommendations**: AI analyzes love stories to create personalized jewelry designs
- **Visual Inspiration Analysis**: Upload images for style-based recommendations
- **Premium Design Generation**: Sophisticated algorithm considers personality, budget, and preferences
- **Interactive Web Interface**: Modern, responsive design with real-time ring visualizations
- **Multiple Input Methods**: Story form, preference selection, or image upload
- **Session Management**: Track user sessions and recommendation history

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jewelry-recommender
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv jewelry_env
   jewelry_env\Scripts\activate

   # macOS/Linux
   python3 -m venv jewelry_env
   source jewelry_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the project structure**
   ```bash
   # Create static directory if it doesn't exist
   mkdir -p static
   
   # Move index.html to static folder
   mv index.html static/
   ```

5. **Run the application**
   ```bash
   # Option 1: Use the startup script (recommended)
   python startup.py

   # Option 2: Run directly with uvicorn
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - Open your browser and go to: `http://localhost:8000`
   - API documentation available at: `http://localhost:8000/docs`

## 📁 Project Structure

```
jewelry-recommender/
├── main.py                 # FastAPI application with all endpoints
├── requirements.txt        # Python dependencies
├── sample_data.json       # Sample jewelry database
├── startup.py             # Easy startup script
├── test_api.py           # API testing script
├── static/
│   └── index.html        # Frontend web interface
└── README.md             # This file
```

## 🔧 Configuration

### Environment Setup

The application runs with default settings, but you can customize:

```python
# In main.py, you can modify:
HOST = "0.0.0.0"  # Change to "127.0.0.1" for local only
PORT = 8000       # Change port if needed
```

### Database Configuration

Currently uses in-memory storage. For production, consider implementing:
- PostgreSQL or MySQL for persistent storage
- Redis for session management
- File-based storage for uploaded images

## 🛠 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the main web interface |
| `POST` | `/api/story-recommendations` | Generate story-based recommendations |
| `POST` | `/api/preferences` | Generate preference-based recommendations |
| `POST` | `/api/upload-images` | Upload and analyze visual inspiration |
| `POST` | `/api/shortlist` | Add design to user's shortlist |
| `GET` | `/api/data/options` | Get available jewelry options |

### Example API Usage

```python
import requests

# Story-based recommendation
story_data = {
    "story": {
        "love_story": "We met at a beach during sunset...",
        "personality": "She's artistic and loves vintage things",
        "occasion": "engagement"
    },
    "preferences": {
        "budget_range": "10000-20000",
        "metal_type": "rose_gold"
    }
}

response = requests.post(
    "http://localhost:8000/api/story-recommendations",
    json=story_data
)
recommendations = response.json()
```

## 🧪 Testing

### Automated Testing

```bash
# Run the test script (requires running server)
python test_api.py
```

### Manual Testing

1. Start the server: `python startup.py`
2. Open `http://localhost:8000`
3. Try different input methods:
   - Fill out the story form
   - Use preference selectors
   - Upload inspiration images

### API Testing with curl

```bash
# Test preferences endpoint
curl -X POST "http://localhost:8000/api/preferences" \
  -H "Content-Type: application/json" \
  -d '{
    "ring_type": "engagement",
    "budget_range": "10000-20000",
    "metal_type": "platinum"
  }'
```

## 🎨 Customization

### Adding New Diamond Shapes

In `main.py`, update the `PREMIUM_JEWELRY_DATA`:

```python
PREMIUM_JEWELRY_DATA = {
    "diamonds": {
        "your_new_shape": {
            "brilliance": "excellent",
            "price_premium": 0.90,
            "story_themes": ["modern", "unique"]
        }
    }
}
```

### Styling Modifications

Edit `static/index.html` to customize:
- Colors and themes
- Layout and typography
- Animation effects
- Ring visualizations

### Adding New Recommendation Logic

In `main.py`, modify these functions:
- `analyze_story_text()` - Story analysis logic
- `generate_premium_suggestions()` - Recommendation algorithm
- `generate_story_connection()` - Personalization logic

## 🚨 Troubleshooting

### Common Issues

**1. Port already in use**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

**2. Static files not found**
```bash
# Ensure index.html is in static folder
mkdir static
cp index.html static/
```

**3. Module not found errors**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

**4. CORS issues**
- The app includes CORS middleware for development
- For production, restrict `allow_origins` in `main.py`

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security Considerations

For production deployment:

1. **Remove CORS wildcard**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Specific domains
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

2. **Add input validation**
3. **Implement rate limiting**
4. **Use HTTPS**
5. **Secure file uploads**

## 📈 Performance Optimization

### For High Traffic

1. **Use async database connections**
2. **Implement caching** (Redis)
3. **Add request queuing**
4. **Optimize image processing**
5. **Use CDN for static files**

### Database Optimization

```python
# Example PostgreSQL setup
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql://user:password@localhost/jewelry_db"
engine = create_async_engine(DATABASE_URL)
```

## 🚀 Deployment

### Local Development
```bash
python startup.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options

- **Heroku**: Simple deployment with Procfile
- **AWS EC2**: Full control with load balancing
- **Google Cloud Run**: Serverless container deployment
- **DigitalOcean**: Cost-effective VPS hosting

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Future Enhancements

- [ ] User authentication and profiles
- [ ] Payment processing integration
- [ ] 3D ring visualization
- [ ] Mobile app development
- [ ] AI-powered chat assistant
- [ ] Inventory management system
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Run the test script: `python test_api.py`
4. Create an issue on GitHub

## 📊 Sample Data

The application includes comprehensive sample data in `sample_data.json`:
- Diamond shapes and properties
- Metal types and pricing
- Setting styles and descriptions
- Style preferences and characteristics

## 🔄 Version History

- **v2.0.0**: Story-based recommendations, enhanced UI
- **v1.5.0**: Image upload and analysis
- **v1.0.0**: Basic preference-based recommendations

---

**Happy coding! 💎✨**
