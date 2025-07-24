import cohere
import os
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from surveys.models import SurveyForm, SurveyResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def analyze_survey(request, form_id):
    form = get_object_or_404(SurveyForm, id=form_id)
    responses = SurveyResponse.objects.filter(form=form)

    if not responses.exists():
        return Response({"error": "No responses found for this form."}, status=404)

    questions = form.schema
    response_data = [resp.response for resp in responses]  # ✅ Use your actual field

    prompt = f"""
You are a smart data analyst embedded in a survey platform.

Your job is to:
1. Read survey form responses
2. Analyze key patterns
3. Output a JSON response that includes:
   - Summary insights
   - Chart suggestions with type, title, x/y fields, and example data points

Form Title: {form.title}

Questions: {questions}

Responses: {response_data}

Instructions:
- Only include meaningful charts (e.g., bar chart for ratings, pie chart for yes/no)
- Provide up to 3 chart suggestions
- Output clean, valid JSON in this format:

{{
  "summary": "...",
  "charts": [
    {{
      "type": "bar",
      "title": "...",
      "xField": "...",
      "yField": "...",
      "data": [
        {{ "xField": "Value1", "yField": 10 }},
        ...
      ]
    }}
  ]
}}
"""

    try:
        response = co.generate(
            model="command",  # most capable model in free tier
            prompt=prompt,
            max_tokens=500,
            temperature=0.5,
        )

        content = response.generations[0].text.strip()

        parsed_json = json.loads(content)
        return Response(parsed_json)

    except json.JSONDecodeError:
        return Response({"error": "Cohere returned invalid JSON", "raw": content}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
