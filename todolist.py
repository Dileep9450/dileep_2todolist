import streamlit as st
from datetime import date

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="My To-Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main page */
    .stApp {
        background-color: #f5f7fb;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Category cards */
    .category-card {
        background: white;
        border-radius: 14px;
        padding: 18px;
        border: 1px solid #e7eaf0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        text-align: center;
        min-height: 120px;
    }

    .category-icon {
        font-size: 25px;
    }

    .category-name {
        color: #6b7280;
        font-size: 14px;
        margin-top: 5px;
    }

    .category-count {
        font-size: 27px;
        font-weight: 700;
        color: #1d4ed8;
        margin-top: 4px;
    }

    /* Task cards */
    .task-card {
        background: white;
        border: 1px solid #e6e9ef;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.03);
    }

    .task-title {
        font-size: 17px;
        font-weight: 600;
        color: #172033;
    }

    .task-completed {
        text-decoration: line-through;
        color: #9ca3af;
    }

    .task-info {
        color: #6b7280;
        font-size: 13px;
        margin-top: 6px;
    }

    /* Category badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 7px;
    }

    .health {
        background: #dcfce7;
        color: #166534;
    }

    .work {
        background: #dbeafe;
        color: #1e40af;
    }

    .mental {
        background: #f3e8ff;
        color: #7e22ce;
    }

    .others {
        background: #fef3c7;
        color: #92400e;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# ---------------------------------------------------------
# CATEGORY INFORMATION
# ---------------------------------------------------------
categories = {
    "Health": "❤️",
    "Work": "💼",
    "Mental Health": "🧠",
    "Others": "📌"
}


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def add_task(title, category, due_date, description):
    task = {
        "id": st.session_state.next_id,
        "title": title,
        "category": category,
        "due_date": due_date,
        "description": description,
        "completed": False
    }

    st.session_state.tasks.append(task)
    st.session_state.next_id += 1


def delete_task(task_id):
    st.session_state.tasks = [
        task for task in st.session_state.tasks
        if task["id"] != task_id
    ]


def complete_task(task_id, status):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = status


def get_category_count(category):
    return sum(
        1 for task in st.session_state.tasks
        if task["category"] == category
    )


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown("## ✅ My Tasks")
    st.caption("Simple productivity dashboard")

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Task",
            "📅 Calendar"
        ]
    )

    st.markdown("---")

    st.markdown("### Filter Tasks")

    filter_category = st.selectbox(
        "Category",
        ["All", "Health", "Work", "Mental Health", "Others"]
    )

    status_filter = st.selectbox(
        "Status",
        ["All", "Pending", "Completed"]
    )


# =========================================================
# DASHBOARD
# =========================================================
if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">Good day 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Manage your tasks and stay organized.</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------
    total_tasks = len(st.session_state.tasks)

    completed_tasks = sum(
        task["completed"]
        for task in st.session_state.tasks
    )

    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📋 Total Tasks",
            total_tasks
        )

    with col2:
        st.metric(
            "⏳ Pending",
            pending_tasks
        )

    with col3:
        st.metric(
            "✅ Completed",
            completed_tasks
        )

    st.markdown("---")

    # -----------------------------------------------------
    # CATEGORY CARDS
    # -----------------------------------------------------
    st.markdown("### Categories")

    c1, c2, c3, c4 = st.columns(4)

    category_columns = [
        (c1, "Health"),
        (c2, "Work"),
        (c3, "Mental Health"),
        (c4, "Others")
    ]

    for column, category in category_columns:

        with column:

            count = get_category_count(category)
            icon = categories[category]

            st.markdown(
                f"""
                <div class="category-card">
                    <div class="category-icon">{icon}</div>
                    <div class="category-name">{category}</div>
                    <div class="category-count">{count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # -----------------------------------------------------
    # TASK LIST
    # -----------------------------------------------------
    st.markdown("### My Tasks")

    search = st.text_input(
        "🔎 Search tasks",
        placeholder="Search by task name..."
    )

    filtered_tasks = []

    for task in st.session_state.tasks:

        if filter_category != "All":
            if task["category"] != filter_category:
                continue

        if status_filter == "Pending" and task["completed"]:
            continue

        if status_filter == "Completed" and not task["completed"]:
            continue

        if search:
            if search.lower() not in task["title"].lower():
                continue

        filtered_tasks.append(task)

    if not filtered_tasks:

        st.info("No tasks found. Add a new task to get started.")

    # -----------------------------------------------------
    # DISPLAY TASKS
    # -----------------------------------------------------
    for task in filtered_tasks:

        category_class = {
            "Health": "health",
            "Work": "work",
            "Mental Health": "mental",
            "Others": "others"
        }[task["category"]]

        col_check, col_content, col_edit, col_delete = st.columns(
            [0.06, 0.65, 0.14, 0.15]
        )

        with col_check:

            checked = st.checkbox(
                "Complete",
                value=task["completed"],
                key=f"check_{task['id']}",
                label_visibility="collapsed"
            )

            if checked != task["completed"]:
                complete_task(task["id"], checked)
                st.rerun()

        with col_content:

            title_class = (
                "task-completed"
                if task["completed"]
                else "task-title"
            )

            st.markdown(
                f"""
                <div class="task-card">
                    <div class="{title_class}">
                        {task["title"]}
                    </div>

                    <span class="badge {category_class}">
                        {categories[task["category"]]}
                        {task["category"]}
                    </span>

                    <div class="task-info">
                        📅 Scheduled: {task["due_date"]}
                    </div>

                    <div class="task-info">
                        {task["description"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # EDIT
        # -------------------------------------------------
        with col_edit:

            if st.button(
                "✏️ Edit",
                key=f"edit_{task['id']}"
            ):

                st.session_state[
                    f"editing_{task['id']}"
                ] = True

                st.rerun()

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------
        with col_delete:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{task['id']}"
            ):

                delete_task(task["id"])
                st.rerun()

        # -------------------------------------------------
        # EDIT FORM
        # -------------------------------------------------
        if st.session_state.get(
            f"editing_{task['id']}",
            False
        ):

            with st.expander(
                "Edit Task",
                expanded=True
            ):

                new_title = st.text_input(
                    "Task Name",
                    value=task["title"],
                    key=f"title_edit_{task['id']}"
                )

                new_category = st.selectbox(
                    "Category",
                    list(categories.keys()),
                    index=list(categories.keys()).index(
                        task["category"]
                    ),
                    key=f"category_edit_{task['id']}"
                )

                new_date = st.date_input(
                    "Schedule Date",
                    value=task["due_date"],
                    key=f"date_edit_{task['id']}"
                )

                new_description = st.text_area(
                    "Description",
                    value=task["description"],
                    key=f"description_edit_{task['id']}"
                )

                save_col, cancel_col = st.columns(2)

                with save_col:

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_{task['id']}"
                    ):

                        task["title"] = new_title
                        task["category"] = new_category
                        task["due_date"] = new_date
                        task["description"] = new_description

                        st.session_state[
                            f"editing_{task['id']}"
                        ] = False

                        st.success("Task updated successfully.")
                        st.rerun()

                with cancel_col:

                    if st.button(
                        "Cancel",
                        key=f"cancel_{task['id']}"
                    ):

                        st.session_state[
                            f"editing_{task['id']}"
                        ] = False

                        st.rerun()


# =========================================================
# ADD TASK
# =========================================================
elif menu == "➕ Add Task":

    st.markdown(
        '<div class="main-title">Add New Task</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Create and schedule a new task.</div>',
        unsafe_allow_html=True
    )

    with st.form("add_task_form"):

        title = st.text_input(
            "Task Name",
            placeholder="Example: Complete Python project"
        )

        category = st.selectbox(
            "Category",
            [
                "Health",
                "Work",
                "Mental Health",
                "Others"
            ]
        )

        due_date = st.date_input(
            "📅 Schedule Date",
            value=date.today()
        )

        description = st.text_area(
            "Description",
            placeholder="Add a short description..."
        )

        submitted = st.form_submit_button(
            "➕ Add Task",
            use_container_width=True
        )

        if submitted:

            if not title.strip():

                st.error("Please enter a task name.")

            else:

                add_task(
                    title.strip(),
                    category,
                    due_date,
                    description.strip()
                )

                st.success(
                    f"Task '{title}' added successfully!"
                )


# =========================================================
# CALENDAR
# =========================================================
elif menu == "📅 Calendar":

    st.markdown(
        '<div class="main-title">Task Calendar 📅</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View your scheduled tasks by date.</div>',
        unsafe_allow_html=True
    )

    selected_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    st.markdown("---")

    selected_tasks = [
        task for task in st.session_state.tasks
        if task["due_date"] == selected_date
    ]

    if not selected_tasks:

        st.info(
            f"No tasks scheduled for {selected_date}."
        )

    else:

        st.markdown(
            f"### Tasks for {selected_date.strftime('%d %B %Y')}"
        )

        for task in selected_tasks:

            status = (
                "✅ Completed"
                if task["completed"]
                else "⏳ Pending"
            )

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-title">
                        {categories[task["category"]]}
                        {task["title"]}
                    </div>

                    <span class="badge">
                        {task["category"]}
                    </span>

                    <div class="task-info">
                        Status: {status}
                    </div>

                    <div class="task-info">
                        {task["description"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )