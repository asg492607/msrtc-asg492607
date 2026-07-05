export default function Home() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>Your Journey Starts Here</h1>
        <p>Premium transit across Maharashtra. Book your seat today.</p>
        <div className="search-box">
          <input type="text" placeholder="From (e.g., Mumbai)" />
          <input type="text" placeholder="To (e.g., Pune)" />
          <input type="date" />
          <button className="btn-primary">Search Buses</button>
        </div>
      </div>
    </div>
  );
}
