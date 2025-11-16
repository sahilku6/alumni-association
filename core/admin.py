from django.contrib import admin
from .models import Profile, Job, Event, SuccessStory, Donation, JobApplication

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'graduation_year', 'branch')
    search_fields = ('user__first_name', 'user__last_name', 'company')
    list_filter = ('graduation_year', 'branch')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_at', 'active')
    search_fields = ('title', 'company')
    list_filter = ('active', 'posted_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'location', 'created_by')
    search_fields = ('title', 'location')
    list_filter = ('start',)

@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'featured', 'created_at')
    search_fields = ('title', 'author__first_name')
    list_filter = ('featured', 'created_at')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'created_at')
    search_fields = ('donor__first_name', 'donor__last_name')
    list_filter = ('created_at', 'amount')
    readonly_fields = ('created_at',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'job__title')
    readonly_fields = ('applied_at', 'updated_at')
