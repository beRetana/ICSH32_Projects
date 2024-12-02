from problem3 import Student, Club
import random
import unittest


class StudentTest(unittest.TestCase):
    def test_has_id_given_when_created(self):
        student1 = Student(12345, "Maria")
        student2 = Student(34567, "Jose")

        self.assertEqual(student1.student_id(), 12345)
        self.assertEqual(student2.student_id(), 34567)

    def test_has_name_when_created(self):

        student1 = Student(12345, "Maria")
        student2 = Student(34567, "Jose")

        self.assertEqual(student1.student_name(), "Maria")
        self.assertEqual(student2.student_name(), "Jose")



class ClubTest(unittest.TestCase):
    def setUp(self):
        self._club = Club()
        self._student_ids = list(range(1000, 9999))
        random.shuffle(self._student_ids)

        
    def test_new_clubs_have_no_students(self):
        self.assertEqual(self._club.number_of_students(), 0)


    def test_after_adding_student__has_1_student(self):
        self._club.add_student(self._create_test_student())
        self.assertEqual(self._club.number_of_students(), 1)


    def test_continuing_to_add_students_means_more_students(self):
        for student_count in range(1, 101):
            self._club.add_student(self._create_test_student())
            self.assertEqual(self._club.number_of_students(), student_count)


    def _create_test_student(self):
        return Student(self._student_ids.pop(), "Jose")

    def test_should_find_student_by_id(self):
        student = Student(12345, "Maria")
        self._club.add_student(student)
        self.assertEqual(self._club.find_student(12345), student)

    def test_failing_to_add_an_existing_student(self):
        
        student = Student(12345, "Maria")
        self._club.add_student(student)
        student1 = Student(12345, "Jose")
        with self.assertRaises(KeyError):
            self._club.add_student(student1)



if __name__ == '__main__':
    unittest.main()
