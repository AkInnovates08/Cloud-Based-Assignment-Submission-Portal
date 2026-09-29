import { useEffect, useMemo, useState } from "react";
import { Routes, Route, NavLink, Navigate, useLocation, useNavigate, useParams } from "react-router-dom";
import api from "./services/api";

const icon = (name) => {
  const paths = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></>,
    file: <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h6"/></>,
    users: <><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></>,
    book: <><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></>,
    logout: <><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/><path d="M21 19V5a2 2 0 0 0-2-2h-6"/></>,
    upload: <><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M5 20h14"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
    clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
    plus: <><path d="M12 5v14M5 12h14"/></>,
    edit: <><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4Z"/></>,
    trash: <><path d="M3 6h18M8 6V4h8v2M19 6l-1 15H6L5 6M10 11v6M14 11v6"/></>,
    download: <><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></>,
    search: <><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></>,
    chevron: <path d="m9 18 6-6-6-6"/>,
  };
  return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
};

function Layout({ user, setUser, children }) {
  const nav = useNavigate();
  const location = useLocation();
  const logout = async () => {
    try { await api.post("/auth/logout"); } catch {}
    localStorage.removeItem("token"); localStorage.removeItem("user"); setUser(null); nav("/login");
  };
  const links = user?.role === "teacher"
    ? [{to:"/", label:"Dashboard", icon:"grid"}, {to:"/assignments", label:"Assignments", icon:"file"}, {to:"/teachers", label:"Teachers", icon:"users"}]
    : [{to:"/", label:"Dashboard", icon:"grid"}, {to:"/assignments", label:"Assignments", icon:"file"}, {to:"/teachers", label:"Teachers", icon:"users"}];

  if (!user) return <div className="auth-shell">{children}</div>;
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark">CA</div><div><strong>CloudAssign</strong><span>Academic Workspace</span></div></div>
      <div className="sidebar-section">Workspace</div>
      <nav className="side-nav">
        {links.map(l => <NavLink key={l.to} to={l.to} end={l.to === "/"} className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>{icon(l.icon)}<span>{l.label}</span></NavLink>)}
      </nav>
      <div className="sidebar-bottom">
        <div className="cloud-card"><div className="cloud-dot"/><div><strong>Cloud ready</strong><span>Secure assignment storage</span></div></div>
        <button className="logout-link" onClick={logout}>{icon("logout")}<span>Sign out</span></button>
      </div>
    </aside>
    <section className="main-shell">
      <header className="topbar">
        <div className="breadcrumb"><span>Workspace</span><b>/</b><strong>{location.pathname === "/" ? "Dashboard" : location.pathname.replace("/", "").replace("-", " ")}</strong></div>
        <div className="profile"><div className="avatar">{user.name?.slice(0,1).toUpperCase()}</div><div><strong>{user.name}</strong><span>{user.role}</span></div></div>
      </header>
      <main className="content">{children}</main>
    </section>
  </div>;
}

function Protected({ user, children }) { return user ? children : <Navigate to="/login" replace />; }

function AuthShell({ title, subtitle, children, footer }) {
  return <div className="auth-page"><div className="auth-brand"><div className="brand-mark">CA</div><strong>CloudAssign</strong></div><div className="auth-card"><div className="auth-heading"><span className="eyebrow">CLOUD ACADEMIC PORTAL</span><h1>{title}</h1><p>{subtitle}</p></div>{children}{footer}</div><p className="auth-foot">Assignment Submission & Feedback Portal</p></div>;
}

