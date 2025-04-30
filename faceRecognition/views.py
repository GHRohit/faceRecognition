from django.shortcuts import render, redirect
from django.contrib import messages
from sklearn.neighbors import KNeighborsClassifier
from datetime import date, datetime
from .models import Student, Attendance
from pathlib import Path
from django import forms
import pandas as pd
import numpy as np
import joblib
import cv2


# Define base directory and paths for static files and media
BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILE_PATH = BASE_DIR / "static"
FACES_DIR = BASE_DIR / "media" / "faces"
ATTENDANCE_DIR = STATICFILE_PATH / "Attendance"
MODEL_PATH = STATICFILE_PATH / "face_recognition_model.pkl"
CASCADECLASSIFIER_PATH = BASE_DIR / "static" / "haarcascade_frontalface_default.xml"
ATTENDANCE_FILE = Path(
    STATICFILE_PATH
    / "Attendance"
    / f'Attendance-{date.today().strftime("%d-%B-%Y")}.csv'
)


# Function to get today's date in a specific format
def datetoday():
    return date.today().strftime("%d-%B-%Y")


# Initialize the face detector and video capture object for webcam access
face_detector = cv2.CascadeClassifier(str(CASCADECLASSIFIER_PATH))

# Create necessary directories if they do not exist
for directory in [ATTENDANCE_DIR, FACES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# Define a ModelForm for the Student model
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name", "email", "gender", "dob", "student_class",
            "section", "address", "year", "student_status", "mobile",
        ]


# Create an attendance file if it does not already exist
if not ATTENDANCE_FILE.exists():
    ATTENDANCE_FILE.write_text("Name,Roll,Time")


# Function to get the total number of registered users
def total_registered_users():
    return len(list(FACES_DIR.iterdir()))


# Function to extract faces from an image
def extract_faces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    return face_detector.detectMultiScale(gray_image, 1.3, 5)  # Detect faces


# Function to identify a face using a machine learning model
def identify_face(face_array):
    model = joblib.load(MODEL_PATH)  # Load the trained model
    return model.predict(face_array)  # Predict the identity of the face


# Function to train the model on all available faces in the faces folder
def train_model():
    face_data, labels = [], []  # Lists to hold face data and corresponding labels
    user_directories = list(FACES_DIR.iterdir())  # List of user directories
    print("\n user list : ", user_directories, "\n")  # Debugging output for user list

    for user_directory in user_directories:
        if user_directory.is_dir():  # Ensure that the user is a directory
            for image_name in user_directory.iterdir():  # Iterate through images in the user's directory
                image = cv2.imread(str(image_name))  # Read the image
                if image is not None:  # Check if the image was loaded successfully
                    resized_face = cv2.resize(image, (50, 50))  # Resize the face image
                    face_data.append(resized_face.ravel())  # Flatten and append the face data
                    labels.append(user_directory.name)  # Append the user's name as the label

    if np.any(face_data):
        knn_classifier = KNeighborsClassifier(n_neighbors=5)  # Initialize the KNN classifier
        knn_classifier.fit(np.array(face_data), labels)  # Train the classifier with the face data and labels
        joblib.dump(knn_classifier, MODEL_PATH)  # Save the trained model


# Function to extract today's attendance records
def extract_attendance():
    today = date.today()  # Get today's date
    attendance_records = Attendance.objects.filter(date=today).select_related("student")  # Optimize query

    # Create a list of dictionaries for each attendance record
    attendance_data = [
        {
            "student_id": record.student.student_id,
            "student_name": record.student.name,
            "attendance_time": record.time,
        }
        for record in attendance_records
    ]

    return attendance_data, len(attendance_records)  # Return extracted data


# Function to add attendance for a specific user
def add_attendance(name):
    username, user_id = name.split("_")  # Extract username and user ID
    current_time = datetime.now().strftime("%H:%M")  # Get the current time in 24-hour format
    today = date.today()  # Get today's date

    # Retrieve all students for today's date
    student_ids = list(Attendance.objects.filter(date=today).values_list("student_id", flat=True))
    print(f"\n student_ids = {student_ids}")

    if int(user_id) not in student_ids:  # Check if the user ID is not in the student list
        # Append attendance record to the CSV file
        with open(ATTENDANCE_FILE, "a") as f:
            f.write(f"\n{username},{user_id},{current_time}")  # Append to CSV

        # Store attendance in the Attendance table
        attendance_record = Attendance(
            student_id=user_id,
            time=current_time,
            date=today,
            status='P'
        )
        print("\n attendanceRecord ", attendance_record)
        attendance_record.save()  # Save the attendance record to the database


