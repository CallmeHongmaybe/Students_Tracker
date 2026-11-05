class Student:
    def __init__(
        self,
        name,
        grade,
        age=None,
        math_score=None,
        literature_score=None,
        english_score=None,
        student_id=None,
    ):
        self.name = name
        self.grade = grade
        self.age = age
        m = math_score if math_score is not None else 0.0
        l = literature_score if literature_score is not None else 0.0
        e = english_score if english_score is not None else 0.0

        self.math_score = float(m)
        self.literature_score = float(l)
        self.english_score = float(e)
        self.student_id = student_id

    def calculate_average(self):
        avg = (self.math_score + self.literature_score + self.english_score) / 3.0
        return round(avg, 2)

    def get_rank(self):
        avg = self.calculate_average()
        if avg >= 8.0:
            return "Giỏi"
        elif avg >= 6.5:
            return "Khá"
        elif avg >= 5.0:
            return "Trung bình"
        else:
            return "Yếu"

    def __str__(self):
        age_str = f" | Tuổi: {self.age}" if self.age is not None else ""
        return (
            f"[{self.student_id or 'N/A'}] {self.name} | Lớp: {self.grade}{age_str} | "
            f"Toán: {self.math_score} - Văn: {self.literature_score} - Anh: {self.english_score} | "
            f"ĐTB: {self.calculate_average():.2f} ({self.get_rank()})"
        )
