import React from 'react';

function Form({
  mode = 'view', // 'view', 'edit', or 'create'
  user,
  form = {},
  onChange,
  onSubmit,
  onEdit,
  onCancel,
  onSave,
  onCreate,
  onDelete,
  loading = false,
  error = ''
}) {
  // Defensive: always use an object for user
  const safeUser = user || {};
  const isReadOnly = mode === 'view';
  const isEdit = mode === 'edit';
  const isCreate = mode === 'create';
  const displayUser = (isCreate || isEdit) ? form : safeUser;

  return (
    <div className="p-0">
      <div className="d-flex align-items-center flex-shrink-0 p-3 link-body-emphasis text-decoration-none border-bottom">
        <span className="bi bi-person pe-none me-2" style={{ fontSize: 24 }} aria-hidden="true"></span>
        <span className="fs-5 fw-semibold flex-grow-1 text-start">{isCreate ? 'Add User' : isEdit ? 'Edit User' : 'User'}</span>
        {!isCreate && !isEdit && (
          <button className="btn btn-danger btn-sm ms-auto" onClick={onDelete} type="button" disabled={loading}>
            <span className="bi bi-trash"></span> Delete
          </button>
        )}
      </div>
      <div className="p-3">
        <form onSubmit={isCreate ? onCreate : isEdit ? onSave : e => e.preventDefault()}>
          {(isReadOnly || isEdit) && (
            <div className="mb-3">
              <label className="form-label">UUID:</label>
              <span className="font-monospace ms-2">{displayUser.uuid || ''}</span>
            </div>
          )}
          <div className="mb-3">
            <label className="form-label">Name</label>
            <input
              name="name"
              className="form-control"
              value={displayUser.name || ''}
              onChange={onChange}
              readOnly={isReadOnly}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Email</label>
            <input
              name="email"
              className="form-control"
              value={displayUser.email || ''}
              onChange={onChange}
              readOnly={isReadOnly}
              required
              type="email"
            />
          </div>
          {error && <div className="alert alert-danger py-1">{error}</div>}
          <div className="d-flex gap-2 justify-content-end">
            {isReadOnly && (
              <>
                <button type="button" className="btn btn-secondary" onClick={onEdit} disabled={loading}>
                  Edit
                </button>
                <button type="button" className="btn btn-danger" onClick={onDelete} disabled={loading}>
                  Delete
                </button>
              </>
            )}
            {isEdit && (
              <>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  Save
                </button>
                <button type="button" className="btn btn-outline-secondary" onClick={onCancel} disabled={loading}>
                  Cancel
                </button>
                {/* Delete button hidden in edit mode */}
              </>
            )}
            {isCreate && (
              <button type="submit" className="btn btn-success" disabled={loading}>
                Create
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

export default Form;
