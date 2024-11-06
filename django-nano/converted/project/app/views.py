import inspect
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render

from .models import Comment


def ensure_http_response(view_fn):
    """
    If a view returns a plain string value, convert it into an HttpResponse
    """
    if inspect.iscoroutinefunction(view_fn):

        @wraps(view_fn)
        async def wrapped(*args, **kwargs):
            response = await view_fn(*args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            return HttpResponse(response)

    else:

        @wraps(view_fn)
        def wrapped(*args, **kwargs):
            response = view_fn(*args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            return HttpResponse(response)

    return wrapped


@ensure_http_response
def comments(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        Comment.objects.create(text=comment)
    comments = Comment.objects.order_by("-created")
    context = {"comments": comments}
    return render(request, "index.html", context)