function Login({ setUser }) {
  const nav = useNavigate(); const [form,setForm]=useState({email:"",password:""}); const [error,setError]=useState(""); const [loading,setLoading]=useState(false);
  const submit=async(e)=>{e.preventDefault();setError("");setLoading(true);try{const r=await api.post("/auth/login",form);localStorage.setItem("token",r.data.access_token);localStorage.setItem("user",JSON.stringify(r.data.user));setUser(r.data.user);nav("/",{replace:true});}catch(x){setError(x.response?.data?.detail||"Login failed. Check your credentials.");}finally{setLoading(false)}};
  return <AuthShell title="Welcome back" subtitle="Sign in to manage assignments, submissions and feedback."><form className="auth-form" onSubmit={submit}>{error&&<div className="alert error">{error}</div>}<label>Email<input value={form.email} type="email" required placeholder="you@example.com" onChange={e=>setForm({...form,email:e.target.value})}/></label><label>Password<input value={form.password} type="password" required placeholder="Enter your password" onChange={e=>setForm({...form,password:e.target.value})}/></label><button className="primary full" disabled={loading}>{loading?"Signing in…":"Sign in"}</button></form><div className="auth-switch">New here? <NavLink to="/register">Create an account</NavLink></div></AuthShell>;
}

function Register({ setUser }) {
  const nav=useNavigate(); const [form,setForm]=useState({name:"",email:"",password:"",role:"student"}); const [error,setError]=useState(""); const [loading,setLoading]=useState(false);
  const submit=async(e)=>{e.preventDefault();setError("");setLoading(true);try{const r=await api.post("/auth/register",form);localStorage.setItem("token",r.data.access_token);localStorage.setItem("user",JSON.stringify(r.data.user));setUser(r.data.user);nav("/",{replace:true});}catch(x){setError(x.response?.data?.detail||"Registration failed.");}finally{setLoading(false)}};
  return <AuthShell title="Create your workspace" subtitle="Set up a student or teacher account in a few seconds."><form className="auth-form" onSubmit={submit}>{error&&<div className="alert error">{error}</div>}<label>Full name<input value={form.name} required placeholder="Your full name" onChange={e=>setForm({...form,name:e.target.value})}/></label><label>Email<input value={form.email} type="email" required placeholder="you@example.com" onChange={e=>setForm({...form,email:e.target.value})}/></label><label>Password<input value={form.password} minLength="8" type="password" required placeholder="At least 8 characters" onChange={e=>setForm({...form,password:e.target.value})}/></label><label>Account type<select value={form.role} onChange={e=>setForm({...form,role:e.target.value})}><option value="student">Student</option><option value="teacher">Teacher</option></select></label><button className="primary full" disabled={loading}>{loading?"Creating…":"Create account"}</button></form><div className="auth-switch">Already registered? <NavLink to="/login">Sign in</NavLink></div></AuthShell>;
}

function PageHeader({eyebrow,title,description,action}) { return <div className="page-header"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{description}</p></div>{action}</div>; }
function Loading(){return <div className="loading-card"><div className="spinner"/><span>Loading workspace…</span></div>}
function Empty({title,description}){return <div className="empty"><div className="empty-icon">{icon("file")}</div><h3>{title}</h3><p>{description}</p></div>}
function Stat({label,value,detail,iconName}){return <div className="stat-card"><div className="stat-top"><span>{label}</span><div className="stat-icon">{icon(iconName)}</div></div><strong>{value}</strong><small>{detail}</small></div>}

