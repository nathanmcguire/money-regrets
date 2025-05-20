import React from 'react';

function ListGroup({ users, selectedUser, handleSelectUser, loading, error, onAddUser }) {
  return (
    <div className="d-flex flex-column align-items-stretch flex-shrink-0 bg-body-tertiary">
      <div className="d-flex align-items-center flex-shrink-0 p-3 link-body-emphasis text-decoration-none border-bottom justify-content-between">
        <span className="bi bi-people pe-none me-2" style={{ fontSize: 24 }} aria-hidden="true"></span>
        <span className="fs-5 fw-semibold">Users</span>
        <button className="btn btn-success btn-sm ms-auto" onClick={onAddUser}>
          <span className="bi bi-plus-lg"></span> Add
        </button>
      </div>
      {error && <div className="alert alert-danger py-1 mx-2">{error}</div>}
      {loading ? <div className="mx-2">Loading...</div> : (
        <div className="list-group list-group-flush border-bottom scrollarea">
          {users.map((user) => (
            <a
              href="#"
              key={user.uuid}
              className={`list-group-item list-group-item-action py-3 lh-sm${selectedUser && selectedUser.uuid === user.uuid ? ' active text-bg-primary border-primary' : ''}`}
              aria-current={selectedUser && selectedUser.uuid === user.uuid ? 'true' : undefined}
              onClick={e => { e.preventDefault(); handleSelectUser(user); }}
              style={{ cursor: 'pointer' }}
            >
              <div className="d-flex w-100 align-items-center justify-content-between">
                <div>
                  <strong className={`mb-1${selectedUser && selectedUser.uuid === user.uuid ? ' text-white' : ''}`}>{user.name}</strong>
                  <div className={`small${selectedUser && selectedUser.uuid === user.uuid ? ' text-white-75' : ' text-body-secondary'}`}>{user.email}</div>
                  <div className={`small text-secondary font-monospace ${selectedUser && selectedUser.uuid === user.uuid ? ' text-white-50' : ''}`}>{user.uuid}</div>
                </div>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

export default ListGroup;
