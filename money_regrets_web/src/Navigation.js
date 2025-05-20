import React from 'react';
import logo from './logo.svg';

function Navigation() {
  return (
    <div className="d-flex flex-column flex-shrink-0 p-3 text-bg-dark min-vh-100">
      <a href="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none">
        <img src={logo} alt="logo" width={40} height={32} className="pe-none me-2" />
        <span className="fs-4">Money Regrets</span>
      </a>
      <hr />
      <ul className="nav nav-pills flex-column mb-auto">
        <li className="nav-item">
          <a href="#" className="nav-link active" aria-current="page">
            <i className="bi bi-people pe-none me-2" style={{ width: 16, height: 16 }}></i>
            Users
          </a>
        </li>
        <li>
          <a href="#" className="nav-link text-white">
            <i className="bi bi-grid pe-none me-2" style={{ width: 16, height: 16 }}></i>
            Dashboard
          </a>
        </li>
        <li>
          <a href="#" className="nav-link text-white">
            <i className="bi bi-cart pe-none me-2" style={{ width: 16, height: 16 }}></i>
            Orders
          </a>
        </li>
        <li>
          <a href="#" className="nav-link text-white">
            <i className="bi bi-box pe-none me-2" style={{ width: 16, height: 16 }}></i>
            Products
          </a>
        </li>
        <li>
          <a href="#" className="nav-link text-white">
            <i className="bi bi-person pe-none me-2" style={{ width: 16, height: 16 }}></i>
            Customers
          </a>
        </li>
      </ul>
      <hr />
      <div className="dropdown">
        <a href="#" className="d-flex align-items-center text-white text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button">
          <img src="https://github.com/mdo.png" alt="" width="32" height="32" className="rounded-circle me-2" />
          <strong>mdo</strong>
        </a>
        <ul className="dropdown-menu dropdown-menu-dark text-small shadow show-on-hover">
          <li><a className="dropdown-item" href="#">New project...</a></li>
          <li><a className="dropdown-item" href="#">Settings</a></li>
          <li><a className="dropdown-item" href="#">Profile</a></li>
          <li><hr className="dropdown-divider" /></li>
          <li><a className="dropdown-item" href="#">Sign out</a></li>
        </ul>
      </div>
    </div>
  );
}

export default Navigation;