function Dashboard({ user }) {
  const [data,setData]=useState(null); const [error,setError]=useState("");
  useEffect(()=>{let active=true;api.get(`/dashboard/${user.role}`).then(r=>active&&setData(r.data)).catch(e=>active&&setError(e.response?.data?.detail||"Could not load dashboard."));return()=>{active=false}},[user.role]);
  if(error)return <div className="alert error">{error}</div>; if(!data)return <Loading/>;
  const teacher=user.role==="teacher";
  const stats=teacher?[{label:"Assignments",value:data.total_assignments,detail:"Created by you",iconName:"file"},{label:"Students",value:data.total_students,detail:"Registered learners",iconName:"users"},{label:"Submissions",value:data.total_submissions,detail:"Across your assignments",iconName:"upload"},{label:"Pending reviews",value:data.pending_reviews,detail:"Need grading",iconName:"clock"}]:[{label:"Assignments",value:data.total_assignments,detail:"Available to you",iconName:"file"},{label:"Submitted",value:data.submitted,detail:"Successfully uploaded",iconName:"check"},{label:"Graded",value:data.graded,detail:"Feedback available",iconName:"check"},{label:"Pending",value:data.pending,detail:"Still to submit",iconName:"clock"}];
  return <><PageHeader eyebrow="OVERVIEW" title={`Good to see you, ${user.name.split(" ")[0]}.`} description={teacher?"Monitor your courses, assignments and grading workload.":"Stay on top of deadlines, submissions and teacher feedback."} action={<NavLink className="primary" to="/assignments">{icon("file")} View assignments</NavLink>}/><div className="stats-grid">{stats.map(s=><Stat key={s.label}{...s}/>)}</div><div className="dashboard-grid"><section className="panel"><div className="panel-head"><div><span className="eyebrow">QUICK ACTIONS</span><h2>Workspace</h2></div></div><div className="quick-grid"><NavLink to="/assignments" className="quick-card"><div>{icon("file")}</div><strong>Assignments</strong><span>{teacher?"Create and manage assignments":"View deadlines and submit work"}</span></NavLink><NavLink to="/teachers" className="quick-card"><div>{icon("users")}</div><strong>Teachers</strong><span>Browse teaching profiles</span></NavLink>{teacher&&<NavLink to="/assignments?create=1" className="quick-card"><div>{icon("plus")}</div><strong>New assignment</strong><span>Publish a new task</span></NavLink>}</div></section><section className="panel workflow"><div className="panel-head"><div><span className="eyebrow">PROJECT FLOW</span><h2>How CloudAssign works</h2></div></div><div className="flow"><span>Authenticate</span><b>→</b><span>Upload</span><b>→</b><span>Store</span><b>→</b><span>Grade</span><b>→</b><span>Feedback</span></div><p>Secure authentication, REST APIs, database metadata and object/file storage work together as one cloud-ready academic workflow.</p></section></div></>;
}

function Assignments({user}) {
 const [items,setItems]=useState([]); const [courses,setCourses]=useState([]); const [selected,setSelected]=useState(null); const [subs,setSubs]=useState([]); const [loading,setLoading]=useState(true); const [error,setError]=useState(""); const [search,setSearch]=useState(""); const [showCreate,setShowCreate]=useState(false); const [editing,setEditing]=useState(null);
 const load=async()=>{setLoading(true);setError("");try{const [a,c]=await Promise.all([api.get("/assignments"),api.get("/courses")]);setItems(a.data);setCourses(c.data);}catch(e){setError(e.response?.data?.detail||"Unable to load assignments.");}finally{setLoading(false)}};
 useEffect(()=>{load()},[]);
 useEffect(()=>{const p=new URLSearchParams(window.location.search);if(user.role==="teacher"&&p.get("create"))setShowCreate(true)},[user.role]);
 const filtered=items.filter(a=>`${a.title} ${a.description}`.toLowerCase().includes(search.toLowerCase()));
 const remove=async(id)=>{if(!confirm("Delete this assignment?"))return;try{await api.delete(`/assignments/${id}`);setItems(items.filter(x=>x.id!==id));}catch(e){setError(e.response?.data?.detail||"Delete failed.")}};
 const viewSubs=async(a)=>{setSelected(a);try{const r=await api.get(`/assignments/${a.id}/submissions`);setSubs(r.data)}catch(e){setError(e.response?.data?.detail||"Could not load submissions.")}};
 if(loading)return <Loading/>;
 return <><PageHeader eyebrow="ACADEMIC WORK" title="Assignments" description={user.role==="teacher"?"Create, update, review and grade your course assignments.":"Find your coursework, check deadlines and submit your files."} action={user.role==="teacher"&&<button className="primary" onClick={()=>{setEditing(null);setShowCreate(true)}}>{icon("plus")} New assignment</button>}/>{error&&<div className="alert error">{error}</div>}<div className="toolbar"><div className="searchbox">{icon("search")}<input placeholder="Search assignments…" value={search} onChange={e=>setSearch(e.target.value)}/></div><span className="result-count">{filtered.length} assignment{filtered.length!==1?"s":""}</span></div>{filtered.length===0?<Empty title="No assignments found" description={search?"Try a different search term.":"Assignments will appear here once they are created."}/>:<div className="assignment-grid">{filtered.map(a=><AssignmentCard key={a.id} assignment={a} user={user} onSubmit={setSelected} onEdit={()=>{setEditing(a);setShowCreate(true)}} onDelete={()=>remove(a.id)} onSubmissions={()=>viewSubs(a)}/>)}</div>}{showCreate&&<AssignmentModal courses={courses} initial={editing} onClose={()=>setShowCreate(false)} onSaved={()=>{setShowCreate(false);load()}}/>}{selected&&user.role==="student"&&<SubmissionModal assignment={selected} onClose={()=>setSelected(null)} onUploaded={()=>setSelected(null)}/>} {selected&&user.role==="teacher"&&<ReviewModal assignment={selected} submissions={subs} onClose={()=>setSelected(null)} onChanged={()=>viewSubs(selected)}/>}</>;
}

