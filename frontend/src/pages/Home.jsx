import { Link } from "react-router-dom";

function Home() {
  return (
    <section className="home-hero">
      <h1 className="home-title">FurFinds</h1>
      <p className="tagline">Find. Adopt. Love.</p>
      <p className="home-description">
        FurFinds helps you discover and adopt pets across Tamil Nadu with ease. Find your perfect
        companion and give them a loving home.
      </p>
      <div className="home-actions">
        <Link className="button-link home-btn" to="/login">
          Login
        </Link>
        <Link className="button-link secondary home-btn" to="/register">
          Register
        </Link>
      </div>
      <p className="home-features">
        Browse pets • Smart recommendations • Adoption insights • Real-time updates
      </p>
      <p className="home-quote">"Every pet deserves a home. Every home deserves a pet."</p>
    </section>
  );
}

export default Home;
