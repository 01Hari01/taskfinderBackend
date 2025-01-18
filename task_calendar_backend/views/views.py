from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError

from task_calendar_backend.models import Task
from task_calendar_backend.serializers.serializers import TaskSerializer


class TaskList(APIView):
    def get(self, request, selected_date):
        """
        Fetch tasks for a specific date.
        """
        try:
            # Parse the selected_date string into a date object
            parsed_date = parse_date(selected_date)
            if parsed_date is None:
                raise ValidationError("Invalid date format. Date must be in YYYY-MM-DD format.")

            # Filter tasks by the parsed date
            tasks = Task.objects.filter(date=parsed_date)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new task.
        """
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get_task(self, task_id):
        """
        Helper method to fetch a task by its ID.
        Returns the task if found, otherwise returns None.
        """
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    def get(self, request, task_id):
        """
        Fetch a specific task by its ID.
        """
        task = self.get_task(task_id)
        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        """
        Update a task by its ID.
        """
        task = self.get_task(task_id)
        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """
        Delete a task by its ID.
        """
        task = self.get_task(task_id)
        if task is None:
            return Response(
                {"error": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class PendingTasks(APIView):
    def get(self, request, current_date):
        """
        Fetch pending tasks (tasks with a date earlier than the current date and not completed).
        """
        try:
            # Parse the current_date string into a date object
            parsed_date = parse_date(current_date)
            if parsed_date is None:
                raise ValidationError("Invalid date format. Date must be in YYYY-MM-DD format.")

            # Filter pending tasks
            pending_tasks = Task.objects.filter(date__lt=parsed_date, completed=False)
            serializer = TaskSerializer(pending_tasks, many=True)
            return Response(serializer.data)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)