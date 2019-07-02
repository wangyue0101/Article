import os

from flask import render_template, request, abort, redirect, url_for, flash
from werkzeug.utils import secure_filename


def init_views(app):
    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files.get("file")
            print(file)

            if not file:
                abort(400)

            print(secure_filename(file.filename))

            abs_path = os.path.abspath(os.path.dirname(__name__))
            # file_path = os.path.join(abs_path, r"templates\uploads")
            file.save(abs_path, secure_filename(file.filename))
            return redirect(url_for("upload_file"))

        return render_template("upload_file.html")

    @app.template_filter("list_rever")
    def do_list_rever(li):
        temp_list = li
        temp_list.reverse()
        return temp_list

    @app.template_filter("md")
    def markdown_to_html(md):
        from markdown import markdown
        return markdown(md)

    def read_md(filename):
        from functools import reduce
        import os
        file_path = os.path.abspath(os.path.join(r"E:/flask_pro_manage", filename))
        print(file_path)
        with open(file_path, encoding="utf8") as f:
            content = reduce(lambda x, y: x + y, f.readlines())

        return content

    @app.context_processor
    def inject_context():
        return dict(read_md=read_md)

    @app.template_test("current_url")
    def check_url(url):
        print(request.url, url, request.path)
        if url == request.url:
            return True
        else:
            return False
