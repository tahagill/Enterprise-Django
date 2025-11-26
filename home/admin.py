from django.contrib import admin
from django.utils.html import format_html
from home.models import Contact, Order, AuditLog, ServicePage, PartnerLogo


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for AuditLog model."""
    
    # List display configuration
    list_display = ('timestamp', 'user_link', 'action_badge', 'description_short', 'ip_address', 'content_info')
    
    # Filters
    list_filter = ('action', 'timestamp', 'content_type')
    
    # Search functionality
    search_fields = ('user__username', 'description', 'ip_address', 'user_agent')
    
    # Read-only fields (audit logs should not be editable)
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'user_agent', 'timestamp', 'content_type', 'object_id')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'timestamp'
    
    # Ordering
    ordering = ('-timestamp',)
    
    # Number of items per page
    list_per_page = 50
    
    # Disable add/delete permissions for audit logs
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def user_link(self, obj):
        """Display user as a clickable link."""
        if obj.user:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return format_html('<span style="color: gray;">Anonymous</span>')
    user_link.short_description = 'User'
    
    def action_badge(self, obj):
        """Display action with color-coded badge."""
        color_map = {
            'login': '#28a745',       # Green
            'logout': '#6c757d',      # Gray
            'signup': '#17a2b8',      # Cyan
            'profile_update': '#ffc107',  # Yellow
            'password_change': '#fd7e14', # Orange
            'order_created': '#007bff',   # Blue
            'order_updated': '#6610f2',   # Indigo
            'order_status_changed': '#e83e8c',  # Pink
            'contact_submitted': '#20c997',     # Teal
        }
        color = color_map.get(obj.action, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_badge.short_description = 'Action'
    
    def description_short(self, obj):
        """Display truncated description."""
        if len(obj.description) > 60:
            return obj.description[:60] + '...'
        return obj.description
    description_short.short_description = 'Description'
    
    def content_info(self, obj):
        """Display related content information."""
        if obj.content_type and obj.object_id:
            return format_html('<span style="color: #6c757d;">{} #{}</span>', obj.content_type, obj.object_id)
        return '-'
    content_info.short_description = 'Related Object'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Contact model."""
    
    # List display configuration
    list_display = ('name', 'email', 'phone', 'user_link', 'date', 'created_badge')
    
    # Filters
    list_filter = ('date', 'user')
    
    # Search functionality
    search_fields = ('name', 'email', 'phone', 'desc')
    
    # Read-only fields
    readonly_fields = ('date', 'user')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'date'
    
    # Ordering
    ordering = ('-date', 'name')
    
    # Number of items per page
    list_per_page = 20
    
    # Fieldsets for organized form layout
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('desc',)
        }),
        ('System Information', {
            'fields': ('user', 'date'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Display user as a clickable link."""
        if obj.user:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return '-'
    user_link.short_description = 'User'
    
    def created_badge(self, obj):
        """Display date with a badge."""
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            obj.date.strftime('%Y-%m-%d')
        )
    created_badge.short_description = 'Submitted On'
    
    # Custom actions
    actions = ['mark_as_resolved', 'soft_delete_contacts', 'restore_contacts']
    
    def mark_as_resolved(self, request, queryset):
        """Custom action to mark contacts as resolved (example)."""
        count = queryset.count()
        self.message_user(request, f'{count} contact(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected contacts as resolved'
    
    def soft_delete_contacts(self, request, queryset):
        """Soft delete selected contacts."""
        count = 0
        for contact in queryset:
            contact.delete()  # Uses soft delete
            count += 1
        self.message_user(request, f'{count} contact(s) soft deleted.')
    soft_delete_contacts.short_description = 'Soft delete selected contacts'
    
    def restore_contacts(self, request, queryset):
        """Restore soft-deleted contacts."""
        count = 0
        for contact in queryset:
            if contact.is_deleted:
                contact.restore()
                count += 1
        self.message_user(request, f'{count} contact(s) restored.')
    restore_contacts.short_description = 'Restore deleted contacts'
    
    def get_queryset(self, request):
        """Show all contacts including deleted in admin."""
        return self.model.all_objects.get_queryset()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Order model with status management."""
    
    # List display configuration
    list_display = (
        'title', 
        'client_name', 
        'user_link',
        'quantity', 
        'priority_badge',
        'status_badge',
        'created_at',
        'updated_at'
    )
    
    # Filters
    list_filter = ('status', 'priority', 'created_at', 'user')
    
    # Search functionality
    search_fields = ('title', 'client_name', 'description', 'user__username')
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'user')
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # Ordering (newest first)
    ordering = ('-created_at',)
    
    # Number of items per page
    list_per_page = 20
    
    # Fieldsets for organized form layout
    fieldsets = (
        ('Order Information', {
            'fields': ('title', 'description', 'client_name')
        }),
        ('Order Details', {
            'fields': ('quantity', 'priority', 'status', 'file')
        }),
        ('System Information', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Display user as a clickable link."""
        if obj.user:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.user.id,
                obj.user.username
            )
        return '-'
    user_link.short_description = 'User'
    
    def priority_badge(self, obj):
        """Display priority with color-coded badge."""
        if obj.priority == 'Urgent':
            color = '#dc3545'  # Red
        else:
            color = '#6c757d'  # Gray
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.priority
        )
    priority_badge.short_description = 'Priority'
    
    def status_badge(self, obj):
        """Display status with color-coded badge."""
        status_colors = {
            'Pending': '#ffc107',      # Yellow
            'Processing': '#17a2b8',   # Cyan
            'Shipped': '#007bff',      # Blue
            'Delivered': '#28a745',    # Green
            'Cancelled': '#dc3545',    # Red
        }
        color = status_colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = 'Status'
    
    # Custom actions for bulk status updates
    actions = [
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled',
        'mark_as_urgent',
        'soft_delete_orders',
        'restore_orders'
    ]
    
    def mark_as_processing(self, request, queryset):
        """Mark selected orders as Processing."""
        updated = queryset.update(status='Processing')
        self.message_user(request, f'{updated} order(s) marked as Processing.')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as Shipped."""
        updated = queryset.update(status='Shipped')
        self.message_user(request, f'{updated} order(s) marked as Shipped.')
    mark_as_shipped.short_description = 'Mark as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        """Mark selected orders as Delivered."""
        updated = queryset.update(status='Delivered')
        self.message_user(request, f'{updated} order(s) marked as Delivered.')
    mark_as_delivered.short_description = 'Mark as Delivered'
    
    def mark_as_cancelled(self, request, queryset):
        """Mark selected orders as Cancelled."""
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f'{updated} order(s) marked as Cancelled.')
    mark_as_cancelled.short_description = 'Mark as Cancelled'
    
    def mark_as_urgent(self, request, queryset):
        """Mark selected orders as Urgent priority."""
        updated = queryset.update(priority='Urgent')
        self.message_user(request, f'{updated} order(s) marked as Urgent.')
    mark_as_urgent.short_description = 'Mark as Urgent Priority'
    
    def soft_delete_orders(self, request, queryset):
        """Soft delete selected orders."""
        count = 0
        for order in queryset:
            order.delete()  # Uses soft delete
            count += 1
        self.message_user(request, f'{count} order(s) soft deleted.')
    soft_delete_orders.short_description = 'Soft delete selected orders'
    
    def restore_orders(self, request, queryset):
        """Restore soft-deleted orders."""
        count = 0
        for order in queryset:
            if order.is_deleted:
                order.restore()
                count += 1
        self.message_user(request, f'{count} order(s) restored.')
    restore_orders.short_description = 'Restore deleted orders'
    
    def get_queryset(self, request):
        """Show all orders including deleted in admin."""
        return self.model.all_objects.get_queryset()


# Customize admin site headers
admin.site.site_header = 'Enterprise Admin Panel'
admin.site.site_title = 'Enterprise Admin'
admin.site.index_title = 'Welcome to Enterprise Management'


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    """Admin interface for ServicePage model (singleton)."""
    
    list_display = ('title', 'heading', 'show_partner_logos', 'updated_at', 'updated_by')
    
    fieldsets = (
        ('Page Content', {
            'fields': ('title', 'heading', 'content')
        }),
        ('Partner Logos Section', {
            'fields': ('show_partner_logos', 'partner_section_title')
        }),
        ('Meta Information', {
            'fields': ('updated_by',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not ServicePage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the singleton instance
        return False
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    """Admin interface for PartnerLogo model."""
    
    list_display = ('name', 'logo_preview', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'url')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Partner Information', {
            'fields': ('name', 'logo', 'url')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def logo_preview(self, obj):
        """Display logo preview in admin list."""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border-radius: 5px;" />',
                obj.logo.url
            )
        return '-'
    logo_preview.short_description = 'Logo'

