
# SEVS - Secure Electronic Voting System

SEVS is a Django-based web application designed to facilitate secure, reliable, and efficient electronic voting. This system ensures the integrity and confidentiality of votes using state-of-the-art cryptographic techniques.

## Features

- **User Authentication**: Secure login and registration process to ensure only authorized users can vote.
- **QR Code Integration**: Generate and use QR codes for unique voter identification.
- **Encrypted Votes**: Use advanced cryptographic techniques to encrypt votes and ensure privacy.
- **PDF Reports**: Generate detailed election results and summaries as PDF documents.
- **Time Zone Handling**: Seamless handling of global time zones using `pytz`.
- **Secure Data Exchange**: Employ secure protocols to ensure data integrity and confidentiality.

## Tech Stack

- **Backend**: Django (Python framework)
- **Cryptography**: `pycryptodome`, `phe` (Partial Homomorphic Encryption), and `pynacl`
- **QR Code Support**: Generate QR codes using `qrcode`
- **PDF Generation**: Create professional PDF reports with `reportlab`

## Installation

Follow these steps to set up and run SEVS locally:

### Prerequisites

- Python 3.8+ installed on your system.
- A virtual environment tool (optional but recommended).

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/sevs.git
   cd sevs
   ```

2. **Set Up Virtual Environment**
   (Recommended for isolating dependencies)
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   Install all required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   Set up the database for the application:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   Start the local server:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your web browser and go to:
   ```
   http://127.0.0.1:8000/


## Usage

- **Admin Panel**: Manage elections, voters, and results at `/admin`.
- **Voter Dashboard**: Access to voting options, including QR code scanning and secure vote submission.
- **PDF Reports**: Download election summaries and detailed results.

## Security

- Encrypted votes using `pycryptodome` ensure the confidentiality of each vote.
- QR code integration ensures unique voter identification.
- Homomorphic encryption (`phe`) supports secure vote tallying without revealing individual vote content.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.



## Acknowledgments

SEVS leverages powerful Python libraries for cryptography, PDF generation, and QR code handling. Special thanks to the maintainers of these libraries for making such tools available to the open-source community.

---
