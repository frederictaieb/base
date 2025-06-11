import React, { useState, useRef } from "react";
import axios from "axios";

const TextFilePage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [coords, setCoords] = useState<{ lat: number; lon: number } | null>(null);
  const [timestamp, setTimestamp] = useState<string | null>(null);
  const [locationError, setLocationError] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError("");
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      setLocationError("La géolocalisation n'est pas supportée par ce navigateur.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setCoords({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
        setTimestamp(new Date().toISOString());
        setLocationError("");
      },
      (err) => {
        setLocationError("Impossible d'obtenir la position: " + err.message);
      }
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Veuillez sélectionner un fichier texte.");
      return;
    }

    // Si pas encore défini, créer un timestamp au moment de l'envoi
    if (!timestamp) {
      setTimestamp(new Date().toISOString());
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    if (coords) {
      formData.append("latitude", coords ? coords.lat.toString() : "0");
      formData.append("longitude", coords ? coords.lon.toString() : "0");
    }

    if (timestamp) {
      formData.append("timestamp", timestamp || "");
    }

    console.log("formData", formData);

    try {
      const response = await axios.post(
        "http://localhost:8000/textfile_to_emo",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResult(response.data);
      setError("");
    } catch (err) {
      setError("Erreur lors de l'envoi du fichier ou du traitement côté serveur.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <label htmlFor="file" className="block mb-2 font-semibold">Choisir un fichier texte :</label>
        <input
          type="file"
          id="file"
          accept=".txt"
          onChange={handleFileChange}
          ref={fileInputRef}
          className="hidden"
          aria-label="Sélectionner un fichier texte"
        />
        <button
          type="button"
          onClick={handleButtonClick}
          className="w-full bg-gray-200 text-gray-800 py-2 rounded hover:bg-gray-300 transition mb-2"
        >
          {file ? `Fichier sélectionné : ${file.name}` : "Sélectionner un fichier"}
        </button>
        <button
          type="button"
          onClick={handleGetLocation}
          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition mb-2"
        >
          Obtenir ma position GPS
        </button>
        {coords && (
          <div className="text-green-700 mb-2">
            Position : {coords.lat}, {coords.lon}
          </div>
        )}
        {timestamp && (
          <div className="text-blue-700 mb-2">
            Date/Heure : {new Date(timestamp).toLocaleString()}
          </div>
        )}
        {locationError && <div className="text-red-600 mb-2">{locationError}</div>}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          disabled={!file || loading}
        >
          {loading ? "Envoi en cours..." : "Envoyer"}
        </button>
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </form>
      {result && (
        <div
          className="mt-6 bg-white p-4 rounded shadow w-full max-w-md overflow-x-auto"
          style={{ maxHeight: "350px", overflowY: "auto" }}
        >
          <h2 className="font-bold mb-2">Résultat :</h2>
          <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TextFilePage;
