from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework import status
from .tasks import save_to_database 
from django.shortcuts import render

class TemperatureStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city_id):
        # Get page number from query parameters, default to 1 if not provided
        page_number = request.query_params.get('page', 1)

        # Execute the SQL query with pagination
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT temperature FROM temperature WHERE city_id = %s
            """, [city_id])
            rows = cursor.fetchall()

        # Convert the result to a list of temperatures
        temperatures = [row[0] for row in rows]

        # Paginate the temperatures
        paginator = Paginator(temperatures, 10)  # Assuming 10 items per page
        page_obj = paginator.get_page(page_number)

        if page_obj.object_list:
            mean_temp = sum(page_obj.object_list) / len(page_obj.object_list)
            max_temp = max(page_obj.object_list)
            min_temp = min(page_obj.object_list)
            response_data = {
                'mean': mean_temp,
                'max': max_temp,
                'min': min_temp,
                'page_info': {
                    'page_number': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_pages': paginator.num_pages
                }
            }
            return Response(response_data)
        else:
            return Response({'message': 'No temperature readings found for the specified city.'}, status=404)


class UploadTemperatureFile(APIView):
    def get(self, request, format=None):
        # Render the upload file form
        return render(request, 'upload_file.html')

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)
        
        # Read file content and pass data to Celery task
        file_data = file.read().decode('utf-8')
        print(file_data)
        print("going to celery")
        save_to_database.delay(file_data)  # Passing file data to Celery task
        
        return Response("File upload request accepted", status=status.HTTP_202_ACCEPTED)
