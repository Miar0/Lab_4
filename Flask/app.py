import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

image_formats = ["jpeg", "png", "gif"]
str_formats = '.jpeg, .png, .gif'
path_gallery = r"C:\Code\Flask\static\gallery"


@app.route('/')
def home():
    categories = os.listdir(path_gallery)
    return render_template('home.html', categories=categories)


@app.route('/create_category', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        name_category = request.form['category']
        if len(name_category) <= 20:
            os.makedirs(os.path.join(path_gallery, name_category), exist_ok=True)
            return redirect(url_for('home'))
        else:
            print('Error')
            return redirect(url_for('create_category', massage='Назва повинна бути меншою або рівною 20 символам.'))

    message = request.args.get('massage')

    return render_template('create_category.html', message=message)


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    categories = os.listdir(path_gallery)

    if request.method == 'POST':
        image = request.files.get('image')
        select_category = request.form['category']

        if select_category in categories:
            if image.filename.split('.')[-1].lower() in image_formats:
                category_path = os.path.join(path_gallery, select_category)
                image.save(os.path.join(category_path, image.filename))
                return redirect(url_for('home'))
            else:
                return redirect(url_for('upload_image', massage=f"Тип фотографії повинен бути {str_formats}"))

    message = request.args.get('massage')

    return render_template('upload_image.html', category=categories, message=message)


@app.route('/category/<name>')
def category(name):
    category_path = os.path.join(path_gallery, name)
    images = os.listdir(category_path) if os.path.exists(category_path) else []
    return render_template('category.html', name=name, images=images)

@app.route('/rename_category/<category>', methods=['POST'])
def rename_category(category):
    categories = os.listdir(path_gallery)
    new_name = request.form['rename']
    if not new_name in categories:
        path_category = os.path.join(path_gallery, category)
        path_new_name = os.path.join(path_gallery, new_name)

        if path_new_name != path_category:
            os.rename(path_category, path_new_name)

    return redirect(url_for('home', name=categories))

@app.route('/delete_category/<category>', methods=['POST'])
def delete_category(category):
    shutil.rmtree(os.path.join(path_gallery, category))
    categories = os.listdir(path_gallery)
    return redirect(url_for('home', name=categories))

@app.route('/delete_image/<category>/<filename>', methods=['POST'])
def delete_image(category, filename):
    os.remove(os.path.join(path_gallery, category, filename))
    return redirect(url_for('category', name=category))


@app.route('/gallery/<category>/<filename>')
def send_image(category, filename):
    return send_from_directory(os.path.join(path_gallery, category), filename)


if __name__ == '__main__':
    app.run(debug=True)
