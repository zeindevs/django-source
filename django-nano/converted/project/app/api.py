from datetime import datetime

from nanodjango import Django
from ninja import NinjaAPI

from .models import Comment


class CommentSchema(app.ninja.Schema):
    id: int
    text: str
    created: datetime


app = Django()
api = NinjaAPI()


@api.get("/comments", response=list[CommentSchema])
def api_comments(request):
    comments = Comment.objects.order_by("-created")
    return comments
