# ⁡⁢⁣⁣الخطوة الأولى⁡
# ⁣استيراد المكتبة أو لنقل بتعبير أدق استيراد المحرك⁡
import sqlite3

# ⁡⁢⁣⁣الخطوة الثانية⁡
# إنشاء الاتصال (𝘊𝘰𝘯𝘯𝘦𝘤𝘵𝘪𝘰𝘯)
conn = sqlite3.connect('school_database.db')

# ⁡⁢⁣⁣الخطوة الثالثة⁡
# إنشاء المؤشر (Cursor)
cursor = conn.cursor()

# ⁡⁢⁣⁣الخطوة الرابعة ⁡
# تنفيذ الاستعلامات(Executing Queries) 
# ⁡⁣⁣⁢إنشاء جدول ⁡
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    grade INTEGER
)
''')

# ⁡⁣⁣⁢إضافة طالب جديد إلى جدول الطلاب⁡
# cursor.execute(
#   """
#   INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
#   """,
#   ("Khdija nour", 13, 3)
# )



# ⁡⁢⁣⁣الخطوة الخامسة⁡
# الالتزام بالتغييرات (Committing Changes) 
conn.commit()


# ⁡⁣⁣⁢طباعة كل الطلاب⁡
All_students = cursor.execute("SELECT * FROM students").fetchall()
#print(All_students)

# ⁡⁣⁣⁢طباعة طلاب الفصل الأول فقط ⁡⁡
First_grade_students = cursor.execute("SELECT * FROM students WHERE grade=1").fetchall()
print(First_grade_students)

# ⁡⁣⁣⁢تحديث أو تغيير فصل طالب محدد⁡
cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (2, "Ahmed karim"))

# ⁡⁣⁣⁢حذف سجل طالب محدد ⁡
cursor.execute("DELETE FROM students WHERE name = ?", ("Ahmed karim",))

# ⁡⁢⁣⁢لا تنس التغييرات في قاعدة البيانات⁡
conn.commit()

# ⁡⁢⁣⁣الخطوة السادسة⁡
# إغلاق الاتصال (Closing the Connection)
conn.close()