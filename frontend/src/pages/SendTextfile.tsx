import React, { useState, useEffect, useRef } from "react";
import Drawer from "../components/Drawer";
import axios from "axios";

const SendTextfile: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [form, setForm] = useState({
    latitude: "",
    longitude: "",
    now: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
    date: new Date().toLocaleDateString(),
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [timestamp, setTimestamp] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        setForm((f) => ({
          ...f,
          latitude: latitude.toFixed(4),
          longitude: longitude.toFixed(4),
        }));
      },
      (err) => console.error("Erreur GPS :", err)
    );
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setForm((f) => ({
        ...f,
        now: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
        date: new Date().toLocaleDateString(),
      }));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      setError("Veuillez sélectionner un fichier texte.");
      return;
    }

    const currentTimestamp = timestamp || new Date().toISOString();
    setTimestamp(currentTimestamp);
    setLoading(true);
    setError("");
    setMessage("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("latitude", form.latitude);
    formData.append("longitude", form.longitude);
    formData.append("timestamp", currentTimestamp);

    try {
      const response = await axios.post("http://localhost:8000/textfile_to_xrp", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);
      setMessage("Fichier envoyé avec succès !");
    } catch (err) {
      setError("Erreur lors de l'envoi du fichier ou du traitement côté serveur.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Drawer isOpen={isOpen} onClose={onClose}>
      <h2 className="text-2xl font-bold text-center mb-6 text-white">Analysis</h2>
      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-black p-6 rounded-xl shadow-lg"
      >
        {/* Date & Time */}
        {["date", "now"].map((field) => (
          <div className="flex flex-col gap-1" key={field}>
            <span className="text-sm font-medium text-white">{field === "date" ? "Date" : "Now"}</span>
            <span className="block rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-400 bg-black">
              {form[field as "date" | "now"]}
            </span>
          </div>
        ))}

        {/* Coordinates */}
        {["latitude", "longitude"].map((coord) => (
          <label className="flex flex-col gap-1" key={coord}>
            <span className="text-sm font-medium text-white">{coord.charAt(0).toUpperCase() + coord.slice(1)}</span>
            <input
              type="number"
              step="any"
              name={coord}
              value={form[coord as "latitude" | "longitude"]}
              onChange={handleChange}
              required
              className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 bg-black focus:border-blue-500 focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </label>
        ))}

        {/* File Upload */}
        <label className="flex flex-col gap-1 sm:col-span-2">
          <span className="text-sm font-medium text-white">Text File</span>
          <div
            onClick={(e) => {
              if (e.target === e.currentTarget) {
                fileInputRef.current?.click();
              }
            }}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`w-full flex items-center justify-center border border-dashed border-gray-300 rounded-lg py-6 cursor-pointer transition ${
              dragOver ? "bg-blue-900" : "bg-black hover:bg-blue-900"
            }`}
          >
            {selectedFile ? (
              <span className="text-gray-300">{selectedFile.name}</span>
            ) : (
              <span className="text-gray-400">Click or drag a file here</span>
            )}
            <input
              type="file"
              accept=".txt"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
        </label>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="sm:col-span-2 w-1/2 mx-auto py-2 mt-2 bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white rounded-lg font-semibold text-base shadow-md transition-all duration-200 flex justify-center items-center"
        >
          {loading ? "Envoi..." : "Envoyer"}
        </button>

        {/* Message / Error */}
        {message && (
          <p className="sm:col-span-2 mt-2 text-center text-xs italic text-green-600">{message}</p>
        )}
        {error && (
          <p className="sm:col-span-2 mt-2 text-center text-xs italic text-red-500">{error}</p>
        )}

        {/* Result */}
        {result && (
          <div className="sm:col-span-2 mt-4 p-4 bg-gray-800 text-gray-400 rounded-lg text-xs italic border border-gray-600">
            <h3 className="font-semibold mb-2">Résultat :</h3>
            <pre className="whitespace-pre-wrap break-words italic">{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </form>
    </Drawer>
  );
};

export default SendTextfile;
