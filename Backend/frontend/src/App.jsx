import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
  // state
  const [items, setItems] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [file, setFile] = useState(null);

  // useEffect goes HERE
  useEffect(() => {
    fetchItems();
    fetchJobs();

    const interval = setInterval(() => {
      fetchItems();
      fetchJobs();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // helper functions
  const fetchItems = async () => {
    try {
      const response = await axios.get("/api/items");
      setItems(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchJobs = async () => {
    try {
      const response = await axios.get("/api/jobs");
      setJobs(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    await axios.post("/api/ingest-csv", formData);

    fetchJobs();
    fetchItems();
  };

  return (
    <div className="min-h-screen p-8 bg-slate-100">
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold">Scale Ingestion Dashboard</h1>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white rounded-3xl shadow p-6">
            <h2 className="text-sm text-gray-500">Total Jobs</h2>
            <p className="text-3xl font-bold">8</p>
          </div>

          <div className="bg-white rounded-3xl shadow p-6">
            <h2 className="text-sm text-gray-500">Processing</h2>
            <p className="text-3xl font-bold">1</p>
          </div>

          <div className="bg-white rounded-3xl shadow p-6">
            <h2 className="text-sm text-gray-500">Items Ingested</h2>
            <p className="text-3xl font-bold">23</p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow p-6 space-y-4">
          <h2 className="text-2xl font-semibold">Upload CSV</h2>
          <input type="file" className="border p-2 rounded" />
          <button className="px-4 py-2 rounded-xl bg-black text-white">
            Upload
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="text-2xl font-semibold mb-4">Job Status</h2>

          {jobs.map((job) => (
            <div key={job.id} className="flex justify-between border-b py-3">
              <span>Job #{job.id}</span>
              <span>{job.source}</span>
              <span
                className={`px-3 py-1 rounded-full text-sm font-semibold
                ${
                  job.status === "completed"
                    ? "bg-green-100 text-green-700"
                    : job.status === "failed"
                    ? "bg-red-100 text-red-700"
                    : job.status === "processing"
                    ? "bg-yellow-100 text-yellow-700"
                    : "bg-blue-100 text-blue-700"
                }`}
              >
                {job.status}
              </span>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-3xl shadow p-6">
          <h2 className="text-2xl font-semibold mb-4">Items</h2>

          {items.map((item) => (
            <div key={item.id} className="flex justify-between border-b py-3">
              <span>{item.name}</span>
              <span>{item.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
