import streamlit as st
import pandas as pd
from csv_manager import load_csv_data, save_csv_data

# Simple Member class using basic OOP features.
class Member:
    def __init__(self, member_id, name, age, gender, trainer, membership, fee, status):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.gender = gender
        self.trainer = trainer
        self.membership = membership
        self.fee = fee
        self.status = status

    def to_dict(self):
        return {
            "ID": self.member_id,
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Trainer": self.trainer,
            "Membership": self.membership,
            "Fee": self.fee,
            "Status": self.status,
        }

# Member management page for adding, viewing, searching and deleting members.
def show_member_management():
    st.title("Member Management")
    st.markdown("Manage gym members using CSV storage and beginner-friendly code.")

    members = load_csv_data("members.csv")
    action = st.selectbox("Choose action", ["Add Member", "View Members", "Search Member", "Delete Member"])

    if action == "Add Member":
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        trainer = st.text_input("Trainer Name")
        membership = st.selectbox("Membership Type", ["Monthly", "Quarterly", "Yearly"])
        fee = st.number_input("Membership Fee", min_value=0, value=50)
        status = st.selectbox("Status", ["Active", "Inactive"])

        if st.button("Add Member"):
            next_id = int(members["ID"].max()) + 1 if not members.empty else 1
            new_member = Member(next_id, name, age, gender, trainer, membership, fee, status)
            members = members.append(new_member.to_dict(), ignore_index=True)
            save_csv_data(members, "members.csv")
            st.success("Member added successfully.")

    elif action == "View Members":
        st.subheader("All Members")
        if not members.empty:
            st.dataframe(members)
        else:
            st.write("No members found.")

    elif action == "Search Member":
        search_name = st.text_input("Enter name to search")
        if st.button("Search"):
            if search_name:
                filtered = members[members["Name"].str.contains(search_name, case=False, na=False)]
                st.dataframe(filtered)
            else:
                st.write("Please enter a name to search.")

    elif action == "Delete Member":
        if members.empty:
            st.write("No members to delete.")
        else:
            member_options = [f"{row['ID']}: {row['Name']}" for _, row in members.iterrows()]
            selected = st.selectbox("Select member to delete", member_options)
            if st.button("Delete Member"):
                selected_id = int(selected.split(":")[0])
                members = members[members["ID"] != selected_id]
                save_csv_data(members, "members.csv")
                st.success("Member deleted successfully.")
