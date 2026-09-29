def register(client, email, role):
    return client.post("/api/auth/register", json={
        "name": role.title(), "email": email, "password": "Password123!", "role": role
    })

def auth(client, email, password="Password123!"):
    r=client.post("/api/auth/login", json={"email":email,"password":password})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def test_register_login_and_role_protection(client):
    assert register(client,"teacher@test.local","teacher").status_code == 201
    assert register(client,"student@test.local","student").status_code == 201
    student_headers=auth(client,"student@test.local")
    assert client.get("/api/dashboard/teacher",headers=student_headers).status_code == 403

def test_teacher_creates_course_and_assignment(client):
    register(client,"teacher2@test.local","teacher")
    h=auth(client,"teacher2@test.local")
    c=client.post("/api/courses",headers=h,json={"course_name":"Cloud Computing"})
    assert c.status_code == 201
    a=client.post("/api/assignments",headers=h,json={
        "course_id":c.json()["id"],"title":"Cloud Assignment","description":"Demo",
        "deadline":"2030-01-01T12:00:00Z","max_marks":100,
        "allowed_file_types":"pdf","max_file_size_mb":2
    })
    assert a.status_code == 201

def test_student_upload_and_teacher_grade(client):
    register(client,"teacher3@test.local","teacher")
    th=auth(client,"teacher3@test.local")
    c=client.post("/api/courses",headers=th,json={"course_name":"Distributed Systems"})
    a=client.post("/api/assignments",headers=th,json={
        "course_id":c.json()["id"],"title":"Report","description":"",
        "deadline":"2030-01-01T12:00:00Z","max_marks":50,
        "allowed_file_types":"pdf","max_file_size_mb":2
    })
    register(client,"student3@test.local","student")
    sh=auth(client,"student3@test.local")
    s=client.post(f"/api/assignments/{a.json()['id']}/submit",headers=sh,files={"file":("report.pdf",b"%PDF-demo","application/pdf")})
    assert s.status_code == 201
    sid=s.json()["id"]
    assert client.post(f"/api/submissions/{sid}/grade",headers=sh,json={"marks":10,"feedback":"x"}).status_code == 403
    g=client.post(f"/api/submissions/{sid}/grade",headers=th,json={"marks":45,"feedback":"Good work"})
    assert g.status_code == 200 and g.json()["submission_status"] == "GRADED"

def test_marks_above_max_rejected(client):
    register(client,"teacher4@test.local","teacher"); th=auth(client,"teacher4@test.local")
    c=client.post("/api/courses",headers=th,json={"course_name":"Cloud"})
    a=client.post("/api/assignments",headers=th,json={"course_id":c.json()["id"],"title":"A","description":"","deadline":"2030-01-01T12:00:00Z","max_marks":10,"allowed_file_types":"pdf","max_file_size_mb":2})
    register(client,"student4@test.local","student"); sh=auth(client,"student4@test.local")
    s=client.post(f"/api/assignments/{a.json()['id']}/submit",headers=sh,files={"file":("a.pdf",b"%PDF","application/pdf")})
    g=client.post(f"/api/submissions/{s.json()['id']}/grade",headers=th,json={"marks":11,"feedback":"bad"})
    assert g.status_code == 400
