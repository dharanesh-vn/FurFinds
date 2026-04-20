import { Link } from "react-router-dom";

function Home() {
  return (
    <section className="card center">
      <h1>FurFinds</h1>
      <p className="tagline">Find. Adopt. Love.</p>
      <p>Welcome to FurFinds, a smart pet adoption platform.</p>
      <div className="row">
        <Link className="button-link" to="/login">
          Login
        </Link>
        <Link className="button-link secondary" to="/register">
          Register
        </Link>
      </div>
    </section>
  );
}

export default Home;
