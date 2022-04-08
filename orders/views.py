from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.generic import ListView
from django.views.generic.edit import FormView

# local app
from orders.models import Order
from account.models import UserBase
from orders.forms import OrderIssue

# Views


class OrderView(ListView):
    model = Order
    template_name = "account/dashboard/user_orders.html"
    context_object_name = "orders"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_id = request.user.id

    def get_queryset(self):
        user_orders = Order.objects.filter(user_id=self.user_id).filter(billing_status=True)
        return user_orders


class OrderIssueView(FormView):
    template_name = "account/order_issue.html"
    form_class = OrderIssue

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.order_key = self.kwargs["order_key"]
        self.user_id = self.request.user.id
        self.user = UserBase.objects.get(id=self.user_id)
        try:
            # Check if user have this order, prevent other fetch order information through url
            self.order = Order.objects.get(order_key=self.order_key, user_id=self.user.id)
        except ObjectDoesNotExist:
            raise PermissionDenied

    def get_initial(self):
        initial = {"email": self.user.email, "orderid": self.order.order_key}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_issue_form"] = self.get_form
        context["order"] = self.order
        return context

    def post(self, request, **kwargs):
        order_issue_form = self.get_form()
        if order_issue_form.is_valid():
            current_site = get_current_site(request)
            subject = "Order Issue, order key: {orderkey}".format(orderkey=self.order_key)
            message = render_to_string(
                "account/order_issue_email.html",
                context={
                    "user": self.user,
                    "order_id": self.order_key,
                    "site_name": current_site,
                },
            )
            self.user.email_user(subject=subject, message=message)
            return render(
                request,
                "account/order_issue_email_success.html",
                status=201,
            )
