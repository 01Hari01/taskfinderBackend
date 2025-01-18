from django.urls import path
from task_calendar_backend.views.views import TaskList, TaskDetail, PendingTasks

urlpatterns = [
    # Fetch tasks for a specific date or create a new task
    path('tasks/<str:selected_date>/', TaskList.as_view(), name='task-list-by-date'),  # GET tasks for a specific date
    path('tasks/', TaskList.as_view(), name='task-create'),  # POST to create a new task

    # Fetch, update, or delete a specific task by ID
    path('tasks/detail/<int:task_id>/', TaskDetail.as_view(), name='task-detail'),  # GET, PUT, DELETE for a specific task

    # Fetch pending tasks (tasks with a date earlier than the current date and not completed)
    path('tasks/pending/<str:current_date>/', PendingTasks.as_view(), name='pending-tasks'),  # GET pending tasks
]