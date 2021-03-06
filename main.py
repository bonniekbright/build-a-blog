from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template("entry.html", blog_id = blog_id, blog=blog)
    
    blog_entries = Blog.query.all()

    return render_template('blog.html', title="Blog", 
    blog_entries=blog_entries)


@app.route('/new-entry', methods=["POST", "GET"])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title:
            error = "Blog entry must contain both a title and content"
            return render_template("new-entry.html", error=error, body=body)
        if not body:
            error = "Blog entry must contain both a title and content"
            return render_template("new-entry.html", error=error, title=title)
        title = request.form['title']
        body = request.form['body']
        new_entry = Blog(title, body)
        db.session.add(new_entry)
        db.session.commit()
        blog_id = new_entry.id
        blog = Blog.query.get(blog_id)
        return redirect("/blog?id=" + str(new_entry.id))
    return render_template('new-entry.html', page_title="Add a New Entry")

if __name__ == '__main__':
    app.run()
