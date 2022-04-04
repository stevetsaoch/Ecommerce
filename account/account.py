def formdata_extract(form, request_data):
    dict = {}
    fields = form.Meta.fields
    for field in fields:
        if isinstance(form.fields[field], forms.ImageField) or isinstance(form.fields[field], forms.FileField):
            pass
        else:
            if field == "customer" or field == "full_name":
                dict[field] = ""
            else:
                dict[field] = request_data.POST[field]
    return dict