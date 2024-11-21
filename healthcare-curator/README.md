http://localhost:5000# Healthcare Product Curator

## Overview
A web application for curating and discovering healthcare products, featuring search, filtering, and product details.

## Features
- Browse healthcare products
- Search products by name, description, or category
- Filter products by category
- Responsive design
- Product ratings and details

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd healthcare-curator
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure
- `src/app.py`: Main Flask application
- `templates/index.html`: Frontend HTML template
- `requirements.txt`: Python dependencies

## Technologies Used
- Backend: Flask, SQLAlchemy
- Frontend: HTML, JavaScript, Bootstrap
- Database: SQLite

## Extending the Project
- Add more product categories
- Implement user authentication
- Create admin panel for product management

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
