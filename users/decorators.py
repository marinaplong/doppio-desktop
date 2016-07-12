from rest_framwework.exceptions import PermissionDenied, NotFound, ValidationError
rfom django.core.exceptions import ObjectDoesNotExist
from alverna.models import Company
from accounts.models import User, Invitation, PasswordReset
from django.http import HttpResponseForbidden
from rest_framework_jwt.settings import api_settings

def manual_token_request(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            token = request.GET.get("token", None)
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            try:
                payload = jwt_decode_handler(token)
            except:
                return HttpResponseForbidden("Not allowed access to this page")
            try:
                user = User.objects.get(id=payload.get("user_id"))
            except:
                return HttpResponseForbidden("Not allowed to access this page")
            request.payload = payload
            request.user = user
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view
    if function is None:
        return _dec
    else:
        return _dec(function)

def user_request(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if "user_id" in kwargs:
                user_id = kwargs.pop("user_id")
                try:
                    request.found_user = User.objects.get(id=user_id)
                except:
                    raise NotFound("User cannot be found")
            else:
                raise ValidationError("Expected a user ID with parameter `user_id`")
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

def invitation_request(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            key = request.query_params.get("key", None)
            try:
                invitation = Invitation.objects.get(key=key)
            except:
                raise NotFound("Could not find invitation with that key")
            if not invitation.valid:
                raise ValidationError("Invitation is invalid")
            elif invitation.user.is_active:
                raise ValidationError("User has already accepted his/her invite")
            request.invitation = invitation
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)



def verify_forgot_password_request(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            key = request.query_params.get("key", None)
            try:
                password_reset = PasswordReset.objects.get(key=key)
            except:
                raise NotFound("Could not find password reset with that key")
            if not password_reset.valid:
                raise ValidationError("Password reset is invalid")
            request.password_reset = password_reset
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
