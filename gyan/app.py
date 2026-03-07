"""
GyaanShelf - Book Reselling Platform
Main Flask Application
Author: GyaanShelf Team
Date: 2026
"""

import os
import re
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
from PIL import Image
import io





app = Flask(__name__)
# use environment variables for configuration (render.com sets PORT, etc.)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'astha123')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'gyaanshelf')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}




def get_db_connection():
    """Get database connection"""
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )





def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (10 digits minimum)"""
    phone = re.sub(r'\D', '', phone)
    return len(phone) >= 10

def validate_password(password):
    """Validate password strength (minimum 8 chars with numbers)"""
    return len(password) >= 8 and any(char.isdigit() for char in password)

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_user_data(user_id):
    """Get user data from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def save_book_image(file, book_id):
    """Save and optimize book image"""
    if file and allowed_file(file.filename):
        try:

            img = Image.open(file)
            img.thumbnail((400, 600), Image.Resampling.LANCZOS)


            filename = f'book_{book_id}_{datetime.now().timestamp()}.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)


            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


            img.save(filepath, 'JPEG', quality=85, optimize=True)
            return filename
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return None
    return None





@app.route('/')
def index():
    """Home page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE status = "Available" ORDER BY created_at DESC LIMIT 8')
    featured_books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', featured_books=featured_books)

@app.route('/browse')
def browse_books():
    """Browse all available books"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '', type=str)
    search = request.args.get('search', '', type=str)

    conn = get_db_connection()
    cursor = conn.cursor()


    query = 'SELECT * FROM books WHERE status = "Available"'
    params = []

    if category:
        query += ' AND category = %s'
        params.append(category)

    if search:
        query += ' AND (title LIKE %s OR author LIKE %s OR description LIKE %s)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])


    count_query = query.replace('SELECT *', 'SELECT COUNT(*) as count')
    cursor.execute(count_query, params)
    total = cursor.fetchone()['count']


    items_per_page = 12
    offset = (page - 1) * items_per_page
    query += f' ORDER BY created_at DESC LIMIT {items_per_page} OFFSET {offset}'

    cursor.execute(query, params)
    books = cursor.fetchall()


    cursor.execute('SELECT DISTINCT category FROM books ORDER BY category')
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    total_pages = (total + items_per_page - 1) // items_per_page

    return render_template('browse.html',
                         books=books,
                         categories=categories,
                         current_page=page,
                         total_pages=total_pages,
                         search=search,
                         selected_category=category)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """View book details"""
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute('''
        SELECT b.*, u.full_name, u.location, u.id as seller_id
        FROM books b
        JOIN users u ON b.user_id = u.id
        WHERE b.id = %s
    ''', (book_id,))
    book = cursor.fetchone()

    if not book:
        cursor.close()
        conn.close()
        flash('Book not found!', 'danger')
        return redirect(url_for('browse_books'))


    cursor.execute('UPDATE books SET views = views + 1 WHERE id = %s', (book_id,))
    conn.commit()


    cursor.execute('''
        SELECT * FROM books
        WHERE category = %s AND id != %s AND status = "Available"
        LIMIT 4
    ''', (book['category'], book_id))
    similar_books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('book_detail.html', book=book, similar_books=similar_books)





