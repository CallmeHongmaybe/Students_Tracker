from ..models.student import Student


class StudentManager:
    def __init__(self):
        self._students = []
        self._next_id = 1

    def add_student(self, student):
        if student.student_id is None:
            student.student_id = self._next_id
            self._next_id += 1
        elif student.student_id >= self._next_id:
            self._next_id = student.student_id + 1

        self._students.append(student)
        return student

    def get_all(self):
        return list(self._students)

    def find_by_name(self, name_query):
        query = name_query.strip().lower()
        matched = []
        has_found = False

        for student in self._students:
            if query in student.name.lower():
                matched.append(student)
                has_found = True

        return matched

    def get_by_id(self, student_id):
        for student in self._students:
            if student.student_id == student_id:
                return student
        return None

    def update_student(self, student_id, updated_student):
        for i, existing in enumerate(self._students):
            if existing.student_id == student_id:
                updated_student.student_id = student_id
                self._students[i] = updated_student
                return True
        return False

    def delete_student(self, student_id):
        initial_len = len(self._students)
        self._students = [s for s in self._students if s.student_id != student_id]
        return len(self._students) < initial_len

    def count(self):
        return len(self._students)

    def load_sample_data(self):
        samples = [
            Student("Nguyễn Lê An", "10A1", 15, 8.5, 8.0, 9.0),
            Student("Trần Thị Bình", "10A2", 15, 7.0, 7.5, 6.5),
            Student("Lê Hoàng Cường", "10A1", 15, 5.5, 6.0, 5.0),
            Student("Phạm Minh Dũng", "10B3", 15, 4.0, 4.5, 3.5),
            Student("Đinh Thủy Lê", "10A1", 15, 9.5, 9.0, 8.5),
            Student("Đinh Văn Bình", "10A1", 15, 8.5, 8.0, 9.0),
            Student("Lê Anh Dzũng", "10A4", 15, 6.5, 7.0, 7.5),
        ]
        for s in samples:
            self.add_student(s)