function AssignmentCard({assignment,user,onSubmit,onEdit,onDelete,onSubmissions}){
 const deadline=new Date(assignment.deadline); const overdue=deadline<new Date();
 return <article className="assignment-card"><div className="assignment-top"><span className={`status ${overdue?"late":"open"}`}>{overdue?"Past deadline":"Open"}</span><span className="marks">{assignment.max_marks} marks</span></div><h3>{assignment.title}</h3><p>{assignment.description||"No description provided."}</p><div className="meta-row"><span>{icon("clock")} {deadline.toLocaleDateString()} · {deadline.toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})}</span><span>{assignment.allowed_file_types}</span></div><div className="card-actions">{user.role==="student"?<button className="primary small" onClick={()=>onSubmit(assignment)}>{icon("upload")} Submit work</button>:<><button className="ghost small" onClick={onSubmissions}>View submissions</button><button className="icon-btn" title="Edit" onClick={onEdit}>{icon("edit")}</button><button className="icon-btn danger" title="Delete" onClick={onDelete}>{icon("trash")}</button></>}</div></article>
}

function AssignmentModal({ courses, initial, onClose, onSaved, onCoursesChanged }) {
  const [courseList, setCourseList] = useState(courses || []);

  const [form, setForm] = useState(
    initial
      ? {
          ...initial,
          deadline: new Date(initial.deadline)
            .toISOString()
            .slice(0, 16),
        }
      : {
          course_id: "",
          title: "",
          description: "",
          deadline: "",
          max_marks: 100,
          allowed_file_types: "pdf,docx,txt",
          max_file_size_mb: 10,
        }
  );

  const [courseName, setCourseName] = useState("");
  const [showCourseForm, setShowCourseForm] = useState(false);

  const [error, setError] = useState("");
  const [courseError, setCourseError] = useState("");

  const [loading, setLoading] = useState(false);
  const [courseLoading, setCourseLoading] = useState(false);

  /*
   * Load teacher's courses whenever the modal opens.
   */
  useEffect(() => {
    loadCourses();
  }, []);

  async function loadCourses() {
    try {
      const response = await api.get("/courses");

      setCourseList(response.data || []);

      /*
       * If there is no selected course yet,
       * automatically select the first available course.
       */
      if (!initial && !form.course_id && response.data?.length > 0) {
        setForm((current) => ({
          ...current,
          course_id: String(response.data[0].id),
        }));
      }
    } catch (error) {
      console.error("Failed to load courses:", error);
      setCourseError(
        error.response?.data?.detail ||
          "Unable to load courses."
      );
    }
  }

  /*
   * Create a new course.
   */
  async function createCourse(e) {
    e.preventDefault();

    if (!courseName.trim()) {
      setCourseError("Please enter a course name.");
      return;
    }

    setCourseLoading(true);
    setCourseError("");

    try {
      const response = await api.post("/courses", {
        course_name: courseName.trim(),
      });

      const newCourse = response.data;

      /*
       * Add the newly created course to dropdown.
       */
      setCourseList((current) => [
        newCourse,
        ...current,
      ]);

      /*
       * Automatically select newly created course.
       */
      setForm((current) => ({
        ...current,
        course_id: String(newCourse.id),
      }));

      setCourseName("");
      setShowCourseForm(false);

      /*
       * Update parent course list too.
       */
      if (onCoursesChanged) {
        onCoursesChanged();
      }
    } catch (error) {
      setCourseError(
        error.response?.data?.detail ||
          "Could not create course."
      );
    } finally {
      setCourseLoading(false);
    }
  }

  /*
   * Create / update assignment.
   */
  async function submit(e) {
    e.preventDefault();

    if (!form.course_id) {
      setError("Please select a course first.");
      return;
    }

    if (!form.title.trim()) {
      setError("Please enter an assignment title.");
      return;
    }

    if (!form.deadline) {
      setError("Please select a deadline.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const body = {
        course_id: Number(form.course_id),
        title: form.title.trim(),
        description: form.description,
        deadline: new Date(form.deadline).toISOString(),
        max_marks: Number(form.max_marks),
        allowed_file_types: form.allowed_file_types,
        max_file_size_mb: Number(form.max_file_size_mb),
      };

      if (initial) {
        await api.put(
          `/assignments/${initial.id}`,
          body
        );
      } else {
        await api.post("/assignments", body);
      }

      onSaved();
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          "Could not save assignment."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-backdrop">
      <div className="modal">

        {/* HEADER */}
        <div className="modal-head">
          <div>
            <span className="eyebrow">
              {initial ? "EDIT" : "CREATE"}
            </span>

            <h2>
              {initial
                ? "Update assignment"
                : "New assignment"}
            </h2>
          </div>

          <button
            className="icon-btn"
            type="button"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        {/* GENERAL ERROR */}
        {error && (
          <div className="alert error">
            {error}
          </div>
        )}

        {/* COURSE SECTION */}
        <div className="course-manager">

          <div className="course-manager-header">
            <div>
              <span className="eyebrow">
                COURSE
              </span>

              <h3>
                Assignment course
              </h3>

              <p className="muted">
                Select an existing course or create a new one.
              </p>
            </div>

            <button
              type="button"
              className="secondary small"
              onClick={() =>
                setShowCourseForm((value) => !value)
              }
            >
              {showCourseForm
                ? "Cancel"
                : "+ New Course"}
            </button>
          </div>

          {/* CREATE COURSE */}
          {showCourseForm && (
            <form
              className="create-course-box"
              onSubmit={createCourse}
            >
              <label>
                Course name

                <input
                  type="text"
                  placeholder="e.g. Cloud Computing"
                  value={courseName}
                  onChange={(e) =>
                    setCourseName(e.target.value)
                  }
                  autoFocus
                />
              </label>

              <button
                className="primary small"
                disabled={courseLoading}
              >
                {courseLoading
                  ? "Creating..."
                  : "Create Course"}
              </button>
            </form>
          )}

          {courseError && (
            <div className="alert error">
              {courseError}
            </div>
          )}

          {/* COURSE DROPDOWN */}
          <label>
            Select course

            <select
              required
              value={form.course_id}
              onChange={(e) =>
                setForm({
                  ...form,
                  course_id: e.target.value,
                })
              }
            >
              <option value="">
                Select a course
              </option>

              {courseList.map((course) => (
                <option
                  key={course.id}
                  value={course.id}
                >
                  {course.course_name}
                </option>
              ))}
            </select>
          </label>

          {courseList.length === 0 && (
            <div className="course-empty">
              <strong>
                No courses available
              </strong>

              <span>
                Create your first course using
                <b> + New Course</b>.
              </span>
            </div>
          )}
        </div>

        {/* ASSIGNMENT FORM */}
        <form
          className="modal-form"
          onSubmit={submit}
        >

          <label>
            Assignment title

            <input
              required
              placeholder="e.g. Cloud Architecture Report"
              value={form.title}
              onChange={(e) =>
                setForm({
                  ...form,
                  title: e.target.value,
                })
              }
            />
          </label>

          <label>
            Maximum marks

            <input
              type="number"
              min="1"
              max="1000"
              value={form.max_marks}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_marks: e.target.value,
                })
              }
            />
          </label>

          <label className="span-2">
            Description

            <textarea
              rows="4"
              placeholder="Describe the assignment requirements..."
              value={form.description}
              onChange={(e) =>
                setForm({
                  ...form,
                  description: e.target.value,
                })
              }
            />
          </label>

          <label>
            Deadline

            <input
              type="datetime-local"
              required
              value={form.deadline}
              onChange={(e) =>
                setForm({
                  ...form,
                  deadline: e.target.value,
                })
              }
            />
          </label>

          <label>
            Maximum file size

            <input
              type="number"
              min="1"
              max="100"
              value={form.max_file_size_mb}
              onChange={(e) =>
                setForm({
                  ...form,
                  max_file_size_mb: e.target.value,
                })
              }
            />

            <small className="field-help">
              Size in MB
            </small>
          </label>

          <label>
            Allowed file types

            <input
              value={form.allowed_file_types}
              onChange={(e) =>
                setForm({
                  ...form,
                  allowed_file_types: e.target.value,
                })
              }
            />

            <small className="field-help">
              Example: pdf,docx,txt
            </small>
          </label>

          {/* ACTIONS */}
          <div className="modal-actions span-2">

            <button
              type="button"
              className="ghost"
              onClick={onClose}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="primary"
              disabled={
                loading ||
                courseList.length === 0
              }
            >
              {loading
                ? "Saving..."
                : initial
                ? "Save Changes"
                : "Create Assignment"}
            </button>

          </div>

        </form>
      </div>
    </div>
  );
}
function SubmissionModal({assignment,onClose,onUploaded}){const [file,setFile]=useState(null);const [error,setError]=useState("");const [loading,setLoading]=useState(false);const submit=async()=>{if(!file)return setError("Choose a file first.");setLoading(true);setError("");const fd=new FormData();fd.append("file",file);try{await api.post(`/assignments/${assignment.id}/submit`,fd);onUploaded()}catch(e){setError(e.response?.data?.detail||"Upload failed.")}finally{setLoading(false)}};return <div className="modal-backdrop"><div className="modal compact"><div className="modal-head"><div><span className="eyebrow">SUBMISSION</span><h2>{assignment.title}</h2></div><button className="icon-btn" onClick={onClose}>×</button></div><p className="muted">Upload a file before {new Date(assignment.deadline).toLocaleString()}.</p>{error&&<div className="alert error">{error}</div>}<label className="dropzone">{icon("upload")}<strong>{file?file.name:"Choose your assignment file"}</strong><span>Allowed: {assignment.allowed_file_types} · Up to {assignment.max_file_size_mb} MB</span><input type="file" onChange={e=>setFile(e.target.files?.[0]||null)}/></label><div className="modal-actions"><button className="ghost" onClick={onClose}>Cancel</button><button className="primary" onClick={submit} disabled={loading}>{loading?"Uploading…":"Upload submission"}</button></div></div></div>}

