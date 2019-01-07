import json
from rest_framework.renderers import JSONRenderer


class QuestionJsonRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):
        if 'errors' in data or 'detail' in data:
            return super().render(data)

        return json.dumps({
            'data': data
        })
