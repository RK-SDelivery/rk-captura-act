import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.html("""
    <style>
        .stMainBlockContainer {
            max-width:60rem;
        }
    </style>
    """
)

# TODO: switch options for the Snowflake's
client_op = ["Raken", "KOF", "Grupo Bafar", "Transnetwork"]
activity_op = ["Administrativas", "Desarrollo","Preventa", "Innovación"]
consultants = ["Juan Carlos Hernández", "Juan José Reyes", "Víctor Rivera", "Alonso Melgar", "Teodoro Macías", "Myriam Barrera", "Elizabeth Monroy"]

def get_week_range(selected_date):
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=4)
    return start_of_week, end_of_week

def main():
    st.title("Time registry")
    
    col1, col2 = st.columns(2)

    # Employee Selection
    employee = col1.selectbox("Consultant:", consultants)
    
    # Week Selection
    selected_date = col2.date_input("Week:", datetime.today())
    start_of_week, end_of_week = get_week_range(selected_date)
    week_display = f"{start_of_week.strftime('%A, %B %d, %Y')} to {end_of_week.strftime('%A, %B %d, %Y')}"
    st.write(f"**Selected week:** {week_display}")
    
    # Table for capturing activities
    columns = ["Client", "Project", "Activity", "Mon", "Tue", "Wed", "Thu", "Fri"]
    data = pd.DataFrame(columns=columns)
    edited_df = st.data_editor(data, num_rows="dynamic", width=1000, hide_index=True, 
                               column_config = {
                                   "Client" : st.column_config.SelectboxColumn(options=client_op, width=100),
                                   "Project" : st.column_config.TextColumn(width=300),
                                   "Activity" : st.column_config.SelectboxColumn(options = activity_op, width = 140),
                                   "Mon" : st.column_config.NumberColumn(width=70, min_value=0.5),
                                   "Tue" : st.column_config.NumberColumn(width=70, min_value=0.5),
                                   "Wed" : st.column_config.NumberColumn(width=70, min_value=0.5),
                                   "Thu" : st.column_config.NumberColumn(width=70, min_value=0.5),
                                   "Fri" : st.column_config.NumberColumn(width=70, min_value=0.5),
                               })
    
    try:
        total_hours = edited_df[['Mon', 'Tue', 'Wed', 'Thu', 'Fri']].sum().sum()
        st.write(f"Total horas capturadas: {total_hours}")
    except:
        st.write("Total horas capturadas: 0")

    # Submit button
    if st.button("Validate", type="primary"):
        csv_filename = f"time_registry_{employee.replace(' ', '_')}.csv"
        df_expanded = []
        edited_df.fillna(0, inplace = True)
        
        for _, row in edited_df.iterrows():
            for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
                if float(row[day]) > 0:
                    df_expanded.append([employee, start_of_week + timedelta(days=i), row["Client"], row["Project"], row["Activity"], row[day]])
        
        df_final = pd.DataFrame(df_expanded, columns=["Consultant", "Date", "Client", "Project", "Activity", "Hours"]).sort_values(by=['Date', 'Client'])
        if total_hours < 40:
            st.warning("Total hours < 40")
        else:
            st.success(f"Time registred as {csv_filename}")
        st.dataframe(df_final, hide_index=True)
        st.download_button("Send", df_final.to_csv(index=False), file_name=csv_filename, mime = "text/csv", icon=":material/download:", type = "primary")
            
        
        
    

if __name__ == "__main__":
    main()
