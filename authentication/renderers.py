import json
from rest_framework.renderers import JSONRenderer


class UserJsonRender(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        if errors:
            return super().render(data)

        return json.dumps({
            'user': data
        })
