import React from "react";

export default function Dashboard({ role }) {
  return (
    <div className="p-10 text-center">
      <h2 className="text-2xl mb-3">{role[0].toUpperCase() + role.slice(1)} Dashboard</h2>
      {role === "student" && <div>Student Profile View</div>}
      {role === "teacher" && <div>Student List</div>}
      {role === "admin" && <div>Analytics Dashboard</div>}
    </div>
  );
}
