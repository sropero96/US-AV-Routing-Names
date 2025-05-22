import { useState } from 'react';
import './App.css';

function App() {
  const [routingNumber, setRoutingNumber] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    if (!/^\d{9}$/.test(routingNumber)) {
      setError('El routing number debe tener exactamente 9 dígitos.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/lookup?routing_number=${routingNumber}`);
      if (!res.ok) {
        throw new Error('No se encontró información para ese routing number.');
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header className="header">
        <img src="/PROMETEO_LOGO.png" alt="Prometeo Logo" className="logo" />
        <div className="title">La API Bancaria Sin Fronteras</div>
        <div className="subtitle">Consulta información de bancos en USA por Routing Number</div>
      </header>
      <main>
        <div className="container">
          <form onSubmit={handleSubmit} className="routing-form">
            <input
              type="text"
              placeholder="Routing Number (9 dígitos)"
              value={routingNumber}
              onChange={e => setRoutingNumber(e.target.value)}
              maxLength={9}
              pattern="\d{9}"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Consultando...' : 'Consultar'}
            </button>
          </form>
          {error && <div className="error">{error}</div>}
          {result && (
            <div className="result-card">
              <h2>{result.bank_name}</h2>
              <p><b>Routing Number:</b> {result.routing_number}</p>
              <p><b>Ciudad:</b> {result.city}</p>
              <p><b>Estado:</b> {result.state}</p>
              <p><b>Dirección:</b> {result.address}</p>
              <p><b>Código Postal:</b> {result.postal_code}</p>
              <p><b>Teléfono:</b> {result.phone}</p>
            </div>
          )}
        </div>
      </main>
      <footer className="footer">
        <span className="footer-disclaimer">
          Disclaimer sobre la fuente principal<br />
          IMPORTANTE: Este proyecto utiliza como fuente principal la API pública de routingnumbers.info, que depende de un directorio descargable de la Reserva Federal. NOTA: Desde el 9 de diciembre de 2018, la Reserva Federal eliminó el directorio descargable del que depende este sitio. Por lo tanto, no existen actualizaciones oficiales después de esa fecha y los datos pueden estar desactualizados. Consulta routingnumbers.info para más detalles.
        </span>
      </footer>
    </>
  );
}

export default App;
