# student/mixins.py

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class StudentRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'student_user'):
            return redirect('dashboard')  # Redirige vers le dashboard si pas un étudiant
        return super().dispatch(request, *args, **kwargs)
