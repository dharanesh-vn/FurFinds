import { Navigate } from "react-router-dom";
import { getStoredAuth } from "../auth";

function AdminRoute({ children }) {
  const { token, role } = getStoredAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  if (role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
}

export default AdminRoute;
