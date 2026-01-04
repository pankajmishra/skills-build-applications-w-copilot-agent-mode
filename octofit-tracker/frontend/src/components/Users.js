import React, { useEffect, useState } from 'react';

const Users = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalData, setModalData] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespaceName ? `https://${codespaceName}-8000.app.github.dev/api/users/` : 'http://localhost:8000/api/users/';

  const fetchData = () => {
    setLoading(true);
    console.log('Fetching Users from', endpoint);
    fetch(endpoint)
      .then((res) => res.json())
      .then((data) => {
        console.log('Users response', data);
        const list = Array.isArray(data) ? data : data.results || [];
        setItems(list);
      })
      .catch((err) => console.error('Users fetch error', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endpoint]);

  const openModal = (row) => { setModalData(row); setShowModal(true); };
  const closeModal = () => { setShowModal(false); setModalData(null); };

  const headers = items.length ? Object.keys(items[0]) : [];

  return (
    <div className="card data-card">
      <div className="card-body">
        <h2 className="h4 card-title">Users</h2>
        <p>Endpoint: <code>{endpoint}</code></p>
        <div className="mb-2">
          <button className="btn btn-primary me-2" onClick={fetchData} disabled={loading}>{loading ? 'Refreshing...' : 'Refresh'}</button>
        </div>

        {items.length ? (
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead>
                <tr>
                  {headers.map((h) => <th key={h}>{h}</th>)}
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it, idx) => (
                  <tr key={idx}>
                    {headers.map((h) => (
                      <td key={h}>{typeof it[h] === 'object' ? JSON.stringify(it[h]) : String(it[h] ?? '')}</td>
                    ))}
                    <td>
                      <button className="btn btn-sm btn-outline-secondary" onClick={() => openModal(it)}>View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="alert alert-info">No users found.</div>
        )}

        {showModal && modalData && (
          <div className="modal d-block" tabIndex="-1" role="dialog" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
            <div className="modal-dialog modal-lg" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">User detail</h5>
                  <button type="button" className="btn-close" aria-label="Close" onClick={closeModal}></button>
                </div>
                <div className="modal-body">
                  <pre>{JSON.stringify(modalData, null, 2)}</pre>
                </div>
                <div className="modal-footer">
                  <button className="btn btn-secondary" onClick={closeModal}>Close</button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Users;
