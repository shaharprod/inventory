"""
כלי עזר עבור Multi-Tenancy
"""
from django.http import Http404
from functools import wraps


def get_tenant_from_request(request):
    """
    מחזיר את ה-Tenant מה-request
    """
    if hasattr(request, 'tenant') and request.tenant:
        return request.tenant

    # אם אין tenant, נסה למצוא לפי המשתמש
    if request.user.is_authenticated:
        tenant_user = request.user.tenant_memberships.first()
        if tenant_user:
            return tenant_user.tenant

    return None


def tenant_required(view_func):
    """
    Decorator שדורש tenant.
    אם אין tenant, מחזיר הודעה ידידותית.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        tenant = get_tenant_from_request(request)

        if not tenant:
            from django.shortcuts import render
            return render(request, 'inventory/no_tenant.html', status=404)

        # שמור את ה-tenant ב-request
        request.tenant = tenant

        return view_func(request, *args, **kwargs)

    return wrapper


def filter_by_tenant(queryset, tenant):
    """
    מסנן queryset לפי tenant אם קיים שדה tenant
    """
    if tenant and hasattr(queryset.model, 'tenant'):
        return queryset.filter(tenant=tenant)
    return queryset

