from rest_framework import status
from rest_framework.response import Response


class AllowPUTAsCreateMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = self.preprocess_data(request.data)
        # First checks for validity
        serializer = self.get_serializer(data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # And THEN creates the operation if everything is OK
        # Could be refactored to reduce duplicity BUT will stay like this for now
        self.instance = self.get_operation()
        serializer = self.get_serializer(self.instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_create_or_update(serializer)

        if getattr(self.instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            self.instance._prefetched_objects_cache = {}

        if self.instance is None:
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        return Response(serializer.data)

    def perform_create_or_update(self, serializer):
        serializer.instance.secao_atual = self.next_section_number
        serializer.save()

    def preprocess_data(self, data):
        return data
