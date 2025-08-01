number = {}
id_cnt = 0

# dat[사용자ID][요일]
attendance_user = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
names = [''] * 100
weekday_count = [0] * 100
weekend_count = [0] * 100

DAY_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

DAY_POINT = {
    "monday": 1,
    "tuesday": 1,
    "wednesday": 3,
    "thursday": 1,
    "friday": 1,
    "saturday": 2,
    "sunday": 2
}

GRADE_SCORE = [
    (1, 50),
    (2, 30),
    (3, 0)
]

def get_day_index(_day):
    return DAY_INDEX[_day]

def get_day_point(_day):
    return DAY_POINT[_day]

def record_attendance(_name, _day):
    global id_cnt

    if _name not in number:
        id_cnt += 1
        number[_name] = id_cnt
        names[id_cnt] = _name

    num_id = number[_name]

    add_point = 0
    add_point += get_day_point(_day)
    index = get_day_index(_day)

    if index == 2:
        weekday_count[num_id] += 1
    elif index == 5 or index == 6:
        weekend_count[num_id] += 1

    attendance_user[num_id][index] += 1
    points[num_id] += add_point

def print_result(_name, _points, _grade):
    print(f"NAME : {_name}, POINT : {_points}, GRADE : ", end="")

    if _grade == 1:
        print("GOLD")
    elif _grade == 2:
        print("SILVER")
    else:
        print("NORMAL")

def decide_grade(idx, grade_rules=None):
    if grade_rules is None:
        grade_rules = GRADE_SCORE
    for g, threshold in grade_rules:
        if points[idx] >= threshold:
            grade[idx] = g
            return

def update_bonus_point(idx):
    if attendance_user[idx][DAY_INDEX["wednesday"]] > 9:
        points[idx] += 10
    if attendance_user[idx][DAY_INDEX["saturday"]] + attendance_user[idx][DAY_INDEX["sunday"]] > 9:
        points[idx] += 10

def update_grade():
    for i in range(1, id_cnt + 1):
        update_bonus_point(i)

        decide_grade(i, GRADE_SCORE)
        print_result(names[i], points[i], grade[i])

def removed_player(idx):
    if grade[idx] not in (1, 2) and weekday_count[idx] == 0 and weekend_count[idx] == 0:
        print(names[idx])

def load_info_file(file_name):
    try:
        with open(file_name, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    record_attendance(parts[0], parts[1])

        update_grade()
        print("\nRemoved player")
        print("==============")
        for i in range(1, id_cnt + 1):
            removed_player(i)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    load_info_file("../attendance_weekday_500.txt")
