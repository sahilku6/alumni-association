# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum
from .models import Profile, Job, Event, SuccessStory, Donation, JobApplication
from .forms import UserRegistrationForm, ProfileForm, DonationForm, JobForm, EventForm, SuccessStoryForm, JobApplicationForm

def index(request):
    featured = SuccessStory.objects.filter(featured=True)[:3]
    upcoming = Event.objects.filter(start__gte=timezone.now()).order_by('start')[:5]
    # total donations across all users
    total = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    # total donated by current user (if logged in)
    user_total = None
    if request.user.is_authenticated:
        user_total = Donation.objects.filter(donor=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'index.html', {
        'featured': featured,
        'upcoming': upcoming,
        'total_donations': total,
        'user_total_donated': user_total,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # avoid UNIQUE constraint if a Profile was already created by signals
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.profile
    # Only show stories created by the logged-in user on their dashboard
    recent_stories = SuccessStory.objects.filter(author=request.user).order_by('-created_at')[:5]
    # Show ONLY upcoming events created by the logged-in user
    upcoming_events = Event.objects.filter(
        created_by=request.user,
        start__gte=timezone.now()
    ).order_by('start')[:5]
    return render(request, 'alumni/dashboard.html', {
        'profile': profile,
        'recent_stories': recent_stories,
        'upcoming_events': upcoming_events
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile', pk=request.user.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'alumni/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, user__pk=pk)
    return render(request, 'alumni/profile.html', {'profile': profile})

class DirectoryView(ListView):
    model = Profile
    template_name = 'alumni/directory.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('user')
        q = self.request.GET.get('q')
        year = self.request.GET.get('year')
        branch = self.request.GET.get('branch')

        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(company__icontains=q)
            )
        if year:
            qs = qs.filter(graduation_year=year)
        if branch:
            qs = qs.filter(branch=branch)
        return qs

class JobListView(ListView):
    model = Job
    template_name = 'alumni/jobs_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        # show only active jobs, newest first
        return Job.objects.filter(active=True).order_by('-posted_at')

class EventListView(ListView):
    model = Event
    template_name = 'alumni/events.html'
    paginate_by = 10
    context_object_name = 'events'   # make template variable consistent

    def get_queryset(self):
        # return all events ordered by start (adjust filter if you want only upcoming)
        return Event.objects.all().order_by('-start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'alumni/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class SuccessStoryListView(ListView):
    model = SuccessStory
    template_name = 'alumni/success_stories.html'
    paginate_by = 10

    def get_queryset(self):
        return SuccessStory.objects.all().order_by('-created_at')

class SuccessStoryDetailView(DetailView):
    model = SuccessStory
    template_name = 'alumni/story_detail.html'
    context_object_name = 'story'

@login_required
def create_story(request):
    if request.method == 'POST':
        form = SuccessStoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, 'Story published successfully!')
            return redirect('core:story_detail', pk=story.pk)
    else:
        form = SuccessStoryForm()
    return render(request, 'alumni/create_story.html', {'form': form})

@login_required
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, f'Thank you — you donated ₹{donation.amount}!')
            return redirect('core:index')
    else:
        form = DonationForm()
    return render(request, 'alumni/donate.html', {'form': form})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully.')
            return redirect('core:job_list')
    else:
        form = JobForm()
    return render(request, 'alumni/post_job.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('core:my_events')
    else:
        form = EventForm()
    return render(request, 'alumni/post_event.html', {'form': form})

@login_required
def my_events(request):
    qs = Event.objects.filter(created_by=request.user).order_by('-start')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'alumni/my_events.html', {'events': events})

class JobDetailView(DetailView):
    model = Job
    template_name = 'alumni/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # check if user already applied
            context['already_applied'] = JobApplication.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
        return context

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # prevent user from applying for their own job
    if job.posted_by == request.user:
        messages.error(request, 'You cannot apply for your own job posting.')
        return redirect('core:job_detail', pk=pk)
    
    # check if already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('core:job_detail', pk=pk)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f'✅ You have successfully applied for {job.title}!')
            return redirect('core:my_applications')
    else:
        form = JobApplicationForm()
    
    return render(request, 'alumni/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job', 'job__posted_by')
    paginator = Paginator(applications, 10)
    page = request.GET.get('page')
    apps = paginator.get_page(page)
    return render(request, 'alumni/my_applications.html', {'applications': apps})

@login_required
def job_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # only job poster can see applicants
    if job.posted_by != request.user:
        messages.error(request, 'You can only view applicants for your own jobs.')
        return redirect('core:job_detail', pk=pk)
    
    applications = JobApplication.objects.filter(job=job).select_related('applicant', 'applicant__profile')
    paginator = Paginator(applications, 10)
    page = request.GET.get('page')
    apps = paginator.get_page(page)
    
    return render(request, 'alumni/job_applicants.html', {
        'job': job,
        'applications': apps
    })

@login_required
def update_application_status(request, app_id):
    application = get_object_or_404(JobApplication, pk=app_id)
    
    # only job poster can update status
    if application.job.posted_by != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('core:job_detail', pk=application.job.pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {new_status}.')
    
    return redirect('core:job_applicants', pk=application.job.pk)

def logout_any(request):
    """
    Accept GET or POST and log the user out, then redirect home.
    Keeps CSRF protection for POST.
    """
    if request.method in ('POST', 'GET'):
        auth_logout(request)
    return redirect('core:index')
