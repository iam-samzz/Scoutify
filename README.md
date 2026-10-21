# Scoutify

**Discover business websites. Extract contacts. Organize leads.**

Scoutify is a Flask-based web application that automates the collection of publicly available business contact information from websites. It extracts email addresses, phone numbers, and address information, helping users organize website data efficiently.

## Features

- **Website Scraping** — Fetches and parses webpage content.
- **Contact Extraction** — Identifies publicly available emails and phone numbers.
- **AI-Powered Address Extraction** — Uses a locally running Qwen2.5 model to assist with address extraction.
- **Results Management** — Displays extracted information through a web interface.
- **CSV Export** — Exports collected contact information for further use.
- **URL Validation** — Validates website URLs before processing.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Web Scraping:** Requests, BeautifulSoup
- **AI:** Qwen2.5-1.5B-Instruct-GGUF, llama-cpp-python
- **Data Processing:** Instructor, Pydantic, phonenumbers

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/iam-samzz/Scoutify.git
cd Scoutify
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

*Note: Local AI inference may require additional setup and system resources.*

## How It Works

1. Submit website URLs.
2. Scoutify fetches and parses webpage content.
3. Contact information is extracted and organized.
4. Review the results and export them as CSV.

## Limitations

Extraction accuracy depends on website structure and accessibility. Local AI processing may take time, and not all contact information can be guaranteed to be found.

## Contributing

Contributions and suggestions are welcome! Fork the repository, make your changes, and submit a pull request.

## License

No open-source license is specified yet. Please check the repository for licensing updates before reusing or redistributing the project.

---

**Built with Python, Flask, and local AI.**

[GitHub Repository](https://github.com/iam-samzz/Scoutify)
