from django.shortcuts import redirect
from django.utils.timezone import timedelta
from users.models import Profile

max_request = 2

def user_session_cap(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            ## if the user is an admin he doesn't have a cap
            if group == "admin":
                return view_function(request, *args, **kwargs)
            ## otherwise we must define a cap
            else:

                ## if the time session age is equal to the value define in settings
                ## by SESSION_COOKIE_AGE then the expiry is set
                if request.session.get_expiry_age() == 1000:
                    request.session.set_expiry(int(timedelta(days=1).total_seconds()))
                ## we count the number of requests made
                num_request = request.session.get("num_request", 0) + 1
                request.session["num_request"] = num_request

                ## if it is superior to the cap we just stay on the home page
                if num_request > max_request:
                    return redirect("index")
                ## otherwise the result view executes normally
                else:
                    return view_function(request, *args, **kwargs)

    return wrapper_function
