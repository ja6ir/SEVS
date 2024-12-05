
# SEVS - Secure Electronic Voting System for College Elections
![License](https://img.shields.io/badge/license-MIT-blue.svg)

SEVS (Secure Electronic Voting System) is a Django-based web application designed to manage and conduct secure college elections. The system ensures transparency, integrity, and confidentiality throughout the voting process. It employs state-of-the-art cryptographic techniques and features a hierarchical role-based structure for managing duties across various election participants.

---

## Features

- **Role-Based Access Control (RBAC)**: Hierarchical user roles such as Election Officer, HOD, Faculty, and Students, each with specific permissions.
- **User Authentication**: Secure login and registration processes to ensure only authorized users can participate.
- **QR Code Integration**: Generate and use QR codes for unique voter identification.
- **Encrypted Votes**: Advanced cryptographic techniques are used to encrypt votes and ensure voter privacy.
- **PDF Reports**: Generate detailed election results and summaries as downloadable PDF files.
- **Time Zone Handling**: Efficient handling of global time zones using `pytz`.
- **Secure Data Exchange**: Ensure data integrity and confidentiality during the voting and election process.

---

## Role Hierarchy

The system is structured to support various roles involved in the election process. Each role has a distinct set of responsibilities and access privileges:

### 1. **Election Officer**
   - Full administrative control over the entire election process.
   - Responsibilities include setting up elections, managing candidates, and generating reports.
   - Can view, edit, and manage all election data.

### 2. **HOD (Head of Department)**
   - Can manage election-related tasks for their respective department.
   - Oversees faculty and student voting within their department.
   - Can view voting results and reports for their department.

### 3. **Faculty**
   - Can participate in elections (as voters) and view results.
   - Can manage candidate nominations for specific departments or elections if allowed by the Election Officer.

### 4. **Student**
   - Can register and vote for candidates in the elections.
   - View election results (only the results they are eligible to see based on their department and position).

---

## Tech Stack

- **Backend**: Django (Python web framework)
- **Cryptography**: `pycryptodome`, `phe` (Partial Homomorphic Encryption), and `pynacl`
- **QR Code Support**: Generate QR codes using `qrcode`
- **PDF Generation**: Create detailed election reports with `reportlab`
- **Time Zone Handling**: `pytz`
- **Database**: SQLite (for local development and small-scale deployments)

---

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
   ```

---

## Usage

### Role-Based Access

- **Election Officer Dashboard**: Full administrative access to manage elections, candidates, and voters.
- **HOD Dashboard**: Can oversee and manage elections within their respective department.
- **Faculty Dashboard**: Can register to vote, view election candidates, and participate in the voting process.
- **Student Dashboard**: Can register, participate in voting, and view results relevant to their department.

### Key Functionalities

- **Admin Panel**: For Election Officers to manage election settings, reports, and candidates.
- **Voter Registration and Voting**: Students and faculty can securely register and cast votes.
- **Election Reports**: Election results are generated and displayed as downloadable PDF reports.

---

## Security

- **Cryptographic Security**: Votes are encrypted using `pycryptodome` to ensure confidentiality and security.
- **Homomorphic Encryption**: The use of `phe` ensures that votes can be tallied without revealing individual votes.
- **QR Code Integration**: Each voter is assigned a unique QR code for authentication, preventing fraud and ensuring integrity.
- **Secure Authentication**: All users (Election Officers, HODs, Faculty, Students) are authenticated and authorized based on their role.

---

## Contributing

We welcome contributions to improve SEVS! Please follow these steps to contribute:

1. Fork the repository on GitHub.
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

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

SEVS relies on the following open-source libraries:
- `Django` for the web framework.
- `pycryptodome` for cryptographic operations.
- `phe` for partial homomorphic encryption.
- `qrcode` for QR code generation.
- `reportlab` for PDF generation.

Special thanks to the maintainers of these libraries for their excellent work in enabling secure systems like SEVS.

---
