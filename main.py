import sys
from src.models.student import Student
from src.services.student_manager import StudentManager

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def print_menu():
    print("\n" + "=" * 45)
    print("STUDENT TRACKER - MENU THAO TÁC")
    print("=" * 45)
    print("1. Thêm học sinh")
    print("2. Hiển thị danh sách học sinh")
    print("3. Tìm kiếm theo tên/ID")
    print("4. Sửa thông tin học sinh")
    print("5. Xóa học sinh")
    print("6. Thoát")
    print("=" * 45)


def input_score(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            val = float(raw)
            if 0.0 <= val <= 10.0:
                return val
            print("Điểm phải nằm trong khoảng từ 0.0 đến 10.0. Vui lòng nhập lại!")
        except ValueError:
            print("Vui lòng nhập số thực hợp lệ (ví dụ: 7.5, 8.0)!")


def handle_add_student(manager):
    print("\n--- THÊM HỌC SINH MỚI ---")
    name = input("Nhập họ và tên: ").strip()
    while not name:
        print(" Tên không được để trống!")
        name = input("Nhập họ và tên: ").strip()

    grade = input("Nhập lớp (ví dụ: 10A1): ").strip()
    while not grade:
        print(" Lớp không được để trống!")
        grade = input("Nhập lớp (ví dụ: 10A1): ").strip()

    age = input("Nhập tuổi: ").strip()
    if not age:
        age = None
    else:
        try:
            age = int(age)
        except ValueError:
            pass

    math = input_score("Điểm Toán: ")
    lit = input_score("Điểm Văn: ")
    eng = input_score("Điểm Tiếng Anh: ")

    student = Student(name, grade, age, math, lit, eng)
    added = manager.add_student(student)
    print(f"\n Đã thêm thành công học sinh: {added.name}")
    print(f"     Điểm trung bình: {added.calculate_average():.2f} | Xếp loại: {added.get_rank()}")


def handle_show_all(manager):
    print("\n--- DANH SÁCH HỌC SINH TỔNG HỢP ---")
    students = manager.get_all()
    if not students:
        print("Danh sách hiện đang trống")
        return

    print(f"{'ID':<5} {'Họ và tên':<22} {'Lớp':<10} {'Tuổi':<6} {'Toán':<6} {'Văn':<6} {'Anh':<6} {'ĐTB':<7} {'Xếp loại':<10}")
    print("-" * 75)
    for s in students:
        avg = s.calculate_average()
        rank = s.get_rank()
        age_str = str(s.age) if s.age is not None else "-"
        print(f"{s.student_id:<5} {s.name:<22} {s.grade:<10} {age_str:<6} {s.math_score:<6.1f} {s.literature_score:<6.1f} {s.english_score:<6.1f} {avg:<7.2f} {rank:<10}")
    print(f"\nTổng cộng: {len(students)} học sinh.")


def select_student_id(manager, action="xử lý") -> int | None:
    print(f"Nhập tên hoặc ID của học sinh cần {action}. Nếu hệ thống phát hiện trùng tên, vui lòng nhập ID.")
    choice = input("Nhập 0 để nhập ID, 1 để nhập tên: ").strip()
    if choice not in ("0", "1"):
        print("Bạn chỉ được nhập 0 hoặc 1.")
        return None

    if choice == "0":
        try:
            student_id = int(input(f"Nhập ID học sinh cần {action}: ").strip())
            return student_id
        except ValueError:
            print("ID phải là số nguyên!")
            return None

    else:  # choice == "1"
        name = input(f"Nhập tên học sinh cần {action}: ").strip()
        if not name:
            print("Từ khóa tìm kiếm không được để trống!")
            return None

        results = manager.find_by_name(name)
        if len(results) == 0:
            print(f" Không tìm thấy học sinh nào có tên chứa '{name}'!")
            return None
        elif len(results) == 1:
            return results[0].student_id
        else:
            print(f"Tìm thấy {len(results)} học sinh hàm chứa tên '{name}':")
            for s in results:
                print(f" ** {s}")
            print(f"Vui lòng chọn ID học sinh cần {action}.")
            try:
                selected_id = int(input(f"Nhập ID học sinh cần {action}: ").strip())
                if any(s.student_id == selected_id for s in results):
                    return selected_id
                else:
                    print(f"ID {selected_id} không nằm trong danh sách kết quả tìm kiếm!")
                    return None
            except ValueError:
                print("ID phải là số nguyên!")
                return None


def handle_search_by_id(manager, action="sửa"):
    return select_student_id(manager, action=action)


def handle_search_by_name(manager):
    print("\n--- TÌM KIẾM HỌC SINH THEO TÊN ---")
    query = input("Nhập tên học sinh cần tìm: ").strip()
    if not query:
        print("Từ khóa tìm kiếm không được để trống!")
        return

    results = manager.find_by_name(query)
    if results:
        print(f"\n Tìm thấy {len(results)} kết quả:")
        for s in results:
            print(f" ** {s}")
    else:
        print(f" Không tìm thấy học sinh nào có tên chứa '{query}'!")


def handle_search_student(manager):
    print("\n--- TÌM KIẾM HỌC SINH ---")
    choice = input("Nhập 0 để tìm theo ID, 1 để tìm theo tên: ").strip()
    if choice == "0":
        try:
            student_id = int(input("Nhập ID học sinh cần tìm: ").strip())
            student = manager.get_by_id(student_id)
            if student:
                print(f"\n Kết quả tìm kiếm ID {student_id}:")
                print(f" ** {student}")
            else:
                print(f" Không tìm thấy học sinh có ID = {student_id}!")
        except ValueError:
            print("ID phải là số nguyên!")
    elif choice == "1":
        handle_search_by_name(manager)
    else:
        print("Bạn chỉ được nhập 0 hoặc 1.")


def handle_update_student(manager):
    print("\n--- SỬA THÔNG TIN HỌC SINH ---")
    
    student_id = select_student_id(manager, action="sửa")
    if student_id is None:
        return

    student = manager.get_by_id(student_id)
    if not student:
        print(f"Không tìm thấy học sinh có ID = {student_id}!")
        return

    print(f"Bạn đang sửa học sinh: {student.name} (Lớp: {student.grade}, Tuổi: {student.age})")
    new_name = input(f"Họ tên mới (nhấn Enter để giữ '{student.name}'): ").strip()
    if not new_name:
        new_name = student.name

    new_grade = input(f"Lớp mới (nhấn Enter để giữ '{student.grade}'): ").strip()
    if not new_grade:
        new_grade = student.grade

    new_age_raw = input(f"Tuổi mới (nhấn Enter để giữ '{student.age}'): ").strip()
    if not new_age_raw:
        new_age = student.age
    else:
        try:
            new_age = int(new_age_raw)
        except ValueError:
            new_age = new_age_raw

    print("Cập nhật lại điểm thi:")
    new_math = input_score(f"Điểm Toán mới (hiện tại: {student.math_score}): ", allow_blank=True)
    if new_math is None:
        new_math = student.math_score
    new_lit = input_score(f"Điểm Văn mới (hiện tại: {student.literature_score}): ", allow_blank=True)
    if new_lit is None:
        new_lit = student.literature_score
    new_eng = input_score(f"Điểm Anh mới (hiện tại: {student.english_score}): ", allow_blank=True)
    if new_eng is None:
        new_eng = student.english_score

    updated = Student(new_name, new_grade, new_age, new_math, new_lit, new_eng, student_id)
    manager.update_student(student_id, updated)
    print(f"\n Cập nhật thành công học sinh ID {student_id}!")


def handle_delete_student(manager):
    print("\n--- XÓA HỌC SINH ---")
    
    student_id = select_student_id(manager, action="xóa")
    if student_id is None:
        return
    
    student = manager.get_by_id(student_id)
    if not student:
        print(f"Không tìm thấy học sinh có ID = {student_id}!")
        return

    confirm = input(f"Bạn có chắc muốn xóa '{student.name}' (ID: {student_id})? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        manager.delete_student(student_id)
        print(f"Đã xóa thành công học sinh '{student.name}'.")
    else:
        print("Đã hủy thao tác xóa.")


def run_cli(manager=None):
    if manager is None:
        manager = StudentManager()
        manager.load_sample_data()

    while True:
        print_menu()
        choice = input("Vui lòng chọn chức năng (1-6): ").strip()

        if choice == "1":
            handle_add_student(manager)
        elif choice == "2":
            handle_show_all(manager)
        elif choice == "3":
            handle_search_student(manager)
        elif choice == "4":
            handle_update_student(manager)
        elif choice == "5":
            handle_delete_student(manager)
        elif choice == "6":
            print("\nCảm ơn bạn đã sử dụng Student Tracker! Tạm biệt!\n")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 6.")

if __name__ == "__main__":
    run_cli()
