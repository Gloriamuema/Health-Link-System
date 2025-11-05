export default function Login() {
  return (
    <div className="max-w-md mx-auto mt-10 p-4 border rounded bg-white shadow">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <form className="flex flex-col space-y-2">
        <input
          type="email"
          placeholder="Email"
          className="border p-2 rounded"
        />
        <input
          type="password"
          placeholder="Password"
          className="border p-2 rounded"
        />
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">
          Sign In
        </button>
      </form>
    </div>
  );
}
