from django.contrib import admin

# Register your models here.
from .models import Review  # Import your Review model

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'created_at')  # Customize columns
    search_fields = ('name', 'text')  # Add search functionality
    list_filter = ('created_at', )  # Add filters