import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="bg-blue-600 text-white p-4">
      <nav className="flex justify-between max-w-6xl mx-auto">
        <h1 className="font-bold text-xl">Health Link</h1>
        <div className="space-x-4">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/patients">Patients</Link>
          <Link to="/appointments">Appointments</Link>
          <Link to="/login">Login</Link>
        </div>
      </nav>
    </header>
  );
}
