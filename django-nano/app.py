# /// script
# dependencies = ["nanodjango"]
# ///

from django.db import models
from django.shortcuts import render
from nanodjango import Django
from datetime import datetime

app = Django()


@app.admin
class Comment(models.Model):
    text = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class CommentSchema(app.ninja.Schema):
    id: int
    text: str
    created: datetime


@app.api.get("/comments", response=list[CommentSchema])
def api_comments(request):
    comments = Comment.objects.order_by("-created")
    return comments


@app.route("/comments/")
def comments(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        Comment.objects.create(text=comment)

    comments = Comment.objects.order_by("-created")
    context = {"comments": comments}
    return render(request, "index.html", context)


if __name__ == "__main__":
    app.run()

