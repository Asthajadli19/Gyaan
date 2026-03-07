# GyaanShelf - Book Reselling Platform (folder renamed to `gyan`) 

A comprehensive Flask-based backend (now contained in the `gyan` folder) for a book reselling marketplace with user authentication, book management, and wishlist functionality.

## 🚀 Features

- **User Authentication**
  - Secure registration with email validation
  - Password hashing using Werkzeug security
  - Session-based login/logout
  - User profile management

- **Book Management**
  - List books for sale with detailed information
  - Upload and optimize book cover images
  - Edit and delete listings
  - Browse and search books with filtering
  - Book details page with seller information

- **User Dashboard**
  - View all your listings
  - Monitor book status and views
  - Quick edit/delete actions
  - Sales statistics

- **Wishlist System**
  - Add/remove books from wishlist
  - View saved books
  - Quick access to favorite listings

- **Responsive Design**
  - Mobile-friendly interface
  - Modern UI with Tailwind CSS
  - Smooth animations and transitions

## 📋 Requirements

- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

## 🔧 Installation & Setup

### 1. Clone/Download the Project
```bash
cd gyan
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

**Option A: Using MySQL Command Line**

```bash
mysql -u root -p
```

Then run:
```sql
CREATE DATABASE IF NOT EXISTS gyaanshelf;
USE gyaanshelf;
-- Paste contents of database.sql here
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Create new connection if needed
3. Go to File > Open SQL Script > Select `database.sql`
4. Execute the script

### 5. Configure Database Connection

Edit `app.py` and update these lines with your MySQL credentials:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'
app.config['MYSQL_DB'] = 'gyaanshelf'
```

Or in `config.py` for different environments.

### 6. Create Uploads Directory

The `/static/uploads` folder is created automatically on first run, but you can pre-create it:

```bash
mkdir static/uploads
```

### 7. Run the Application

```bash
python app.py
```

The app will start at: **http://localhost:5000**

## 📁 Project Structure

```
gyan/
├── app.py                 # Main Flask application with all routes
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── database.sql          # MySQL database schema
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── browse.html       # Book browsing page
│   ├── book_detail.html  # Book details page
│   ├── sell_book.html    # List a new book
│   ├── edit_book.html    # Edit book listing
│   ├── dashboard.html    # User dashboard
│   ├── profile.html      # User profile
│   ├── wishlist.html     # Wishlist page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── uploads/          # User-uploaded book images
└── README.md             # This file
```

## 🗄️ Database Schema

### Tables

**users** - User accounts and profiles
- id, full_name, email, phone, password_hash, location, profile_image, bio, created_at, updated_at, is_active

**books** - Book listings
- id, user_id, title, author, isbn, category, description, price, condition, book_image, publication_year, pages, language, status, views, created_at, updated_at

**transactions** - (Optional) Purchase history
- id, buyer_id, seller_id, book_id, price_paid, transaction_type, status, transaction_date, completed_date, notes

**wishlist** - User wishlist items
- id, user_id, book_id, added_at

**reviews** - Book reviews and ratings
- id, user_id, book_id, rating, review_text, created_at, updated_at

## 🛣️ API Routes

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Books
- `GET /` - Home page
- `GET /browse` - Browse all books
- `GET /book/<id>` - View book details
- `GET /sell` - Sell book form
- `POST /sell` - Create new listing
- `GET /book/<id>/edit` - Edit listing
- `POST /book/<id>/edit` - Update listing
- `POST /book/<id>/delete` - Delete listing

### User Account
- `GET /dashboard` - User dashboard
- `GET /profile` - View/edit profile
- `POST /profile/update` - Update profile

### Wishlist
- `GET /wishlist` - View wishlist
- `GET /wishlist/add/<id>` - Add to wishlist
- `GET /wishlist/remove/<id>` - Remove from wishlist

## 🔐 Security Features

- **Password Hashing**: Uses Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session Management**: Flask sessions with secret key
- **Input Validation**: Email, phone, password strength validation
- **File Upload Security**: File type validation, size limits, image optimization
- **SQL Injection Prevention**: Using parameterized queries
- **CSRF Protection**: (Can be added with Flask-WTF)

## 📸 Image Handling

- Uploaded images are automatically resized to 400x600px
- Images are optimized to JPEG format with 85% quality
- Supports: PNG, JPG, JPEG, GIF, WEBP
- Maximum file size: 16MB

## 🎨 Styling

- **Tailwind CSS** for responsive design
- **Lucide Icons** for SVG icons
- **Custom CSS** in base.html for themed colors
- Color scheme: Warm book-themed palette (browns, golds, creams)

## 🧪 Testing

Create a test user:
1. Go to `http://localhost:5000/register`
2. Fill in test data:
   - Name: John Doe
   - Email: john@example.com
   - Phone: 9876543210
   - Location: Mumbai
   - Password: Test@123

## 🚨 Troubleshooting

### MySQL Connection Error
```
Error: MySQL server is not running
```
**Solution**: Start MySQL service
```bash
# Windows
net start MySQL80

# Mac
brew services start mysql-community-server

# Linux
sudo systemctl start mysql
```

### Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Image Upload Not Working
```
FileNotFoundError: [Errno 2] No such file or directory: 'static/uploads'
```
**Solution**: Create the uploads directory
```bash
mkdir static/uploads
chmod 755 static/uploads
```

### Database Connection Failed
- Verify MySQL is running
- Check credentials in `app.py`
- Ensure database is created: `CREATE DATABASE gyaanshelf;`

## 🔄 Database Backup

To backup the database:
```bash
mysqldump -u root -p gyaanshelf > backup.sql
```

To restore from backup:
```bash
mysql -u root -p gyaanshelf < backup.sql
```

## 📝 Environment Variables

For production, use environment variables:

```bash
# .env file
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=gyaanshelf
FLASK_ENV=production
```

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production` and `DEBUG=False`
2. Use a production WSGI server like **Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. Use **Nginx** or **Apache** as reverse proxy
4. Set up **SSL/HTTPS** certificate
5. Use **PostgreSQL** instead of MySQL for better scalability
6. Implement proper **logging and monitoring**

## 📧 Future Enhancements

- Email verification for registration
- Password reset functionality
- Messaging system between buyers/sellers
- Payment integration (Razorpay, Stripe)
- Book ratings and reviews
- Advanced search with Elasticsearch
- Email notifications
- Admin panel for moderation
- Analytics dashboard

## 📄 License

This project is open source and available for educational purposes.

## 👥 Support

For issues or questions, please contact: support@gyaanshelf.com

---

**Created**: March 7, 2026  
**Version**: 1.0.0  
**Framework**: Flask 2.3.3  
**Database**: MySQL 5.7+
