from rest_framework.permissions import BasePermission


class IsInGroupPermission(BasePermission):
    def has_permission(self, request, view):
        res = (
            request.user.groups.filter(name="Директор").exists()
            or request.user.groups.filter(name="Кадровый отдел / Бухгалтерия").exists()
        )
        # print("IsInGroup", res)
        return res


class IsMaster(BasePermission):
    def has_permission(self, request, view):
        result = (
            request.user.groups.filter(name="Начальники объекта").exists()
            or request.user.groups.filter(name="Мастеры").exists()
        )
        # print("IsMaster", result)
        return result
