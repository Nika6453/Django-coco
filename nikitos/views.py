from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Group, Club
from .forms import RegisterForm

# Регистрация
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "students/register.html", {"form": form})


# -----------------------------
#      CRUD для студентов
# -----------------------------

def hello(request):
    return render(request, "students/hello.html")

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "students/index.html", {"students": students})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/details.html", {"student": student})


@login_required
def add_student(request):
    groups = Group.objects.all()
    clubs = Club.objects.all()

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        group_id = request.POST.get("group")
        club_ids = request.POST.getlist("clubs")
        photo = request.FILES.get("photo")

        # получаем объект группы
        group = get_object_or_404(Group, id=group_id)

        # создаём студента
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            group=group,
            photo=photo
        )

        # добавляем клубы (многие-ко-многим)
        student.clubs.set(club_ids)

        return redirect("student_list")

    return render(request, "students/add.html", {"groups": groups, "clubs": clubs})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    groups = Group.objects.all()
    clubs = Club.objects.all()

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.age = request.POST.get("age")

        group_id = request.POST.get("group")
        club_ids = request.POST.getlist("clubs")
        student.group = get_object_or_404(Group, id=group_id)

        if "photo" in request.FILES:
            student.photo = request.FILES["photo"]

        student.save()
        student.clubs.set(club_ids)

        return redirect("student_list")

    return render(
        request,
        "students/edit.html",
        {"student": student, "groups": groups, "clubs": clubs},
    )


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("student_list")