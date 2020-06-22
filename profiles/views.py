from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import FormView

from profiles.forms import UserProfileForm
from profiles.models import Profile


class UserProfileView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    template_name = 'profiles/form.html'
    success_url = '/'

    def set_form(self, request):
        user = request.user
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        try:
            my_profile = user.profile
        except ObjectDoesNotExist:
            my_profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                raise Exception('Something went wrong.')
        form = self.form_class(request.POST or None, instance=my_profile, initial=user_data)

        return form, user

    def post(self, request, *args, **kwargs):
        form, user = self.set_form(request)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            profile_obj.save()
            return redirect(self.success_url)
        context = {
            "form": form,
            "btn_label": "Save",
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form, user = self.set_form(request)
        context = {
            "form": form,
            "btn_label": "Save",
        }
        return render(request, self.template_name, context)
