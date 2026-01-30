import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Support tickets", page_icon="🎫")
st.title("🎫 Support tickets")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can create a ticket, edit 
    existing tickets, and view some statistics.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]
    
    # Make up some fake project names
    project_names = [
        "Alpha Project",
        "Beta Initiative",
        "Gamma System",
        "Delta Upgrade",
        "Epsilon Migration",
        "Zeta Implementation",
        "Eta Integration",
        "Theta Deployment",
        "Iota Modernization",
        "Kappa Optimization"
    ]
    
    # Make up some fake project descriptions
    project_descriptions = [
        "Website redesign and development",
        "Mobile app development for iOS and Android",
        "Cloud infrastructure migration",
        "CRM system implementation",
        "Data analytics platform setup",
        "Security enhancement project",
        "Network infrastructure upgrade",
        "Database optimization initiative",
        "API gateway implementation",
        "DevOps pipeline automation"
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Project Name": np.random.choice(project_names, size=100),
        "Project Description": np.random.choice(project_descriptions, size=100),
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
        "Start Date": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 90))
            for _ in range(100)
        ],
        "End Date": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(91, 182))
            for _ in range(100)
        ]
    }
    df = pd.DataFrame(data)
    
    # Calculate days of completion for each ticket
    df['Days of Completion'] = (df['End Date'] - df['Start Date']).dt.days

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Add a ticket")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("Project Name")
        project_description = st.text_area("Project Description")
        issue = st.text_area("Describe the issue")
    
    with col2:
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        start_date = st.date_input("Start Date", value=datetime.date.today())
        end_date = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=30))
    
    submitted = st.form_submit_button("Submit")

if submitted:
    # Validate dates
    if end_date < start_date:
        st.error("End Date cannot be before Start Date!")
    else:
        # Calculate days of completion
        days_of_completion = (end_date - start_date).days
        
        # Make a dataframe for the new ticket and append it to the dataframe in session
        # state.
        recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        df_new = pd.DataFrame(
            [
                {
                    "ID": f"TICKET-{recent_ticket_number+1}",
                    "Project Name": project_name,
                    "Project Description": project_description,
                    "Issue": issue,
                    "Status": "Open",
                    "Priority": priority,
                    "Date Submitted": today,
                    "Start Date": start_date,
                    "End Date": end_date,
                    "Days of Completion": days_of_completion
                }
            ]
        )

        # Show a little success message.
        st.success("Ticket submitted successfully!")
        st.write("Here are the ticket details:")
        st.dataframe(df_new, use_container_width=True, hide_index=True)
        st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Existing tickets")
st.write(f"Number of tickets: `{len(st.session_state.df)}`")

st.info(
    "You can edit the tickets by double clicking on a cell. Note how the plots below "
    "update automatically! You can also sort the table by clicking on the column headers.",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_order=["ID", "Project Name", "Project Description", "Issue", "Status", 
                  "Priority", "Date Submitted", "Start Date", "End Date", "Days of Completion"],
    column_config={
        "Project Name": st.column_config.TextColumn(
            "Project Name",
            help="Name of the project",
            required=True,
        ),
        "Project Description": st.column_config.TextColumn(
            "Project Description",
            help="Description of the project",
            required=True,
        ),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
        "Date Submitted": st.column_config.DateColumn(
            "Date Submitted",
            help="Date when ticket was submitted",
            format="YYYY-MM-DD",
        ),
        "Start Date": st.column_config.DateColumn(
            "Start Date",
            help="Project start date",
            format="YYYY-MM-DD",
            required=True,
        ),
        "End Date": st.column_config.DateColumn(
            "End Date",
            help="Project end date",
            format="YYYY-MM-DD",
            required=True,
        ),
        "Days of Completion": st.column_config.NumberColumn(
            "Days of Completion",
            help="Number of days to complete the project",
            min_value=0,
            format="%d days",
        ),
    },
    # Disable editing the ID column only
    disabled=["ID"],
)

# Update Days of Completion when dates are edited
if not edited_df.equals(st.session_state.df):
    # Check if Start Date or End Date columns were modified
    if 'Start Date' in edited_df.columns and 'End Date' in edited_df.columns:
        # Recalculate Days of Completion
        edited_df['Days of Completion'] = (edited_df['End Date'] - edited_df['Start Date']).dt.days
    st.session_state.df = edited_df

# Show some metrics and charts about the ticket.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3, col4 = st.columns(4)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
avg_days_completion = st.session_state.df['Days of Completion'].mean()
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)
col4.metric(label="Avg days of completion", value=f"{avg_days_completion:.1f}", delta=-1.2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

col1, col2 = st.columns(2)

with col1:
    st.write("##### Current ticket priorities")
    priority_plot = (
        alt.Chart(edited_df)
        .mark_arc()
        .encode(theta="count():Q", color="Priority:N")
        .properties(height=300)
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

with col2:
    st.write("##### Average days of completion per project")
    # Group by project and calculate average days of completion
    project_stats = edited_df.groupby('Project Name')['Days of Completion'].mean().reset_index()
    project_stats.columns = ['Project Name', 'Avg Days of Completion']
    
    project_plot = (
        alt.Chart(project_stats)
        .mark_bar()
        .encode(
            x='Avg Days of Completion:Q',
            y=alt.Y('Project Name:N', sort='-x'),
            color=alt.Color('Project Name:N', legend=None)
        )
        .properties(height=300)
    )
    st.altair_chart(project_plot, use_container_width=True, theme="streamlit")

# Show projects overview
st.write("")
st.write("##### Projects Overview")
st.write("Summary of all projects and their ticket status:")

# Create a summary table
project_summary = edited_df.groupby(['Project Name', 'Status']).size().unstack(fill_value=0)
project_summary['Total Tickets'] = project_summary.sum(axis=1)
project_summary['Avg Days Completion'] = edited_df.groupby('Project Name')['Days of Completion'].mean()

# Display the summary
st.dataframe(project_summary, use_container_width=True)
