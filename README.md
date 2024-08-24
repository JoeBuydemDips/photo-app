# Cyberpunk Photo Search

![Run Tests](https://github.com/yourusername/cyberpunk-photo-search/workflows/Run%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/cyberpunk-photo-search/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/cyberpunk-photo-search)

Photo Search is a web application with "Cyber Punk Theme" that allows users to search for photos using the Unsplash API.

## Features

- Search for photos using keywords
- Paginated results
- Expandable photo previews
- Dark and light mode toggle

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- Httpx
- Python-dotenv

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cyberpunk-photo-search.git
   cd cyberpunk-photo-search
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Unsplash API key:
   ```
   UNSPLASH_API_KEY=your_unsplash_api_key_here
   ```

## Usage

1. Start the FastAPI server:

   ```
   uvicorn app.main:app --reload
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Enter keywords in the search box to find cyberpunk-themed photos

4. Use the pagination controls to navigate through the results

5. Click on a photo to view an expanded preview

6. Toggle between dark and light modes using the "Toggle Theme" button

## Running Tests

To run the tests, use the following command:

```
pytest --cov=app tests/
```

This will run all the tests and provide a coverage report.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
