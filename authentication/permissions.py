from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    massage = "only staffs can access"

    def has_permission(self, request, view):
        user = request.user
        return user.is_staff
class Is3(permissions.BasePermission):
    massage = "only speople with a phone number ending with 3 is allowed!"

    def has_permission(self, request, view):
        user = request.user
        return user.phone.endswith("3")
