# GyaanShelf gyan Folder - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### For Windows Users

1. **Open Command Prompt** and navigate to the gyan folder:
   ```bash
   cd gyan
   ```

2. **Run the setup script**:
   ```bash
   setup.bat
   ```

3. **Create the database**:
   - Open MySQL Command Line Client
   - Copy and paste the contents of `database.sql` and execute

4. **Update credentials** in `app.py` (lines ~13-17):
   ```python
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   ```

5. **Run the app**:
   ```bash
   python app.py
   ```

6. **Open browser**:
   - Go to `http://localhost:5000`

---

### For Mac/Linux Users

1. **Open Terminal** and navigate to the gyan folder:
   ```bash
   cd gyan
   ```

2. **Make setup script executable**:
   ```bash
   chmod +x setup.sh
   ```

3. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

4. **Create the database**:
   ```bash
   mysql -u root -p < database.sql
   ```

5. **Update credentials** in `app.py` (lines ~13-17):
   ```python
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   ```

6. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

7. **Run the app**:
   ```bash
   python app.py
   ```

8. **Open browser**:
   - Go to `http://localhost:5000`

---

## 📋 Manual Setup (If Setup Scripts Don't Work)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database
```bash
mysql -u root -p

# In MySQL prompt:
CREATE DATABASE gyaanshelf;
USE gyaanshelf;
-- Paste entire contents of database.sql
SOURCE database.sql;
```

### Step 4: Configure Database Connection
Edit `app.py` and update (around line 13-17):
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # CHANGE THIS
app.config['MYSQL_DB'] = 'gyaanshelf'
```

### Step 5: Run Application
```bash
python app.py
```

Output should show:
```
 * Running on http://127.0.0.1:5000
```

---

## 🧪 Test the Application

### 1. Register a Test User
- Go to http://localhost:5000/register
- Fill in test data:
  - **Full Name**: Test User
  - **Email**: test@example.com
  - **Phone**: 9876543210
  - **Location**: Test City
  - **Password**: Test@12345
  - Check agreements
  - Click "Create Account"

### 2. Login
- Go to http://localhost:5000/login
- Use the email and password you just created

### 3. List a Book
- After login, click "Sell Books"
- Fill in book details:
  - **Title**: Test Book
  - **Author**: Test Author
  - **Category**: Fiction
  - **Price**: 299
  - **Condition**: Good
  - Click "List This Book"

### 4. Browse Books
- Click "Browse Books" to see all listings
- Search and filter books

---

## 📁 Project Structure Explained

```
gyan/
├── app.py                 # Main Flask app - all routes here
├── config.py             # Configuration for different environments
├── database.sql          # SQL to create tables
├── requirements.txt      # Python packages needed
├── setup.bat             # Auto-setup for Windows
├── setup.sh              # Auto-setup for Mac/Linux
│
├── templates/            # HTML files
│   ├── base.html         # Navigation and footer (used by all)
│   ├── index.html        # Home page
│   ├── register.html     # Registration form
│   ├── login.html        # Login form
│   ├── browse.html       # Browse all books
│   ├── book_detail.html  # Single book page
│   ├── sell_book.html    # List a book for sale
│   ├── edit_book.html    # Edit your book
│   ├── dashboard.html    # Your books
│   ├── profile.html      # Your profile
│   ├── wishlist.html     # Saved books
│   ├── 404.html          # Page not found
│   └── 500.html          # Server error
│
└── static/
    └── uploads/          # Where book images are saved
```

---

## 🔑 Key Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register` | POST | Create new account |
| `/login` | POST | Login |
| `/logout` | GET | Logout |
| `/browse` | GET | See all books |
| `/book/<id>` | GET | Book details |
| `/sell` | POST | List new book |
| `/book/<id>/edit` | POST | Update book |
| `/book/<id>/delete` | POST | Remove book |
| `/dashboard` | GET | Your books |
| `/profile` | GET/POST | Your profile |
| `/wishlist` | GET | Saved books |

---

## 🆘 Common Issues & Solutions

### ❌ "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### ❌ "Can't connect to MySQL server on 'localhost'"
**Solution**: Start MySQL service
```bash
# Windows
net start MySQL80

# Mac
brew services start mysql-community-server

# Linux
sudo systemctl start mysql
```

### ❌ "ERROR 2003 (HY000): Can't connect to MySQL server"
**Solution**: Update credentials in `app.py`
```python
app.config['MYSQL_PASSWORD'] = 'your_actual_password'
```

### ❌ Image upload not working
**Solution**: Create uploads folder
```bash
mkdir static/uploads
```

### ❌ Port 5000 already in use
**Solution**: Change port in `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

---

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app with all routes and logic |
| `config.py` | Database and app settings |
| `database.sql` | Creates tables in MySQL |
| `requirements.txt` | List of Python packages to install |
| `base.html` | Navigation bar and footer (used by all pages) |
| `README.md` | Full documentation |

---

## 🎯 What Each Page Does

### 🏠 Home (`/`)
- Shows featured books
- Has "How it works" section
- Call-to-action buttons

### 📚 Browse (`/browse`)
- All available books
- Search by title/author
- Filter by category
- Pagination

### 📖 Book Detail (`/book/<id>`)
- Full book info
- Seller details
- Similar books
- Wishlist button

### ✏️ Sell Book (`/sell`)
- Form to list a book
- Image upload
- Category selection
- Price and condition

### 🎯 Dashboard (`/dashboard`)
- Your listed books
- Edit/delete options
- Statistics (total, sold, available)

### 👤 Profile (`/profile`)
- Edit your info
- Change location
- Add bio
- Security settings

### ❤️ Wishlist (`/wishlist`)
- Saved books
- Quick access
- Remove items

---

## 🔒 Security Notes

- ✅ Passwords are hashed (not stored as plain text)
- ✅ Email and phone are unique
- ✅ File uploads are validated
- ✅ Images are optimized
- ✅ SQL queries use parameters (no injection)

---

## 📞 Support

If you get stuck:
1. Check the README.md file (full documentation)
2. Review error messages carefully
3. Ensure MySQL is running
4. Verify file paths are correct
5. Check that credentials are updated

---

## ✅ Next Steps After Setup

1. **Explore the application** - Click around and test features
2. **Read the README.md** - Full documentation and features
3. **Check database.sql** - Understand the schema
4. **Review app.py** - See how routes work
5. **Customize** - Change colors, add features, etc.

---

**Good luck! Happy coding! 🎉**
