import React, { useState } from "react";
import axios from "axios";

const TextFilePage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Veuillez sélectionner un fichier texte.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
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
          className="w-full mb-4"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          disabled={!file}
        >
          Envoyer
        </button>
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </form>
      {result && (
        <div className="mt-6 bg-white p-4 rounded shadow w-full max-w-md overflow-x-auto">
          <h2 className="font-bold mb-2">Résultat :</h2>
          <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default TextFilePage; 