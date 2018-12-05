from django.utils import dateparse
from django.conf import settings
from rest_framework import viewsets


class CWTAPViewSet(viewsets.ModelViewSet):

    query_fields = []  # 查询字段

    def filter_queryset(self, queryset):
        """ 通用查询 """
        if isinstance(self.query_fields, list) and len(self.query_fields) > 0:
            for query_field in self.query_fields:
                field_value = self.request.query_params.get(query_field, None)
                if field_value is not None:
                    if query_field in settings.QUERY_DATETIME_FIELDS:
                        start, end = field_value.lower().split(
                            settings.QUERY_DATETIME_DELIMITER.lower())
                        start = dateparse.parse_datetime(start.strip())
                        end = dateparse.parse_datetime(end.strip())
                        if start:
                            queryset = queryset.filter(
                                **{"{0}__gte".format(query_field): start})

                        if end:
                            queryset = queryset.filter(
                                **{"{0}__lte".format(query_field): end})
                    else:
                        queryset = queryset.filter(
                            **{"{0}".format(query_field): field_value})

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            tenant=self.request.user.userprofile.tenant)

    def perform_update(self, serializer):
        serializer.save(
            owner=self.request.user,
            tenant=self.request.user.userprofile.tenant)
