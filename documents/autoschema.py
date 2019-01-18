from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema


class DocumentSwaggerAutoSchema(SwaggerAutoSchema):
    def get_request_body_parameters(self, consumes):
        """
        Overwrite original method
        """
        serializer = self.get_request_serializer()
        if serializer is None:
            return []

        return self.serializer_to_parameters(serializer, in_=openapi.IN_FORM)
