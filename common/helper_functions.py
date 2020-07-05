from django.contrib import messages


def issue_errors(request, form):
    for error in form.non_field_errors():
        messages.error(request, error)
    for field in form.visible_fields():
        if field.errors:
            messages.error(
                request,
                field.errors,
                extra_tags=F"field_errors {field.name}",
            )
