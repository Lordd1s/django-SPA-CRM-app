from rest_framework.permissions import BasePermission


class IsInGroupPermission(BasePermission):
    def has_permission(self, request, view):
        # Проверяем, принадлежит ли пользователь к группе "МояГруппа"
        return (
            request.user.groups.filter(name="Директор").exists()
            or request.user.groups.filter(name="Кадровый отдел / Бухгалтерия").exists()
        )
