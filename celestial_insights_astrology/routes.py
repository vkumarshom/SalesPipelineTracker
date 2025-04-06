import logging
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import urlsplit
from app import db
from models import Admin, BlogPost, Service, Booking, CartItem, Order, OrderItem, Contact
from forms import LoginForm, ContactForm, BlogPostForm, ServiceForm, BookingForm, CheckoutForm
from utils import get_session_id, generate_order_number, get_available_booking_slots, format_price, get_cart_total

def register_routes(app):
    # Add current_year to all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}
    
    # Home page
    @app.route('/')
    def index():
        services = Service.query.filter_by(is_available=True).limit(3).all()
        recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
        return render_template('index.html', services=services, recent_posts=recent_posts)

    # About page
    @app.route('/about')
    def about():
        return render_template('about.html')

    # Contact page
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(contact)
            db.session.commit()
            flash('Your message has been sent! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    # Blog routes
    @app.route('/blog')
    def blog():
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=6)
        return render_template('blog/index.html', posts=posts)

    @app.route('/blog/<slug>')
    def blog_post(slug):
        post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
        return render_template('blog/post.html', post=post)

    # Shop/Services routes
    @app.route('/services')
    def services():
        services = Service.query.filter_by(is_available=True).all()
        return render_template('shop/index.html', services=services)

    @app.route('/services/<slug>')
    def service_detail(slug):
        service = Service.query.filter_by(slug=slug, is_available=True).first_or_404()
        return render_template('shop/product.html', service=service)

    # Cart routes
    @app.route('/cart')
    def cart():
        session_id = get_session_id()
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        total = get_cart_total(cart_items)
        return render_template('shop/cart.html', cart_items=cart_items, total=total, format_price=format_price)

    @app.route('/cart/add', methods=['POST'])
    def add_to_cart():
        service_id = request.form.get('service_id', type=int)
        session_id = get_session_id()
        
        service = Service.query.get_or_404(service_id)
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(session_id=session_id, service_id=service_id).first()
        
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(session_id=session_id, service_id=service_id, quantity=1)
            db.session.add(cart_item)
        
        db.session.commit()
        flash(f"{service.name} added to your cart!", "success")
        return redirect(url_for('cart'))

    @app.route('/cart/update', methods=['POST'])
    def update_cart():
        item_id = request.form.get('item_id', type=int)
        quantity = request.form.get('quantity', type=int)
        
        if not quantity or quantity < 1:
            flash("Quantity must be at least 1", "error")
            return redirect(url_for('cart'))
        
        cart_item = CartItem.query.get_or_404(item_id)
        
        # Verify the cart item belongs to the current session
        if cart_item.session_id != get_session_id():
            abort(403)
        
        cart_item.quantity = quantity
        db.session.commit()
        flash("Cart updated", "success")
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:item_id>', methods=['POST'])
    def remove_from_cart(item_id):
        cart_item = CartItem.query.get_or_404(item_id)
        
        # Verify the cart item belongs to the current session
        if cart_item.session_id != get_session_id():
            abort(403)
        
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart", "success")
        return redirect(url_for('cart'))

    # Checkout
    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        session_id = get_session_id()
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            flash("Your cart is empty", "error")
            return redirect(url_for('cart'))
        
        total = get_cart_total(cart_items)
        form = CheckoutForm()
        
        if form.validate_on_submit():
            # Create order
            order = Order(
                order_number=generate_order_number(),
                customer_name=form.customer_name.data,
                customer_email=form.customer_email.data,
                customer_phone=form.customer_phone.data,
                total_amount=total,
                status='paid'  # In a real app, this would be 'pending' until payment confirmation
            )
            db.session.add(order)
            db.session.flush()  # Get order ID before committing
            
            # Create order items
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    service_id=cart_item.service_id,
                    service_name=cart_item.service.name,
                    price=cart_item.service.price,
                    quantity=cart_item.quantity
                )
                db.session.add(order_item)
            
            # Clear the cart
            for item in cart_items:
                db.session.delete(item)
            
            db.session.commit()
            flash("Your order has been placed successfully!", "success")
            return redirect(url_for('index'))
        
        return render_template('shop/checkout.html', form=form, cart_items=cart_items, total=total, format_price=format_price)

    # Booking routes
    @app.route('/booking', methods=['GET', 'POST'])
    def booking():
        form = BookingForm()
        
        # Populate service choices
        form.service_id.choices = [(s.id, f"{s.name} - {format_price(s.price)} - {s.duration} min") 
                                   for s in Service.query.filter_by(is_available=True).all()]
        
        if form.validate_on_submit():
            booking = Booking(
                service_id=form.service_id.data,
                customer_name=form.customer_name.data,
                customer_email=form.customer_email.data,
                customer_phone=form.customer_phone.data,
                booking_date=form.booking_date.data,
                booking_time=datetime.strptime(form.booking_time.data, '%H:%M').time(),
                notes=form.notes.data,
                status='confirmed'  # In a real app, this might be 'pending' until reviewed
            )
            db.session.add(booking)
            db.session.commit()
            return redirect(url_for('booking_confirmation', booking_id=booking.id))
        
        return render_template('booking/calendar.html', form=form)

    @app.route('/booking/get_slots', methods=['GET'])
    def get_booking_slots():
        service_id = request.args.get('service_id', type=int)
        date_str = request.args.get('date')
        
        if not service_id or not date_str:
            return jsonify({'error': 'Missing parameters'}), 400
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        service = Service.query.get_or_404(service_id)
        
        # Get all bookings for the day
        day_bookings = Booking.query.filter(
            Booking.booking_date == date_obj,
            Booking.status != 'cancelled'
        ).all()
        
        # Format booked slots
        booked_slots = []
        for booking in day_bookings:
            start_time = datetime.combine(date_obj, booking.booking_time)
            end_time = start_time + timedelta(minutes=service.duration)
            booked_slots.append((start_time, end_time))
        
        # Get available slots
        available_slots = get_available_booking_slots(service.duration, date_obj, booked_slots)
        
        return jsonify({'slots': available_slots})

    @app.route('/booking/confirmation/<int:booking_id>')
    def booking_confirmation(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        return render_template('booking/confirmation.html', booking=booking)

    # Admin routes
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(username=form.username.data).first()
            if admin is None or not admin.check_password(form.password.data):
                flash('Invalid username or password', 'error')
                return redirect(url_for('admin_login'))
            
            login_user(admin, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('admin_dashboard')
            return redirect(next_page)
        
        return render_template('admin/login.html', form=form)

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_dashboard():
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
        unread_contacts = Contact.query.filter_by(is_read=False).count()
        
        return render_template('admin/dashboard.html', 
                             recent_orders=recent_orders, 
                             recent_bookings=recent_bookings,
                             unread_contacts=unread_contacts)

    @app.route('/admin/blog')
    @login_required
    def admin_blog_posts():
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        return render_template('admin/blog_posts.html', posts=posts)

    @app.route('/admin/blog/new', methods=['GET', 'POST'])
    @login_required
    def admin_new_post():
        form = BlogPostForm()
        if form.validate_on_submit():
            post = BlogPost(
                title=form.title.data,
                slug=form.slug.data,
                summary=form.summary.data,
                content=form.content.data,
                image_url=form.image_url.data,
                published=form.published.data
            )
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('admin_blog_posts'))
        return render_template('admin/blog_form.html', form=form, is_edit=False)

    @app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        form = BlogPostForm(obj=post)
        
        if form.validate_on_submit():
            form.populate_obj(post)
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('admin_blog_posts'))
        
        return render_template('admin/blog_form.html', form=form, is_edit=True, post=post)

    @app.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
    @login_required
    def admin_delete_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('admin_blog_posts'))

    @app.route('/admin/services')
    @login_required
    def admin_services():
        services = Service.query.all()
        return render_template('admin/products.html', services=services)

    @app.route('/admin/services/new', methods=['GET', 'POST'])
    @login_required
    def admin_new_service():
        form = ServiceForm()
        if form.validate_on_submit():
            service = Service(
                name=form.name.data,
                slug=form.slug.data,
                short_description=form.short_description.data,
                description=form.description.data,
                price=form.price.data,
                duration=form.duration.data,
                image_url=form.image_url.data,
                is_available=form.is_available.data
            )
            db.session.add(service)
            db.session.commit()
            flash('Service created successfully!', 'success')
            return redirect(url_for('admin_services'))
        return render_template('admin/service_form.html', form=form, is_edit=False)

    @app.route('/admin/services/edit/<int:service_id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_service(service_id):
        service = Service.query.get_or_404(service_id)
        form = ServiceForm(obj=service)
        
        if form.validate_on_submit():
            form.populate_obj(service)
            db.session.commit()
            flash('Service updated successfully!', 'success')
            return redirect(url_for('admin_services'))
        
        return render_template('admin/service_form.html', form=form, is_edit=True, service=service)

    @app.route('/admin/services/delete/<int:service_id>', methods=['POST'])
    @login_required
    def admin_delete_service(service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully!', 'success')
        return redirect(url_for('admin_services'))

    @app.route('/admin/bookings')
    @login_required
    def admin_bookings():
        bookings = Booking.query.order_by(Booking.booking_date.desc(), Booking.booking_time).all()
        return render_template('admin/bookings.html', bookings=bookings)
    
    @app.route('/admin/bookings/update/<int:booking_id>', methods=['POST'])
    @login_required
    def admin_update_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        status = request.form.get('status')
        
        if status in ['pending', 'confirmed', 'cancelled']:
            booking.status = status
            db.session.commit()
            flash('Booking status updated', 'success')
        else:
            flash('Invalid status', 'error')
            
        return redirect(url_for('admin_bookings'))

    # Initialize admin user
    @app.route('/init_admin', methods=['GET'])
    def init_admin():
        # This is a development route to create an initial admin user
        # In production, this should be removed or secured
        if Admin.query.first() is None:
            admin = Admin(username='admin', email='admin@example.com')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()
            return "Admin created"
        return "Admin already exists"

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
