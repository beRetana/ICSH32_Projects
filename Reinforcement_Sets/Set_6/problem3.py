class Student:
    def __init__(self, student_id: int, student_name: str):
        self._student_id = student_id
        self._student_name = student_name


    def student_id(self) -> int:
        return self._student_id

    def student_name(self) -> str:
        return self._student_name



class Club:
    def __init__(self):
        self._students = {}


    def number_of_students(self) -> int:
        return len(self._students)


    def add_student(self, student_to_add: Student) -> None:

        if self.find_student(student_to_add.student_id()) != "Student ID Not Found":
            raise KeyError("A STUDENT WITH THIS ID ALREADY EXISTS")
        
        self._students[student_to_add.student_id()] = student_to_add

    def find_student(self, student_id: int) -> Student | None:

        student = self._students.get(student_id, "Student ID Not Found")

        return student
