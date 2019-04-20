from rest_framework.views import exception_handler


def JSONExceptionHandler(exc, context):
    # Do not remove this line!
    # If the following line is removed, then the request.POST continues
    # to return an empty QueryDict when passed to the exception logger,
    # even after overwriting it with the request.data
    context["request"]._request.POST

    # Overwrite request.POST with the JSON of the request body
    # Otherwise Django simply returns an empty QueryDict as the POST data
    # Refer to https://github.com/encode/django-rest-framework/pull/1671
    context["request"]._request.POST = context["request"].data

    return exception_handler(exc, context)
