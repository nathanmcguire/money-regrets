import React, { useEffect, useState, useRef } from 'react';
import { getUsers, createUser, updateUser, deleteUser } from './api';
import logo from './logo.svg';
import ListGroup from './users/ListGroup';
import Form from './users/Form';


function App() {
  const sidebarRef = useRef(null);
  const toggleButtonRef = useRef(null);

  useEffect(() => {
    const toggleButton = toggleButtonRef.current;
    const sidebar = sidebarRef.current;
    if (!toggleButton || !sidebar) return;

    const handleToggle = () => {
      if (window.innerWidth < 768) {
        sidebar.classList.toggle('show');
      } else {
        sidebar.classList.toggle('collapsed');
      }
    };
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        sidebar.classList.remove('show');
      }
    };
    toggleButton.addEventListener('click', handleToggle);
    window.addEventListener('resize', handleResize);
    return () => {
      toggleButton.removeEventListener('click', handleToggle);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

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
    <div className="d-flex min-vh-100">
      {/* Sidebar */}
      <nav
        id="sidebar"
        ref={sidebarRef}
        className="bg-dark text-white p-3"
        style={{
          transition: 'all 0.3s ease',
          minHeight: '100vh',
          width: 250,
        }}
      >
        <div className="d-flex align-items-center mb-4">
          <img src={logo} alt="logo" width={32} height={32} className="me-2" />
          <h4 className="text-white mb-0">Menu</h4>
        </div>
        <ul className="nav flex-column">
          <li className="nav-item"><a className="nav-link text-white" href="#">Dashboard</a></li>
          <li className="nav-item"><a className="nav-link text-white" href="#">Settings</a></li>
          <li className="nav-item"><a className="nav-link text-white" href="#">Users</a></li>
        </ul>
      </nav>
      {/* Main Content */}
      <div className="flex-grow-1 d-flex flex-column">
        <header className="p-3 bg-light d-flex align-items-center">
          <button id="menu-toggle" ref={toggleButtonRef} className="btn btn-outline-secondary me-2" type="button">
            &#9776;
          </button>
          <h1 className="h5 mb-0">Page Title</h1>
        </header>
        <main className="col-10 col-md-10 p-0 row">
          <div className="col-4 col-md-4 p-0">
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
          <div className="col-8 col-md-8 p-0">
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
      <style>{`
        #sidebar {
          transition: all 0.3s ease;
          min-height: 100vh;
        }
        #sidebar.collapsed {
          width: 60px !important;
        }
        #sidebar:not(.collapsed) {
          width: 250px !important;
        }
        @media (max-width: 768px) {
          #sidebar {
            position: absolute;
            left: -250px;
            z-index: 1050;
          }
          #sidebar.show {
            left: 0;
          }
        }
      `}</style>
    </div>
  );
}

export default App;
