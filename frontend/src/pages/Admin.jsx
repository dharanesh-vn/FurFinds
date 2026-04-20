import { useEffect, useState } from "react";
import { extractErrorMessage, getAdminUsers, getPets } from "../api";

function Admin() {
  const [users, setUsers] = useState([]);
  const [pets, setPets] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [usersResponse, petsResponse] = await Promise.all([getAdminUsers(), getPets()]);
        setUsers(usersResponse.data);
        setPets(petsResponse.data);
        setError("");
      } catch (err) {
        setError(extractErrorMessage(err, "Admin data could not be loaded."));
      }
    };
    load();
  }, []);

  return (
    <section className="card">
      <h2>Admin Panel</h2>
      {error ? <p className="error-text">{error}</p> : null}
      <h3>All Users</h3>
      <ul className="simple-list">
        {users.map((user) => (
          <li key={user.id}>
            {user.name} - {user.email} ({user.role})
          </li>
        ))}
      </ul>
      <h3>All Pets</h3>
      <ul className="simple-list">
        {pets.map((pet) => (
          <li key={pet.id}>
            {pet.name} - {pet.type} - {pet.adopted ? "Adopted" : "Available"}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Admin;
