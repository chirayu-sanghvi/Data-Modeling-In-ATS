# Data Modeling in ATS

Data Modeling in ATS (Applicant Tracking System) is a Python-based project designed to create, manipulate, and manage database tables effectively. The project provides utilities for table creation, deletion, and viewing results through a web interface powered by Flask.

---
## Demo Video

Watch the demo video directly here:  
[![Demo Video](https://via.placeholder.com/600x300.png?text=Demo+Video+Preview)]([https://drive.google.com/uc?id=YOUR_FILE_ID](https://drive.google.com/file/d/137IlEInLIAr6yHuo61FtIJA2OySg51IN/view)
---

## Features

- **Table Management**:
  - Create tables with the desired schema using `create_table.py`.
  - Delete unnecessary tables using `delete_tables.py`.
- **Web Interface**:
  - View and interact with results using Flask-based templates.
  - Display results in a user-friendly format via `index.html` and `results.html`.
- **Modular Architecture**:
  - Organized structure for easy navigation and development.
- **Lightweight**:
  - Minimal dependencies with essential functionality.

---

## Directory Structure

```plaintext
chirayu-sanghvi-Data-Modeling-In-ATS/
├── README.md                  # Project documentation
├── ProcFile                   # Deployment configuration for platforms like Heroku
├── app.py                     # Flask application entry point
├── create_table.py            # Script to create database tables
├── delete_tables.py           # Script to delete database tables
├── index.html                 # Main HTML template for the web interface
├── requirements.txt           # List of project dependencies
├── results.html               # Results display template
└── template/                  # Template folder for Flask
    ├── index.html             # Index page template
    ├── result.txt             # Example output data
    └── results.html           # Results page template
```
---
## Installation

### Prerequisites

- Python 3.8 or higher
- Flask
- SQLite or any compatible database

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/chirayu-sanghvi/Data-Modeling-In-ATS.git
   cd Data-Modeling-In-ATS
   ```
2. **Set Up Environment Variable**
   ```
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Run the application**
   ```
   python app.py
   ```
5. Access the Web Interface:
   - Open your browser and navigate to http://127.0.0.1:5000
---
## Usage
1. **Create Tables**:
   - User create_table.py to define and create tables in your database.
   - Run the Script:
     ```
     python create_table.py
     ```
2. **Delete Tables**:
   - Use delete_table.py to remove unnecessary tables.
   - Run the Script:
     ```
     python delete_table.py
     ```
3. **View Results**:
   - Open the web interface (http://127.0.0.1:5000) to interact with data and view results.
---
## Deployment
if deploying to a platform like Heroku:
1. Ensure the ProcFile is correctly configured.
2. Add required environment variables.
3. Deploy the app using Git:
   ```
   git push heroku main
   ```
---
## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Contact

For queries, reach out to **Chirayu Sanghvi** at [chirayus@buffalo.edu](mailto:chirayus@buffalo.edu).

---

## Acknowledgments

- **PostgreSQL**: [Documentation](https://www.postgresql.org/)
- **Heroku**: [Heroku](https://www.heroku.com/?utm_source=google&utm_medium=paid_search&utm_campaign=amer_heraw&utm_content=general-branded-search-rsa&utm_term=heroku&utm_source_platform=GoogleAds&gad_source=1&gclid=CjwKCAiAp4O8BhAkEiwAqv2UqNYlFb9wLLmxGDnwez1oHZa3s4W5awKaUJpj1FvV7-sVoiPxOQ2DHxoCa90QAvD_BwE)
