import React, { useRef, useEffect } from 'react';
import logo from './logo.svg';

function Navigation({ children }) {
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

  return (
    <div className="d-flex">
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
      <div className="flex-grow-1">
        <header className="p-3 bg-light d-flex align-items-center">
          <button id="menu-toggle" ref={toggleButtonRef} className="btn btn-outline-secondary me-2" type="button">
            &#9776;
          </button>
          <h1 className="h5 mb-0">Page Title</h1>
        </header>
        <main className="p-3">
          {children || <p>Main content goes here.</p>}
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

export default Navigation;
