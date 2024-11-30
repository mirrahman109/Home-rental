from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Property, db
import os
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import func

main = Blueprint('main', __name__)



# Set the homepage route to display properties directly
@main.route('/', methods=['GET'])
def home():
    query = request.args.get('query')
    print(f"Query: {query}")  # Debug print
    try:
        if query:
            properties = Property.query.filter(Property.title.ilike(f'%{query}%')).all()
        else:
            properties = Property.query.all()
        print(f"Properties fetched: {properties}")  # Debug print

        cities = (
            db.session.query(
                Property.city,  # Ensure this column exists
                func.count(Property.id).label('property_count')
            )
            .group_by(Property.city)
            .all()
        )
        print(f"Cities: {cities}")  # Debug print
        
        return render_template('index.html', properties=properties, cities=cities)
    except Exception as e:
        print(f"Error in home route: {e}")  # Log the error
        return "An internal error occurred.", 500
# Admin Blueprint remains the same
admin = Blueprint('admin', __name__)

# Route to add a new property
@admin.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        available_from = request.form['available_from']
        price = request.form['price']
        address = request.form['address']

        # Handle image upload
        image_file = request.files['image']
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            # Save image filename to the database
            new_property = Property(
                title=title,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                available_from=available_from,
                price=price,
                address=address,
                image=f'roomimages/{filename}'
            )
            db.session.add(new_property)
            db.session.commit()
            flash('Property added successfully!', 'success')
        return redirect(url_for('admin.add_property'))

    return render_template('add_property.html')

# Route to edit a property
@admin.route('/edit_property/<int:id>', methods=['GET', 'POST'])
def edit_property(id):
    property = Property.query.get_or_404(id)
    if request.method == 'POST':
        # Update property details
        property.title = request.form['title']
        property.bedrooms = request.form['bedrooms']
        property.bathrooms = request.form['bathrooms']
        property.available_from = request.form['available_from']
        property.price = request.form['price']
        property.address = request.form['address']
        property.image = request.form['image']
        
        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('admin.edit_property', id=property.id))
    
    return render_template('edit_property.html', property=property)

# Route to delete a property
@admin.route('/delete_property/<int:id>', methods=['POST'])
def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('main.home'))  # Redirect to the main index page

@admin.route('/dashboard')
def dashboard():
    properties = Property.query.all()
    return render_template('dashboard.html', properties=properties)

@admin.route('/listings', methods=['GET'])
def city_listings():
    city = request.args.get('city')
    if city:
        properties = Property.query.filter(Property.address == city).all()
    else:
        properties = Property.query.all()  # Fallback: show all properties

    return render_template('listings.html', properties=properties, city=city)


if __name__ == "__main__":
    app.run(debug=True)

