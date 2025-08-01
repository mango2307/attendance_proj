
class User:
    def __init__(self, name: str):
        self.name = name
        self.attendance_user = [0] * 7
        self.points = 0
        self.grade = None
        self.weekday_count = 0
        self.weekend_count = 0

    def add_attendance(self, day_index: int, point: int):
        self.attendance_user[day_index] += 1
        self.points += point

        if day_index == 2:
            self.weekday_count += 1
        if day_index >= 5:
            self.weekend_count += 1

    def apply_bonus(self):
        if self.attendance_user[3] > 9:
            self.points += 10
        if self.attendance_user[5] + self.attendance_user[6] > 9:
            self.points += 10

    def evaluate_grade(self):
        if self.points >= 50:
            self.grade = "GOLD"
        elif self.points >= 30:
            self.grade = "SILVER"
        else:
            self.grade = "NORMAL"

    def is_inactive(self):
        return self.grade == "NORMAL" and self.weekday_count == 0 and self.weekend_count == 0


class AttendanceRule:
    DAY_INDEX = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    DAY_POINTS = {
        "monday": 1,
        "tuesday": 1,
        "wednesday": 3,
        "thursday": 1,
        "friday": 1,
        "saturday": 2,
        "sunday": 2
    }

    @classmethod
    def get_day_index(cls, weekday: str) -> int:
        return cls.DAY_INDEX[weekday]

    @classmethod
    def get_point(cls, weekday: str) -> int:
        return cls.DAY_POINTS[weekday]


class AttendanceSystem:
    def __init__(self):
        self.users = {}

    def get_or_create_user(self, name: str) -> User:
        if name not in self.users:
            self.users[name] = User(name)
        return self.users[name]

    def record_attendance(self, name: str, weekday: str):
        user = self.get_or_create_user(name)
        day_index = AttendanceRule.get_day_index(weekday)
        point = AttendanceRule.get_point(weekday)
        user.add_attendance(day_index, point)

    def finalize(self):
        for user in self.users.values():
            user.apply_bonus()
            user.evaluate_grade()

    def print_summary(self):
        for user in self.users.values():
            print(f"NAME : {user.name}, POINT : {user.points}, GRADE : {user.grade}")

        print("\nRemoved player")
        print("==============")
        for user in self.users.values():
            if user.is_inactive():
                print(user.name)


class FileLoader:
    def __init__(self, system: AttendanceSystem, filename: str):
        self.system = system
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, weekday = parts
                        system.record_attendance(name, weekday.lower())

        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {self.filename}")


if __name__ == "__main__":
    system = AttendanceSystem()
    loader = FileLoader(system, "../attendance_weekday_500.txt")
    loader.load()
    system.finalize()
    system.print_summary()
