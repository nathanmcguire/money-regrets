import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { getUsers, createUser, updateUser, deleteUser } from './api';

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      fetchUsers();
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Manage Users</h2>
        <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
          <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
          <input name="password" placeholder="Password" value={form.password} onChange={handleChange} required type="password" />
          <button type="submit" disabled={loading}>Add User</button>
        </form>
        {error && <div style={{ color: 'red' }}>{error}</div>}
        {loading ? <div>Loading...</div> : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {users.map((user) => (
              <li key={user.uuid} style={{ marginBottom: 10 }}>
                <span>{user.name} ({user.email})</span>
                <button onClick={() => handleDelete(user.uuid)} style={{ marginLeft: 10 }}>Delete</button>
              </li>
            ))}
          </ul>
        )}
      </header>
    </div>
  );
}

export default App;
