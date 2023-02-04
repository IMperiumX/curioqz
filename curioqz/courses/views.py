from braces import views
from django.views.generic import TemplateView


def print_mro(cls):
    print(", ".join(c.__name__ for c in cls.mro()))


"""

django braces

"""


class SomeSecretView(views.LoginRequiredMixin, TemplateView):
    template_name = "path/to/template.html"

    # optional
    login_url = "/signup/"
    redirect_field_name = "hollaback"
    raise_exception = True

    def get(self, request):
        return self.render_to_response({})


class SomeProtectedView(
    views.LoginRequiredMixin, views.PermissionRequiredMixin, TemplateView
):
    permission_required = "auth.change_user"
    template_name = "path/to/template.html"
