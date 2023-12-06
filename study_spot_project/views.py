# REFERENCES
# Title: Simple modal to open details of an item (Django + bootstrap)
# Author: Antoine Garcia
# URL: https://medium.com/@antoinewg/simple-modal-to-open-details-of-an-item-django-bootstrap-ffeeb11f12c1

# Title: Modal
# URL: https://getbootstrap.com/docs/5.0/components/modal/
# Software License: MIT


from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
import httpx    
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView
from .models import Place, UnacceptedPlace, Review, UserProfile
from django.views.generic.edit import UpdateView
from .forms import ReviewForm, PlaceForm, RejectionForm
from .filters import PlaceFilter
from operator import itemgetter
from django.contrib import messages

def get_max_rating(place):
    reviews = Review.objects.filter(place=place)
    max_rating = max(
        reviews,
        key=lambda review: max(
            review.noise_level_rating,
            review.space_rating,
            review.open_seats_rating,
        ),
        default=None,
    )

    if max_rating:
        max_category = max(
            [
                ('Noise Level', max_rating.noise_level_rating),
                ('Space', max_rating.space_rating),
                ('Open Seats', max_rating.open_seats_rating),
            ],
            key=lambda x: x[1],
        )
        return {'category': max_category[0], 'rating': max_category[1]}
    else:
        return None

def home(request):
    user = request.user
    is_admin = request.user.groups.filter(name='Admin').exists()
    # check if the user needs to see the user type select modal
    display_modal = False
    if user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
        user_profile = UserProfile.objects.get(user=request.user)
        owner_deletion_message = user_profile.deletion_message
        if owner_deletion_message:
            messages.success(request, owner_deletion_message)
            user_profile.deletion_message = ""
            user_profile.save()
        if UserProfile.objects.filter(user_id=user.id).exists():
            user_profile = UserProfile.objects.get(user_id=user.id)
            has_seen_modal = user_profile.has_seen_modal
        
            if not has_seen_modal:
                user_profile.has_seen_modal = True
                user_profile.save()
                display_modal = True
    
    # Get top three rated study spots
    top_study_spots = Place.objects.order_by('-average_rating')[:3]

    # Get best-rated category of a top study spot
    for place in top_study_spots:
        place.max_rating = get_max_rating(place)

    context = {
        'is_admin': is_admin,
        'top_study_spots': top_study_spots,
        'display_modal' : display_modal,
    }

    return render(request, 'home.html', context)

def staff(request):
    user = request.user
    is_admin = request.user.groups.filter(name='Admin').exists()
    unaccepted_places = UnacceptedPlace.objects.filter(rejection_message='')
    users = User.objects.all()
    context = {
        'is_admin': is_admin,
        'unaccepted_places': unaccepted_places,
        'users': users
    }
    return render(request, 'staff.html', context)

def map(request):
    is_admin = request.user.groups.filter(name='Admin').exists()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        owner_deletion_message = user_profile.deletion_message
        if owner_deletion_message:
            messages.success(request, owner_deletion_message)
            user_profile.deletion_message = ""
            user_profile.save()
    if is_admin:
        return redirect('admin_map')
    else:
        places = Place.objects.all()
        filter = PlaceFilter(request.GET, queryset=places)
        context = {
            'places' : places,
            'is_admin': is_admin,
            'filter': filter
        }
        return render(request, 'map.html', context)

def logout_view(request):
    token = request.session.get("google_sso_access_token")
    messages.success(request, "You have succesfully logged out")
    logout(request)

    # You can revoke the Access Token here
    if token:
        httpx.post("https://oauth2.googleapis.com/revoke", params={"token": token})
    return HttpResponseRedirect("home")

def admin_map(request):
    unaccepted_places = UnacceptedPlace.objects.filter(rejection_message='')
    accepted_places = Place.objects.all()
    is_admin = request.user.groups.filter(name='Admin').exists()
    user_profile = UserProfile.objects.get(user=request.user)
    owner_deletion_message = user_profile.deletion_message
    if owner_deletion_message:
        messages.success(request, owner_deletion_message)
        user_profile.deletion_message = ""  
        user_profile.save()

    context = {
        'unaccepted_places' : unaccepted_places,
        'accepted_places' : accepted_places,
        'is_admin': is_admin,
    }
    return render(request, 'admin_map.html', context)

