from flask import render_template


class IndexController:
    def get_index(self) -> str:
        return render_template("index.html")
