# Python API Application

A small Python-based application designed to support API testing.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Running the Application](#running-the-application)
- [Verifying the Application](#verifying-the-application)
- [User Tokens](#user-tokens)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python**: Download from [python.org](https://www.python.org/downloads/).

## Installation Steps

### Step 1: Install Python

1. **Download Python**:
   - Visit the official Python website: [python.org](https://www.python.org/downloads/).
   - Download the latest version of Python compatible with your operating system.

2. **Install Python**:
   - Run the installer.
   - Ensure you check the box that says **"Add Python to PATH"** before clicking **"Install Now"**.

3. **Verify Python Installation**:
   - Open a command prompt (Windows) or terminal (macOS/Linux).
   - Type the following command and press Enter:
     ```bash
     python --version
     ```
   - You should see the installed version of Python.

### Step 2: Install Required Libraries

1. **Set Up a Virtual Environment** (optional but recommended):
   - Create a virtual environment by running:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **macOS/Linux**:
       ```bash
       source venv/bin/activate
       ```

2. **Install Flask**:
   - With the virtual environment activated, run the following command to install Flask:
     ```bash
     pip install Flask
     ```

### Step 3: Download and Run the Application

1. **Download the Application File**:
   - Download `webshop_api.py` to your computer.

2. **Run the Application**:
   - Open a terminal in the folder where you have placed the `webshop_api.py` file.
   - Run the application with the following command:
     ```bash
     python webshop_api.py
     ```

3. **Check for Output**:
   - You should see output indicating that the Flask server is running, typically something like:
     ```
     Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     ```

### Step 4: Verify the Application Works

1. **Open Your Web Browser**:
   - Navigate to the following URL:
     ```
     http://127.0.0.1:5000/products
     ```
   - You should see the currently available products in the application.

## User Tokens

Below is a table listing the user tokens for existing users:

| Username | Token        |
|----------|--------------|
| admin    | admin_token  |
| user1    | user1_token  |
| user2    | user2_token  |

For any additional newly created users, the token will be in the format `'username'_token`.

## Conclusion

You have successfully set up and run the Python API application. You can now use it for API testing and further development.
