from rest_framework import permissions
class IsAdminORReadonly(permissions.IsAdminUser):
    def has_permission(self,request,view):
         if request.method in permissions.SAFE_METHODS:
             print("vgc")
             return True
         else:
            admin_permission=bool(request.user and request.user.is_staff)
            print("vvjcjcjc")
            return  admin_permission


class IsReviewORReadonly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
           return True
        else:
            return obj.review_user==request.user or request.user.is_staff

