# Developer Guide

This guide will help you set up your development environment and explain how to contribute to the Emoji Library project.

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setting Up Your Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/emoji-call.git
cd emoji-call
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```
The database will be automatically created when you first run the application.

### Running the Application Locally

1. Start the Flask development server:
```bash
python app.py
```

2. Visit `http://localhost:5000` in your web browser

### Project Structure

```
emoji-call/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html    # Main page template
├── emoji_stats.db    # SQLite database (created on first run)
├── README.md         # Project documentation
└── DEVELOPER.md      # This guide
```

## Deployment

### Deploying to Azure Web App

1. Create an Azure Web App:
```bash
az webapp up --name <your-app-name> --runtime "PYTHON:3.9" --sku B1
```

2. Configure the application settings:
   - Set `WEBSITE_PYTHON_VERSION` to "3.9"
   - Add startup command in Configuration → General settings:
     ```
     gunicorn --bind=0.0.0.0 --timeout 600 app:app
     ```

3. Set up deployment from your repository:
   - Connect your GitHub repository to Azure
   - Enable GitHub Actions for continuous deployment

### Database Considerations

The default SQLite database works for development but for production:
- Consider using Azure SQL Database or another cloud database
- Update the database connection code in `app.py`
- Use environment variables for database credentials

## Contributing

### Getting Started

1. Fork the repository on GitHub
2. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

### Development Guidelines

1. Code Style
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add comments for complex logic

2. Making Changes
   - Keep commits focused and atomic
   - Write clear commit messages
   - Add tests for new features
   - Update documentation as needed

3. Testing
   - Run existing tests before submitting changes
   - Add new tests for new functionality
   - Ensure all tests pass

### Submitting Changes

1. Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create a Pull Request:
   - Open a PR from your fork to our main repository
   - Describe your changes in detail
   - Reference any related issues
   - Wait for review and address any feedback

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include screenshots for UI changes
- Update README.md if adding new features
- Ensure CI checks pass

## Need Help?

- Open an issue for bugs or feature requests
- Join our community discussions
- Check existing issues and PRs before creating new ones

## License

This project is licensed under the MIT License - see the LICENSE file for details. 