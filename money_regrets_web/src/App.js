import React, { useEffect, useState } from 'react';
import { getUsers, createUser, updateUser, deleteUser } from './api';
import Navigation from './Navigation';
import ListGroup from './users/ListGroup';
import Form from './users/Form';

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [formMode, setFormMode] = useState('view'); // 'view', 'edit', 'create'

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (e) {
      setError(
        e.message.includes('Failed to fetch')
          ? 'API is not accessible. Please check that the backend is running and reachable.'
          : e.message
      );
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createUser(form);
      setForm({ name: '', email: '', password: '' });
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  const handleDelete = async (uuid) => {
    setLoading(true);
    setError('');
    try {
      await deleteUser(uuid);
      if (selectedUser && selectedUser.uuid === uuid) setSelectedUser(null);
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  const handleAddUserClick = () => {
    setForm({ name: '', email: '', password: '' });
    setSelectedUser(null);
    setFormMode('create');
  };

  const handleSelectUser = (user) => {
    setSelectedUser(user);
    setFormMode('view');
  };

  const handleEdit = () => {
    setForm(selectedUser ? { ...selectedUser, password: '' } : { name: '', email: '', password: '' });
    setFormMode('edit');
  };

  const handleCancel = () => {
    setFormMode(selectedUser ? 'view' : 'create');
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createUser(form);
      setForm({ name: '', email: '', password: '' });
      setFormMode('view');
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await updateUser(selectedUser.uuid, form);
      setFormMode('view');
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  const handleDeleteUser = async () => {
    if (!selectedUser) return;
    setLoading(true);
    setError('');
    try {
      await deleteUser(selectedUser.uuid);
      setSelectedUser(null);
      setForm({ name: '', email: '', password: '' });
      setFormMode('create');
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="container-fluid">
      <div className="row min-vh-100">
        <nav className="col-2 col-md-2 bg-light border-end p-0 d-flex flex-column">
          <Navigation />
        </nav>
        <main className="col-10 col-md-10 row p-0 m-0">
          <div className="col-4 col-md-4 p-0 border-end bg-light">
            <ListGroup
              users={users}
              selectedUser={selectedUser}
              handleSelectUser={handleSelectUser}
              handleDelete={handleDelete}
              handleSubmit={handleSubmit}
              handleChange={handleChange}
              form={form}
              loading={loading}
              error={error}
              onAddUser={handleAddUserClick}
            />
          </div>
          <div className="col-8 col-md-8 p-0 bg-light">
            <Form
              mode={formMode}
              user={selectedUser}
              form={form}
              onChange={handleChange}
              onSubmit={handleSubmit}
              onEdit={handleEdit}
              onCancel={handleCancel}
              onSave={handleSave}
              onCreate={handleCreate}
              onDelete={handleDeleteUser}
              loading={loading}
              error={error}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
