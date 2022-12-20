from rest_framework.permissions import BasePermission

class Permisos(BasePermission):
    def has_permission(self, request, view):

        if request.method in ["GET", "POST"] and request.user.is_authenticated:
            return True

        if request.method in ['PUT', 'DELETE'] and request.user.is_authenticated and request.user.is_superuser:
            return True
        return False


""" 
Tomar en cuenta:

Django user models don't have the attribute is_admin.

The error is shown because somewhere in your code (probably login view?) 
you are calling user.is_admin.
 Find it and remove it, or use user.is_staff / user.is_superuser instead.


  """