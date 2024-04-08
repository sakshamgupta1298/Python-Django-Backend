from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework import status
# from .tasks import save_to_database 
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from minio import Minio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import save_to_database 
from django.shortcuts import render
from minio.error import InvalidResponseError
import tempfile 
import os

class TemperatureStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city_id):
        # Define the page size
        page_size = 10000  

        # Fetch all temperatures for the specified city with pagination
        with connection.cursor() as cursor:
            # Fetch total count of temperatures for the specified city
            cursor.execute("""
                SELECT COUNT(*) FROM temperature 
                WHERE city_id = %s
            """, [city_id])
            total_count = cursor.fetchone()[0]

            # Calculate total pages
            total_pages = total_count // page_size + (1 if total_count % page_size > 0 else 0)

            # Initialize variables to store aggregate values
            min_temp = None
            max_temp = None
            sum_temp = 0

            # Fetch temperatures for each page
            for page_number in range(1, total_pages + 1):
                cursor.execute("""
                    SELECT MAX(temperature), MIN(temperature), SUM(temperature) FROM temperature 
                    WHERE city_id = %s
                    LIMIT %s OFFSET %s
                """, [city_id, page_size, page_size * (page_number - 1)])
                row = cursor.fetchone()

                # Update min and max temperatures
                if row:
                    max_temp_page, min_temp_page, sum_temp_page = row
                    if min_temp is None or min_temp_page < min_temp:
                        min_temp = min_temp_page
                    if max_temp is None or max_temp_page > max_temp:
                        max_temp = max_temp_page
                    sum_temp += sum_temp_page

            # Calculate average temperature
            average_temp = sum_temp / total_count if total_count > 0 else 0

            # Prepare response data
            response_data = {
                'min_temp': min_temp,
                'max_temp': max_temp,
                'mean_temp': average_temp,
                'total_pages': total_pages
            }

            return Response(response_data)




class UploadTemperatureFile(APIView):
    def get(self, request, format=None):
        # Render the upload file form
        return render(request, 'upload_file.html')

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response("No file provided by the user", status=status.HTTP_400_BAD_REQUEST)
        
        # Initialize MinIO client
        minio_client = Minio(
                endpoint='play.min.io',
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=True
            )

        # Construct the object name (key) for the file in MinIO
        object_name = file.name
        
        # Save the file to a temporary location on the server
        temp_file_path = os.path.join(tempfile.gettempdir(), object_name)
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Upload the file to MinIO
        file_content_type = file.content_type
        try:
            minio_client.fput_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                file_path=temp_file_path,
                content_type=file_content_type
            )
            
            # Generate the URL for the uploaded file
            presigned_url = minio_client.presigned_get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
            )
            save_to_database.delay(presigned_url)
            return Response({"file_url": presigned_url}, status=status.HTTP_201_CREATED)
        except InvalidResponseError as e:
            return Response(f"Failed to upload file to MinIO: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)