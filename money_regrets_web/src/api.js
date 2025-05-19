// src/api.js

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

export async function getUsers() {
  const res = await fetch(`${API_BASE}/users/`);
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
}

export async function createUser(user) {
  const res = await fetch(`${API_BASE}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
  if (!res.ok) throw new Error('Failed to create user');
  return res.json();
}

export async function updateUser(uuid, user) {
  const res = await fetch(`${API_BASE}/users/${uuid}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
  if (!res.ok) throw new Error('Failed to update user');
  return res.json();
}

export async function deleteUser(uuid) {
  const res = await fetch(`${API_BASE}/users/${uuid}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete user');
  return res.json();
}
