def add_url_rule (blueprint, *args):
    for ViewClass in args:
        blueprint.add_url_rule(ViewClass.route_path, view_func=ViewClass.as_view(ViewClass.route_name), methods=ViewClass.methods)


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
