import { Navigate } from "react-router-dom";
import { getStoredAuth } from "../auth";

function ProtectedRoute({ children }) {
  const { token } = getStoredAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default ProtectedRoute;