@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':

        full_name = request.form.get('fullName', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')


        if not all([full_name, email, phone, location, password, confirm_password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        if not validate_email(email):
            flash('Invalid email format!', 'danger')
            return redirect(url_for('register'))

        if not validate_phone(phone):
            flash('Phone number must have at least 10 digits!', 'danger')
            return redirect(url_for('register'))

        if not validate_password(password):
            flash('Password must be at least 8 characters with at least one number!', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))


        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s OR phone = %s', (email, phone))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            flash('Email or phone number already registered!', 'danger')
            return redirect(url_for('register'))


        password_hash = generate_password_hash(password)

        try:
            cursor.execute('''
                INSERT INTO users (full_name, email, phone, password_hash, location)
                VALUES (%s, %s, %s, %s, %s)
            ''', (full_name, email, phone, password_hash, location))
            conn.commit()

            flash('Account created successfully! Please login.', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('login'))

        except Exception as e:
            conn.rollback()
            flash(f'Error creating account: {str(e)}', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email and password are required!', 'danger')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND is_active = TRUE', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))





@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()


    user = get_user_data(user_id)


    cursor.execute('''
        SELECT * FROM books WHERE user_id = %s ORDER BY created_at DESC
    ''', (user_id,))
    user_books = cursor.fetchall()


    cursor.execute('''
        SELECT
            COUNT(*) as total_books,
            SUM(CASE WHEN status = "Available" THEN 1 ELSE 0 END) as available_books,
            SUM(CASE WHEN status = "Sold" THEN 1 ELSE 0 END) as sold_books
        FROM books WHERE user_id = %s
    ''', (user_id,))
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', user=user, books=user_books, stats=stats)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user_id = session.get('user_id')
    user = get_user_data(user_id)
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    user_id = session.get('user_id')
    full_name = request.form.get('full_name', '').strip()
    location = request.form.get('location', '').strip()
    bio = request.form.get('bio', '').strip()

    if not full_name or not location:
        flash('Name and location are required!', 'danger')
        return redirect(url_for('profile'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET full_name = %s, location = %s, bio = %s
            WHERE id = %s
        ''', (full_name, location, bio, user_id))
        conn.commit()
        cursor.close()
        conn.close()


        session['full_name'] = full_name

        flash('Profile updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'danger')

    return redirect(url_for('profile'))





@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_book():
    """Add a new book for sale"""
    if request.method == 'POST':
        user_id = session.get('user_id')


        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        isbn = request.form.get('isbn', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        condition = request.form.get('condition', 'Good')
        publication_year = request.form.get('publication_year', '')
        pages = request.form.get('pages', '')
        language = request.form.get('language', 'English')


        if not all([title, author, category, price, condition]):
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('sell_book'))

        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            flash('Invalid price!', 'danger')
            return redirect(url_for('sell_book'))


        book_image = None
        if 'book_image' in request.files:
            file = request.files['book_image']
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    flash('Invalid file type! Allowed: PNG, JPG, JPEG, GIF, WEBP', 'danger')
                    return redirect(url_for('sell_book'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (user_id, title, author, isbn, category, description, price,
                                 book_condition, publication_year, pages, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, title, author, isbn, category, description, price, condition,
                  publication_year if publication_year else None, pages if pages else None, language))
            conn.commit()


            book_id = cursor.lastrowid


            if 'book_image' in request.files:
                file = request.files['book_image']
                if file and file.filename != '':
                    filename = save_book_image(file, book_id)
                    if filename:
                        cursor.execute('UPDATE books SET book_image = %s WHERE id = %s',
                                     (filename, book_id))
                        conn.commit()

            cursor.close()
            conn.close()
            flash('Book listed successfully!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'Error listing book: {str(e)}', 'danger')
            return redirect(url_for('sell_book'))

    return render_template('sell_book.html')

@app.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """Edit book listing"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute('SELECT * FROM books WHERE id = %s AND user_id = %s', (book_id, user_id))
    book = cursor.fetchone()
    cursor.close()
    conn.close()

    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        condition = request.form.get('condition', 'Good')
        status = request.form.get('status', 'Available')

        if not all([title, author, category, price, condition]):
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('edit_book', book_id=book_id))

        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            flash('Invalid price!', 'danger')
            return redirect(url_for('edit_book', book_id=book_id))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books SET title = %s, author = %s, category = %s,
                              description = %s, price = %s, book_condition = %s, status = %s
                WHERE id = %s AND user_id = %s
            ''', (title, author, category, description, price, condition, status, book_id, user_id))
            conn.commit()


            if 'book_image' in request.files:
                file = request.files['book_image']
                if file and file.filename != '':
                    if allowed_file(file.filename):

                        if book['book_image']:
                            old_path = os.path.join(app.config['UPLOAD_FOLDER'], book['book_image'])
                            if os.path.exists(old_path):
                                os.remove(old_path)


                        filename = save_book_image(file, book_id)
                        if filename:
                            cursor.execute('UPDATE books SET book_image = %s WHERE id = %s',
                                         (filename, book_id))
                            conn.commit()

            cursor.close()
            conn.close()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'Error updating book: {str(e)}', 'danger')
            return redirect(url_for('edit_book', book_id=book_id))

    return render_template('edit_book.html', book=book)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    """Delete book listing"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute('SELECT book_image FROM books WHERE id = %s AND user_id = %s', (book_id, user_id))
    book = cursor.fetchone()

    if not book:
        cursor.close()
        conn.close()
        flash('Book not found or unauthorized!', 'danger')
        return redirect(url_for('dashboard'))

    try:

        if book['book_image']:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], book['book_image'])
            if os.path.exists(image_path):
                os.remove(image_path)


        cursor.execute('DELETE FROM books WHERE id = %s AND user_id = %s', (book_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Book deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting book: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))





@app.route('/wishlist')
@login_required
def wishlist():
    """View user's wishlist"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT b.* FROM books b
        JOIN wishlist w ON b.id = w.book_id
        WHERE w.user_id = %s AND b.status = "Available"
        ORDER BY w.added_at DESC
    ''', (user_id,))
    wishlist_books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('wishlist.html', books=wishlist_books)

@app.route('/wishlist/add/<int:book_id>')
@login_required
def add_to_wishlist(book_id):
    """Add book to wishlist"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT IGNORE INTO wishlist (user_id, book_id) VALUES (%s, %s)
        ''', (user_id, book_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Added to wishlist'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/wishlist/remove/<int:book_id>')
@login_required
def remove_from_wishlist(book_id):
    """Remove book from wishlist"""
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            DELETE FROM wishlist WHERE user_id = %s AND book_id = %s
        ''', (user_id, book_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Removed from wishlist'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})





@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500





@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    user_id = session.get('user_id')
    user = None
    if user_id:
        user = get_user_data(user_id)
    return dict(current_user=user)





if __name__ == '__main__':
    # ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() in ('1', 'true', 'yes')
    app.run(debug=debug, host='0.0.0.0', port=port)