function ReviewModal({assignment,submissions,onClose,onChanged}){const [selected,setSelected]=useState(null);return <div className="modal-backdrop"><div className="modal wide"><div className="modal-head"><div><span className="eyebrow">TEACHER REVIEW</span><h2>{assignment.title}</h2><p>{submissions.length} submission{submissions.length!==1?"s":""}</p></div><button className="icon-btn" onClick={onClose}>×</button></div>{submissions.length===0?<Empty title="No submissions yet" description="Students have not submitted work for this assignment."/>:<div className="review-list">{submissions.map(s=><div className="review-row" key={s.id}><div><strong>Student #{s.student_id}</strong><span>{s.file_name} · {new Date(s.submitted_at).toLocaleString()}</span></div><span className={`status ${s.submission_status.toLowerCase()==="late"?"late":"open"}`}>{s.submission_status}</span><button className="ghost small" onClick={()=>setSelected(s)}>Grade</button>{s.marks!=null&&<strong className="score">{s.marks}/{assignment.max_marks}</strong>}</div>)}</div>}{selected&&<GradeForm submission={selected} maxMarks={assignment.max_marks} onClose={()=>setSelected(null)} onSaved={()=>{setSelected(null);onChanged()}}/>}</div></div>}
function GradeForm({submission,maxMarks,onClose,onSaved}){const [marks,setMarks]=useState(submission.marks??"");const [feedback,setFeedback]=useState(submission.feedback??"");const [error,setError]=useState("");const [loading,setLoading]=useState(false);const save=async()=>{if(marks===""||Number(marks)<0||Number(marks)>maxMarks)return setError(`Marks must be between 0 and ${maxMarks}.`);setLoading(true);try{await api.post(`/submissions/${submission.id}/grade`,{marks:Number(marks),feedback});onSaved()}catch(e){setError(e.response?.data?.detail||"Could not save grade.")}finally{setLoading(false)}};return <div className="inline-grade"><h3>Grade submission</h3>{error&&<div className="alert error">{error}</div>}<div className="grade-grid"><label>Marks<input type="number" min="0" max={maxMarks} value={marks} onChange={e=>setMarks(e.target.value)}/></label><label>Feedback<textarea value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder="Write constructive feedback…"/></label></div><div className="modal-actions"><button className="ghost" onClick={onClose}>Cancel</button><button className="primary" onClick={save} disabled={loading}>{loading?"Saving…":"Save grade"}</button></div></div>}

function Teachers(){const [teachers,setTeachers]=useState([]);const [loading,setLoading]=useState(true);const [error,setError]=useState("");useEffect(()=>{api.get("/teachers").then(r=>setTeachers(r.data)).catch(e=>setError(e.response?.data?.detail||"Could not load teachers.")).finally(()=>setLoading(false))},[]);if(loading)return <Loading/>;return <><PageHeader eyebrow="PEOPLE" title="Teachers" description="Teaching profiles connected to the assignment workspace."/><div className="teacher-grid">{error?<div className="alert error">{error}</div>:teachers.length===0?<Empty title="No teachers found" description="Create a teacher account to see profiles here."/>:teachers.map(t=><article className="teacher-card" key={t.id}><div className="teacher-avatar">{t.name.slice(0,1).toUpperCase()}</div><div><h3>{t.name}</h3><p>{t.email}</p><span className="role-pill">Teacher</span></div></article>)}</div></>}

export default function App(){const [user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem("user")||"null")}catch{return null}});return <Layout user={user} setUser={setUser}><Routes><Route path="/login" element={user?<Navigate to="/" replace/>:<Login setUser={setUser}/>}/><Route path="/register" element={user?<Navigate to="/" replace/>:<Register setUser={setUser}/>}/><Route path="/" element={<Protected user={user}><Dashboard user={user}/></Protected>}/><Route path="/assignments" element={<Protected user={user}><Assignments user={user}/></Protected>}/><Route path="/teachers" element={<Protected user={user}><Teachers/></Protected>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes></Layout>}
