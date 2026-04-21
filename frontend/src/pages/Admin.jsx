import { useEffect, useState } from "react";
import { deletePet, extractErrorMessage, getAdminUsers, getPets, updatePet } from "../api";

function Admin() {
  const [users, setUsers] = useState([]);
  const [pets, setPets] = useState([]);
  const [error, setError] = useState("");
  const [editingPetId, setEditingPetId] = useState(null);
  const [editForm, setEditForm] = useState(null);

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

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      load();
    }, 0);
    return () => clearTimeout(timeoutId);
  }, []);

  const beginEdit = (pet) => {
    setEditingPetId(pet.id);
    setEditForm({
      name: pet.name,
      type: pet.type,
      breed: pet.breed,
      age: pet.age,
      gender: pet.gender,
      vaccinated: pet.vaccinated,
      sterilized: pet.sterilized,
      description: pet.description || "",
      image_url: pet.image_url || "",
      shelter_name: pet.shelter_name || "",
      contact_person: pet.contact_person || "",
      phone: pet.phone || "",
      email: pet.email || "",
      city: pet.city,
    });
  };

  const cancelEdit = () => {
    setEditingPetId(null);
    setEditForm(null);
  };

  const saveEdit = async (petId) => {
    if (!editForm) {
      return;
    }
    try {
      await updatePet(petId, editForm);
      cancelEdit();
      await load();
    } catch (err) {
      setError(extractErrorMessage(err, "Unable to update pet."));
    }
  };

  const removePet = async (petId) => {
    try {
      await deletePet(petId);
      setPets((current) => current.filter((pet) => pet.id !== petId));
      setError("");
    } catch (err) {
      setError(extractErrorMessage(err, "Unable to delete pet."));
    }
  };

  return (
    <section className="card">
      <h2>Admin Dashboard</h2>
      <p className="helper-text">Manage pet records and monitor platform inventory in one place.</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="stats-grid">
        <div className="stat-item">
          <h3>{pets.length}</h3>
          <p>Total Pets</p>
        </div>
        <div className="stat-item">
          <h3>{pets.filter((pet) => pet.adopted).length}</h3>
          <p>Adopted</p>
        </div>
        <div className="stat-item">
          <h3>{pets.filter((pet) => !pet.adopted).length}</h3>
          <p>Available</p>
        </div>
      </div>

      <h3>Users</h3>
      <ul className="simple-list">
        {users.map((user) => (
          <li key={user.id}>
            {user.name} - {user.email} ({user.role})
          </li>
        ))}
      </ul>
      <h3>Pet Management</h3>
      <div className="table-wrap">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Breed</th>
              <th>Age</th>
              <th>Gender</th>
              <th>City</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {pets.map((pet) => {
              const isEditing = editingPetId === pet.id;
              return (
                <tr key={pet.id}>
                  <td>
                    {isEditing ? (
                      <input
                        value={editForm?.name || ""}
                        onChange={(e) => setEditForm((v) => ({ ...v, name: e.target.value }))}
                      />
                    ) : (
                      pet.name
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <input
                        value={editForm?.type || ""}
                        onChange={(e) => setEditForm((v) => ({ ...v, type: e.target.value }))}
                      />
                    ) : (
                      pet.type
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <input
                        value={editForm?.breed || ""}
                        onChange={(e) => setEditForm((v) => ({ ...v, breed: e.target.value }))}
                      />
                    ) : (
                      pet.breed
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <input
                        value={editForm?.age || ""}
                        onChange={(e) => setEditForm((v) => ({ ...v, age: e.target.value }))}
                      />
                    ) : (
                      pet.age
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <select
                        value={editForm?.gender || "Male"}
                        onChange={(e) => setEditForm((v) => ({ ...v, gender: e.target.value }))}
                      >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                      </select>
                    ) : (
                      pet.gender
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <input
                        value={editForm?.city || ""}
                        onChange={(e) => setEditForm((v) => ({ ...v, city: e.target.value }))}
                      />
                    ) : (
                      pet.city
                    )}
                  </td>
                  <td>{pet.adopted ? "Adopted" : "Available"}</td>
                  <td className="admin-actions">
                    {isEditing ? (
                      <>
                        <button type="button" onClick={() => saveEdit(pet.id)}>
                          Save
                        </button>
                        <button type="button" className="button-link secondary" onClick={cancelEdit}>
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button type="button" onClick={() => beginEdit(pet)}>
                          Edit
                        </button>
                        <button type="button" className="button-link secondary" onClick={() => removePet(pet.id)}>
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default Admin;
