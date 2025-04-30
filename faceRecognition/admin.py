from django.contrib import admin
from .models import Student, Attendance

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'student_class',
                    'section', 'email', 'dob', 'address', 'year',
                    'student_status', 'gender', 'mobile',
                    ]


class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'attendance_id',
        'student',
        'date',
        'time',
        'status',
    ]

admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)