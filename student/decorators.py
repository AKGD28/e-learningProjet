# student/decorators.py

from django.shortcuts import redirect
from functools import wraps

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'student_user'):
            return view_func(request, *args, **kwargs)
        else:
            # Rediriger vers le dashboard de l'instructeur ou afficher une page 403
            return redirect('dashboard')  # Ou utiliser: raise PermissionDenied
    return _wrapped_view
