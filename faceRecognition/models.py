from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    student_class = models.IntegerField()
    section = models.CharField(max_length=1)
    email = models.EmailField(max_length=150, unique=True)
    dob = models.DateField()
    address = models.TextField()
    year = models.IntegerField()
    student_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Other')])
    mobile = models.CharField(max_length=15, unique=True)


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Leave')])

# class Teacher(models.Model):
#     teacher_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=150, unique=True)
#     mobile = models.CharField(max_length=15, null=True, blank=True)
#     address = models.TextField()
#     teacher_status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], null=True, blank=True)
#     gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Other')])


# class TeacherAttendance(models.Model):
#     attendance_id = models.AutoField(primary_key=True)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late')], null=True, blank=True)

# class LeaveRequest(models.Model):
#     leave_id = models.AutoField(primary_key=True)
#     sender = models.EmailField()
#     receiver = models.EmailField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     reason = models.TextField()
#     status = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')])


# class Subject(models.Model):
#     subject_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     student_class = models.IntegerField()
#     subject_type = models.CharField(max_length=1, choices=[('T', 'Theory'), ('P', 'Practical'), ('G', 'General')], null=True, blank=True)


# class SubjectTeacher(models.Model):
#     subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     email = models.ForeignKey(Teacher, to_field='email', on_delete=models.CASCADE)


# class Timetable(models.Model):
#     timetable_id = models.CharField(max_length=20, primary_key=True)
#     student_class = models.CharField(max_length=255)
#     section = models.CharField(max_length=255)
#     day = models.CharField(max_length=10, choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')])
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     period_id = models.IntegerField(null=True, blank=True)


# class Login(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     username = models.EmailField(max_length=100, unique=True)
#     password = models.CharField(max_length=255)
#     user_type = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')])
#     created_at = models.DateTimeField(auto_now_add=True)