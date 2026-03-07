




echo ""
echo "============================================"
echo "GyaanShelf - gyan folder setup"
echo "============================================"
echo ""


if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2] Activating virtual environment..."
source venv/bin/activate

echo "[3] Upgrading pip..."
python -m pip install --upgrade pip

echo "[4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[5] Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Create MySQL database:"
echo "   - Open MySQL Client: mysql -u root -p"
echo "   - Run: source database.sql"
echo ""
echo "2. Update database credentials in app.py:"
echo "   - MYSQL_HOST = 'localhost'"
echo "   - MYSQL_USER = 'your_username'"
echo "   - MYSQL_PASSWORD = 'your_password'"
echo ""
echo "3. Run the application:"
echo "   - python app.py"
echo ""
echo "4. Open browser and go to: http://localhost:5000"
echo ""


chmod +x setup.sh