# Function to add a new user
def add(username, user_id):
    user_image_folder = FACES_DIR / f"{username}_{user_id}"  # Create a folder for user images
    user_image_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

    cap = cv2.VideoCapture(0)  # Initialize video capture
    images_to_capture = 50  # Total images to capture
    captured_images = 0  # Counter for captured images

    def draw_face_rectangle_and_text(frame, x, y, w, h, captured_count):
        """Draw rectangle around detected face and display captured count."""
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)  # Draw rectangle
        cv2.putText(frame, f"Images Captured: {captured_count}/{images_to_capture}", 
                    (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)  # Display count

    while captured_images < images_to_capture:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:  # Check if the frame was read successfully
            break  # Exit the loop if there was an error reading the frame

        faces = extract_faces(frame)  # Extract faces from the frame
        for x, y, w, h in faces:
            draw_face_rectangle_and_text(frame, x, y, w, h, captured_images)  # Draw rectangle and text
            if captured_images % 10 == 0:  # Capture every 10th frame
                image_name = f"{username}_{captured_images}.jpg"  # Create a filename for the image
                cv2.imwrite(user_image_folder / image_name, frame[y:y + h, x:x + w])  # Save the captured face image
                captured_images += 1  # Increment the image counter

        cv2.imshow("Adding new User", frame)  # Display the frame with the detected face
        if cv2.waitKey(1) == 27:  # Exit if the 'Esc' key is pressed
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print("Training Model")  # Debugging output before training the model
    train_model()  # Train the model with the captured images


# Function to handle student addition
def add_student(request):
    if request.method == "POST":  # Check if the request method is POST
        form_data = StudentForm(request.POST)  # Create a form instance with the submitted data

        if form_data.is_valid():  # Validate the form data
            existing_student = Student.objects.filter(email=request.POST.get("email")).exists()  # Check for existing student
            if not existing_student:  # If the student does not exist
                student = form_data.save()  # Save the form and get the instance
                student_id = student.student_id  # Get the student ID from the saved instance
                add(request.POST.get("name"), student_id)  # Add the student
                messages.success(request, "Student added successfully!")  # Success message
                return redirect("home")  # Redirect to the home page
            else:
                messages.error(request, f"Student '{request.POST.get('email')}' data already exists!")  # Error message
        else:
            print(form_data.errors)  # Print form validation errors
            messages.error(request, "There was an error with the form. Please check the details.")  # Error message

    return redirect("home")  # Redirect to home if the request method is not POST


# Function to start attendance tracking
def start(request):
    if not Path(MODEL_PATH).exists():  # Check if the model exists
        messages.error(request, "There is no trained model in the static folder. Please add a new face to continue.")
        return render_attendance_data(request)  # Render attendance data if model doesn't exist

    cap = cv2.VideoCapture(0)  # Initialize video capture
    if not cap.isOpened():  # Check if the webcam opened successfully
        messages.error(request, "Could not open webcam.")  # Error message
        return redirect("home")  # Redirect to home if webcam fails

    process_frames(cap)  # Process frames for attendance tracking

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows
    return render_attendance_data(request)  # Render attendance data after processing


def process_frames(cap):
    """Process frames from the webcam for face detection and attendance tracking."""
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:  # Check if the frame was read successfully
            break  # Exit the loop if there was an error reading the frame

        faces = extract_faces(frame)  # Extract faces from the frame
        if len(faces) > 0:  # Check if any faces are detected
            for x, y, w, h in faces:  # Loop through all detected faces
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)  # Draw rectangle around detected face
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))  # Resize the detected face
                identified_person = identify_face(face.reshape(1, -1))[0]  # Identify the face
                add_attendance(identified_person)  # Add attendance for the identified person
                cv2.putText(frame, f"{identified_person}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)  # Display the identified person's name

        cv2.imshow("Attendance", frame)  # Show the frame with the detected face
        if cv2.waitKey(1) == 27:  # Exit if the 'Esc' key is pressed
            break


def render_attendance_data(request):
    """Render the index page with attendance data."""
    attendance_data, total_present = extract_attendance()
    print("Attendance Data: ", attendance_data, "Total Present: ", total_present)
    return render(
        request,
        "index.html",
        context={
            "attendance_data": attendance_data,
            "totalPresent": total_present,
            "datetoday": datetoday(),  # Pass today's date
        },
    )


# Function to render the home page
def home(request):
    return render_attendance_data(request)  # Render attendance data for the home page
