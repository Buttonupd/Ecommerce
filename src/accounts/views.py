from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DeleteView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

# from ecommer