#consulted Django documentation on Create View: https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/
class PlaceCreateView(CreateView):
    model = Place
    form_class = PlaceForm
    template_name = "add.html"

    def get_context_data(self, **kwargs):
        context = super(PlaceCreateView, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.groups.filter(name='Admin').exists()
        return context

    def form_valid(self, form):
        name = form.cleaned_data['name']
        form.instance.user = self.request.user
        if Place.objects.filter(name__iexact=name).exists() or UnacceptedPlace.objects.filter(name__iexact=name).exists():
            form.add_error('name', 'A study spot with this name already exists (if you dont see it on the map it might not be approved yet).')
            return self.form_invalid(form)
        messages.success(self.request, 'Study Spot Created. Pending Approval')
        return super(PlaceCreateView, self).form_valid(form)

def place_details(request, place_name_slug):
    unacc = False
    review_form = None
    rej_form = None
    user_has_submitted_review = False

    is_admin = request.user.groups.filter(name='Admin').exists()
    

    try:
        place = get_object_or_404(Place, name_slug=place_name_slug)
        reviews = place.review_set.all()
    except:
        unacc = True
        place = get_object_or_404(UnacceptedPlace, name_slug=place_name_slug)
        reviews = None

    is_admin = request.user.groups.filter(name='Admin').exists()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        owner_deletion_message = user_profile.deletion_message
        if owner_deletion_message:
            messages.success(request, owner_deletion_message)
            user_profile.deletion_message = ""
            user_profile.save()
    if request.user.is_authenticated and not unacc: 
        user_has_submitted_review = Review.objects.filter(user=request.user, place=place).exists()

        if not user_has_submitted_review:
            if request.method == 'POST':
                review_form = ReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.place = place
                    review.user = request.user
                    review.save()
                    messages.success(request, "You have succesfully posted a review.")
                    return redirect('place_details', place_name_slug=place_name_slug)
            
            else:
                review_form = ReviewForm()

    if is_admin and unacc:
        if request.method == 'POST':
            rej_form = RejectionForm(request.POST)
            if rej_form.is_valid():
                place.name = place.name + str(place.id) + "_rej"
                place.rejection_message = rej_form.cleaned_data['rejection_message']
                place.save()
                deletion_message = f"Place '{place.name[:-4 - len(str(place.id))      ]}' deleted."
                messages.success(request, deletion_message)

                user_profile, created = UserProfile.objects.get_or_create(user=place.user)
                deletion_message = f"Place '{place.name[:-4-len(str(place.id))]}' deleted for: {place.rejection_message}."
                user_profile.deletion_message = deletion_message
                user_profile.save()

                request.session['owner_deletion_message'] = deletion_message

                return redirect('admin_map')

        else:
            rej_form = RejectionForm

    context = {
        'place': place,
        'place_name_slug': place_name_slug,
        'is_admin': is_admin,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_submitted_review': user_has_submitted_review,
        'rej_form': rej_form,
    }

    template_name = 'unapp_place_detail.html' if unacc else 'place_detail.html'
    return render(request, template_name, context)

def delete_unapproved(request, place_name_slug):
    unacc_place = get_object_or_404(UnacceptedPlace, name_slug=place_name_slug)
    deletion_message = f"Place '{unacc_place.name}' deleted."
    messages.success(request, deletion_message)
    unacc_place.delete()
    return redirect('admin_map')

def approve_unapproved(request, place_name_slug):
    unacc_place = get_object_or_404(UnacceptedPlace, name_slug=place_name_slug)
    acc_place = Place()
    acc_place.lat = unacc_place.lat
    acc_place.long = unacc_place.long
    acc_place.name = unacc_place.name
    acc_place.place_description = unacc_place.place_description
    acc_place.average_rating = 0
    acc_place.name_slug = unacc_place.name_slug

    acc_place.save()
    unacc_place.delete()
    messages.success(request, "Study Spot Approved")
    return redirect('admin_map')

def select_user_type(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user_type = request.POST.get('user_type')
        if user_type == 'Users':
            user_group = Group.objects.get(name='Users')
            request.user.groups.add(user_group)
            request.user.save()
        elif user_type == 'Admin':
            user_group = Group.objects.get(name='Admin')
            request.user.groups.add(user_group)
            request.user.save()
    return HttpResponse(status=200) 
  
def remove_place(request, place_name_slug):
    place = get_object_or_404(Place, name_slug = place_name_slug)
    place.delete()
    messages.success(request, "You have succesfully deleted a Study Spot.")
    return redirect('admin_map')

def delete_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_to_delete = User.objects.get(username=user_name)
        user_to_delete.delete()

#consulted Django documentation on Update View: https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/
#consulted YouTube tutorial on implementing Update View by Coding Entrepreneurs: https://www.youtube.com/watch?v=KB_wDXBwhUA&t=222s
class PlaceUpdateView(UpdateView):
    model = Place
    template_name = "add.html"
    form_class = PlaceForm
    
    def get_context_data(self, **kwargs):
        context = super(PlaceUpdateView, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.groups.filter(name='Admin').exists()
        return context

    def get_object(self):
        place_id = self.kwargs.get('place_name_slug')
        return get_object_or_404(Place, name_slug = place_id)
    
    def form_valid(self, form):
        new_name = form.cleaned_data.get('name')
        existing_place = Place.objects.exclude(id=self.object.id).filter(name=new_name)
        existing_unapp_place = UnacceptedPlace.objects.exclude(id=self.object.id).filter(name=new_name)

        if existing_place.exists():
            form.add_error('name', 'A Study Spot with this name is already on the map.')
            return self.form_invalid(form)
        if existing_unapp_place.exists():
            form.add_error('name', 'A Study Spot with this name is being currently being approved.')
            return self.form_invalid(form)

        return super(PlaceUpdateView, self).form_valid(form)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('map')

def profile(request, user_id):
    profile_user = get_object_or_404(User, id = user_id)
    is_profile_admin = profile_user.groups.filter(name='Admin').exists()
    is_admin = request.user.groups.filter(name='Admin').exists()
    reject_unaccepted_places = False
    wait_unaccepted_places = False
    if request.user == profile_user or is_admin:
        wait_unaccepted_places = UnacceptedPlace.objects.filter(user=profile_user, rejection_message='')
        reject_unaccepted_places = UnacceptedPlace.objects.filter(user=profile_user).exclude(rejection_message='')
        for place in reject_unaccepted_places:
            place.name = place.name[:-4-len(str(place.id))]
    reviews = Review.objects.filter(user=profile_user)

    context = {
        'profile_user': profile_user,
        'is_admin': is_admin,
        'wait_unaccepted_places': wait_unaccepted_places,
        'reject_unaccepted_places': reject_unaccepted_places,
        'reviews' : reviews,
        'is_profile_admin' : is_profile_admin,
    }
    return render(request, 'profile.html', context)